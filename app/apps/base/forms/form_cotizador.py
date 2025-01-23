from django import forms


class CotizadorForm(forms.Form):
    opc_frecuencia = [
        ("1", "Mensual"), 
        ("2", "Quincena"),
        ("3", "Semanal"),
        ("4", "Diario"),
    ]
    opc_plazo = [(x, x) for x in range(1,13)]

    frecuencia = forms.ChoiceField(choices=opc_frecuencia, required=True)
    plazo_meses = forms.ChoiceField(choices=opc_plazo, required=True)
    monto = forms.CharField(max_length=7, required=True)
    tasa = forms.DecimalField(max_digits=5, decimal_places=2, required=True)
    date_registered = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date'}), label="Fecha 1ra cuota")
    
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

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
