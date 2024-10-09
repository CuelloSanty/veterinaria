from django import forms
from django.forms import modelformset_factory
from .models import Empleado, Adelanto

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'FechaContratacion', 'TurnoChoice', 'sueldo']

class AdelantoForm(forms.ModelForm):
    class Meta:
        model = Adelanto
        fields = ['Monto', 'FechaAdelanto']
        widgets = {
        "Monto":forms.TextInput(attrs={"type":"number"}),
        "FechaAdelanto":forms.TextInput(attrs={"type":"date"})
        }
AdelantoFormSet = modelformset_factory(Adelanto, form=AdelantoForm, extra=2)
