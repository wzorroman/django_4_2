from datetime import date, datetime, timedelta
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView


from ..forms.form_cotizador import CotizadorForm


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
            'CLASS_MENU_MAESTROS': "menu-open",
            'CLASS_MENU_MAESTROS_SELECT': "active",
            'CLASS_MENU_0_CLIENT': "menu-open",
            'CLASS_MENU_0_CLIENT_SELECT': "active",
            'CLASS_MENU_1_CLIENT_ADD': "",
            'CLASS_MENU_1_CLIENT_LIST': "active",
            'title_page': title_page,
            'main_title_content': main_title_content,
            'main_subtitle_content': main_subtitle_content,
            'subtitle_table': subtitle_table,
        })
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        fecha_final = date.today() + timedelta(days=30)
        form.fields["date_registered"].initial = fecha_final.strftime("%Y-%m-%d")
        return form
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.send_email()
        # return super().form_valid(form)

        frecuencia = form.cleaned_data['frecuencia']
        plazo_meses = form.cleaned_data['plazo_meses']
        monto = form.cleaned_data['monto']
        tasa = form.cleaned_data['tasa']
        date_registered = form.cleaned_data['date_registered']

        # Redirigir a la vista destino con los datos
        return self.redirect_to_destino(frecuencia, plazo_meses, monto, tasa, date_registered)

    def redirect_to_destino(self, frecuencia, plazo_meses, monto, tasa,date_registered):
        return redirect(reverse('base:cronograma') + f'?frec={frecuencia}&pm={plazo_meses}&mt={monto}&ta={tasa}&fpc={date_registered}')
        

class CronogramaReporte(TemplateView):
    template_name = 'cotizador/cronograma.html'
    data_extra = {}
    
    def dispatch(self, request, *args, **kwargs):
        print(self.request.GET)

        frecuencia = self.request.GET.get("frec")
        plazo_meses = self.request.GET.get("pm")
        monto = self.request.GET.get("mt")
        tasa = self.request.GET.get("ta")
        fecha_cuota = self.request.GET.get("fpc")

        if not (frecuencia and monto and tasa and plazo_meses and fecha_cuota):
            messages.warning(request, "Necesita llenar los campos correctamente")
            return HttpResponseRedirect(reverse("base:cotizador"))
        
        self.data_extra["frecuencia"] = int(frecuencia)
        self.data_extra["plazo_meses"] = int(plazo_meses)
        self.data_extra["monto"] = float(monto)
        self.data_extra["tasa"] = float(tasa)
        self.data_extra["fecha_cuota"] = fecha_cuota
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

    def procesar_cuotas(self):
        cuota = 0
        nro_cuotas = 1
        frecuencia = self.data_extra["frecuencia"]
        plazo_meses = self.data_extra["plazo_meses"]
        monto = self.data_extra["monto"]
        tasa = self.data_extra["tasa"]
        fecha_cuota = self.data_extra["fecha_cuota"]

        cuota_1 = datetime.strptime(fecha_cuota, "%Y-%m-%d")

        interes_total = round(monto * (tasa /100) * plazo_meses, 2) 
        total_cancelar = monto + interes_total
        cuota_mensual = round(total_cancelar / plazo_meses, 2)
        cuota_quincenal = round(cuota_mensual / 2, 2)
        cuota_semanal = round(cuota_mensual / 4, 2)
        cuota_diaria = round(cuota_mensual / 30, 2)
        if frecuencia == 1:
            frecuencia_desc = "Mensual"
            cuota = cuota_mensual
            nro_cuotas = plazo_meses
            cant_dias = 30
        elif frecuencia == 2:
            frecuencia_desc = "Quincenal"
            cuota = cuota_quincenal
            nro_cuotas = plazo_meses * 2
            cant_dias = 15
        elif frecuencia == 3:
            frecuencia_desc = "Semanal"
            cuota = cuota_semanal
            nro_cuotas = plazo_meses * 4
            cant_dias = 7
        elif frecuencia == 4:
            frecuencia_desc = "Diario"
            cuota = cuota_diaria
            nro_cuotas = plazo_meses * 30
            cant_dias = 1

        print(f"cuota : {cuota}")
        print(f"nro_cuotas : {nro_cuotas}")
        print(f"total_cancelar : {total_cancelar}")
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

        self.data_extra["frec_descripcion"] = frecuencia_desc
        self.data_extra["interes_total"] = interes_total
        self.data_extra["cuota"] = cuota
        self.data_extra["nro_cuotas"] = nro_cuotas
        self.data_extra["monto_total"] = total_cancelar
        self.data_extra["data_cuotas"] = data_cuotas
        