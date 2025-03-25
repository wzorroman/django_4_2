from django import forms


class CotizadorForm(forms.Form):
    opc_frecuencia = [
        ("1", "Mensual"), 
        ("2", "Quincena"),
        ("3", "Semanal"),
        ("4", "Diario"),
    ]
    opc_plazo = [(x, x) for x in range(1, 13)]

    payment_frequency = forms.ChoiceField(choices=opc_frecuencia, required=True)
    term_months = forms.ChoiceField(choices=opc_plazo, required=True, label="Plazo en meses")
    initial_amount = forms.CharField(max_length=7, required=True)
    interest_rate = forms.DecimalField(max_digits=5, decimal_places=2, required=True)
    first_payment_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date'}),
                                         label="Fecha 1ra cuota")
    include_saturday = forms.BooleanField(label="Incluir Sab", required=False,
                                          widget=forms.CheckboxInput(
                                              attrs={'class': 'form-check-input form-control-sm'}))
    include_sunday = forms.BooleanField(label="Incluir Dom", required=False,
                                        widget=forms.CheckboxInput(
                                            attrs={'class': 'form-check-input form-control-sm'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs.update(
                {
                    "class": "form-control",
                    "autocomplete": "off",
                }
            )
        # self.fields["address"].widget.attrs.update({"class": "form-control uppercase"})
        # self.fields["ubigeo_via"].initial = 1
