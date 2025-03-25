from datetime import date, datetime, timedelta
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
import snoop

from ..decoradores import medir_tiempo
from ..forms.form_cotizador import CotizadorForm
from ...commons.constants import FRECUENCY_MONTHLY, FRECUENCY_FORTNIGHTLY, FRECUENCY_MONTHLY_STR, \
    FRECUENCY_FORTNIGHTLY_STR, FRECUENCY_WEEKLY_STR, FRECUENCY_WEEKLY, FRECUENCY_DAILY, FRECUENCY_DAILY_STR
from ...utils.dates import count_days_in_month, calculate_date_info


class CotizadorDemoView(FormView):
    template_name = 'cotizador/cotizador.html'
    form_class = CotizadorForm
    # success_url = "/base/cronograma"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        title_page = "Maestro | Client"
        main_title_content = "Cotizador"
        main_subtitle_content = "Ingrese datos"
        subtitle_table = "Formulario"

        context.update({
            #'CLASS_MENU_MAESTROS': "menu-open",
            #'CLASS_MENU_MAESTROS_SELECT': "active",
            #'CLASS_MENU_0_CLIENT': "menu-open",
            #'CLASS_MENU_0_CLIENT_SELECT': "active",
            #'CLASS_MENU_1_CLIENT_ADD': "",
            #'CLASS_MENU_1_CLIENT_LIST': "active",
            'title_page': title_page,
            'main_title_content': main_title_content,
            'main_subtitle_content': main_subtitle_content,
            'subtitle_table': subtitle_table,
        })
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        fecha_final = date.today() + timedelta(days=30)
        form.fields["first_payment_date"].initial = fecha_final.strftime("%Y-%m-%d")
        form.fields["include_saturday"].initial = True
        form.fields["include_sunday"].initial = True
        return form
    
    def form_valid(self, form):
        payment_frequency = form.cleaned_data['payment_frequency']
        term_months = form.cleaned_data['term_months']
        initial_amount = form.cleaned_data['initial_amount']
        interest_rate = form.cleaned_data['interest_rate']
        first_payment_date = form.cleaned_data['first_payment_date']
        inc_sab = form.cleaned_data['include_saturday']
        inc_dom = form.cleaned_data['include_sunday']

        return self.redirect_to_schedule(payment_frequency, term_months, initial_amount,
                                         interest_rate, first_payment_date, inc_sab, inc_dom)

    def redirect_to_schedule(self, payment_frequency, term_months, initial_amount, interest_rate,
                             first_payment_date, inc_sab, inc_dom):
        values = f'?frec={payment_frequency}&pm={term_months}&mt={initial_amount}&ta={interest_rate}'\
                 f'&fpc={first_payment_date}&inc_sab={inc_sab}&inc_dom={inc_dom}'
        return redirect(reverse('base:cronograma') + values)
        

class CronogramaReporte(TemplateView):
    template_name = 'cotizador/cronograma.html'
    data_extra = {}
    
    def dispatch(self, request, *args, **kwargs):
        # print(self.request.GET)

        frecuencia = self.request.GET.get("frec")
        plazo_meses = self.request.GET.get("pm")
        monto = self.request.GET.get("mt")
        tasa = self.request.GET.get("ta")
        fecha_cuota = self.request.GET.get("fpc")
        incluye_sab = self.request.GET.get("inc_sab")
        incluye_dom = self.request.GET.get("inc_dom")

        if not (frecuencia and monto and tasa and plazo_meses and fecha_cuota):
            messages.warning(request, "Necesita llenar los campos correctamente")
            return HttpResponseRedirect(reverse("base:quoter"))
        
        self.data_extra["frecuencia"] = int(frecuencia)
        self.data_extra["plazo_meses"] = int(plazo_meses)
        self.data_extra["monto"] = float(monto)
        self.data_extra["tasa"] = float(tasa)
        self.data_extra["fecha_cuota"] = fecha_cuota
        self.data_extra["incluye_sab"] = eval(incluye_sab.title())  # convert boolean
        self.data_extra["incluye_dom"] = eval(incluye_dom.title())  # convert boolean
        self.procesar_cuotas()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        title_page = "Maestro | Client"
        main_title_content = "Cronograma"
        main_subtitle_content = "Simulacion del cronograma"
        subtitle_table = "Formulario"

        context.update({
            # 'CLASS_MENU_MAESTROS': "menu-open",
            # 'CLASS_MENU_MAESTROS_SELECT': "active",
            # 'CLASS_MENU_0_CLIENT': "menu-open",
            # 'CLASS_MENU_0_CLIENT_SELECT': "active",
            # 'CLASS_MENU_1_CLIENT_ADD': "",
            # 'CLASS_MENU_1_CLIENT_LIST': "active",
            'title_page': title_page,
            'main_title_content': main_title_content,
            'main_subtitle_content': main_subtitle_content,
            'subtitle_table': subtitle_table,
            'data': self.data_extra
        })
        
        return context

    @medir_tiempo
    def procesar_cuotas(self):
        cuota = 0
        nro_cuotas = 1
        frecuencia = self.data_extra["frecuencia"]
        plazo_meses = self.data_extra["plazo_meses"]
        monto = self.data_extra["monto"]
        tasa = self.data_extra["tasa"]
        fecha_cuota = self.data_extra["fecha_cuota"]
        incluye_sab = self.data_extra["incluye_sab"]
        incluye_dom = self.data_extra["incluye_dom"]

        cuota_1 = datetime.strptime(fecha_cuota, "%Y-%m-%d")

        interes_total = round(monto * (tasa /100) * plazo_meses, 2) 
        total_cancelar = monto + interes_total
        cuota_mensual = round(total_cancelar / plazo_meses, 2)

        if frecuencia == FRECUENCY_DAILY:
            return self.calcular_cuotas_diarias(
                plazo_meses,
                cuota_1,
                interes_total,
                total_cancelar,
                incluye_sab,
                incluye_dom
            )

        elif frecuencia == FRECUENCY_MONTHLY:
            frecuencia_desc = FRECUENCY_MONTHLY_STR
            cuota = cuota_mensual
            nro_cuotas = plazo_meses
            cant_dias = 30
        elif frecuencia == FRECUENCY_FORTNIGHTLY:
            frecuencia_desc = FRECUENCY_FORTNIGHTLY_STR
            cuota = round(cuota_mensual / 2, 2)
            nro_cuotas = plazo_meses * 2
            cant_dias = 15
        elif frecuencia == FRECUENCY_WEEKLY:
            frecuencia_desc = FRECUENCY_WEEKLY_STR
            cuota = round(cuota_mensual / 4, 2)
            nro_cuotas = plazo_meses * 4
            cant_dias = 7

        # print(f"cuota : {cuota}")
        # print(f"nro_cuotas : {nro_cuotas}")
        # print(f"total_cancelar : {total_cancelar}")
        data_cuotas = {}
        
        cuotas_pendientes = nro_cuotas
        capital_actual = total_cancelar
        i = 0
        while i < cuotas_pendientes:
            if i == 0:
                data_cuotas[i] = {
                    "nro": 1,
                    "fecha": cuota_1,
                    "fecha_str": cuota_1.strftime("%d-%m-%Y"),
                    "cuota": cuota,
                    "capital": capital_actual
                }
            else:
                fecha_prev = data_cuotas[i-1]["fecha"]
                sgt_fecha = fecha_prev + timedelta(days=cant_dias)
                capital_actual -= cuota
                data_cuotas[i] = {
                    "nro": i + 1,
                    "fecha": sgt_fecha,
                    "fecha_str": sgt_fecha.strftime("%d-%m-%Y"),
                    "cuota": cuota,
                    "capital": capital_actual
                }
            i += 1

        self.data_extra["es_diario"] = False
        self.data_extra["frec_descripcion"] = frecuencia_desc
        self.data_extra["interes_total"] = interes_total
        self.data_extra["cuota"] = cuota
        self.data_extra["nro_cuotas"] = nro_cuotas
        self.data_extra["monto_total"] = total_cancelar
        self.data_extra["data_cuotas"] = data_cuotas

    def calcular_cuotas_diarias(
            self,
            plazo_meses,
            cuota_1,
            interes_total,
            total_cancelar,
            incluye_sab,
            incluye_dom,
    ):
        data_cuotas = {}

        # Calculate the last date to pay on the schedule
        current_year = cuota_1.year
        current_month = cuota_1.month
        data_aux = count_days_in_month(current_year, current_month)
        # total_days_to_plus = data_aux["total_days"] - cuota_1.day
        total_days_to_plus = data_aux["total_days"]
        if plazo_meses == 1:
            total_days_to_plus = 29
        elif plazo_meses != 1:
            days_aditional = 0
            for _ in range(plazo_meses-1):
                current_month += 1
                if current_month > 12:
                    current_year += 1
                    current_month = 1
                data_aux = count_days_in_month(current_year, current_month)
                days_aditional += data_aux["total_days"]

            total_days_to_plus += days_aditional

        last_day = cuota_1 + timedelta(days=total_days_to_plus)

        # calculate fee amount
        data_days = calculate_date_info(cuota_1.strftime("%Y-%m-%d"), last_day.strftime("%Y-%m-%d"))
        nro_cuotas = data_days['total_days']

        rango_info_dias = data_days['range_days']
        if not incluye_sab:
            nro_cuotas -= data_days['saturdays']
        if not incluye_dom:
            nro_cuotas -= data_days['sundays']
        monto_cuota = round(total_cancelar/nro_cuotas, 2)

        # Scheduler
        capital_actual = total_cancelar
        current_count = 0
        for key, value in rango_info_dias.items():
            if value["day_number"] == 5 and not incluye_sab:
                continue
            if value["day_number"] == 6 and not incluye_dom:
                continue

            current_count += 1
            if current_count == nro_cuotas:  # last paid
                capital_actual = monto_cuota
            data_cuotas[key] = {
                "nro": current_count,
                "fecha": value["date"],
                "fecha_str": value["date"],
                "dia_desc": value["day_of_week_spa"],
                "mes_desc": value["month_desc"],
                "cuota": monto_cuota,
                "capital": capital_actual
            }
            capital_actual -= monto_cuota

        self.data_extra["es_diario"] = True
        self.data_extra["frec_descripcion"] = FRECUENCY_DAILY_STR
        self.data_extra["interes_total"] = interes_total
        self.data_extra["cuota"] = monto_cuota
        self.data_extra["nro_cuotas"] = nro_cuotas
        self.data_extra["monto_total"] = total_cancelar
        self.data_extra["data_cuotas"] = data_cuotas
        return True
