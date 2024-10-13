from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Empleado, Adelanto, Atencione, ArticuloAtencion

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
AdelantoFormSet = inlineformset_factory(Empleado,Adelanto, form=AdelantoForm, extra=2, can_delete=True)


# Atencion Form
class AtencionForm(forms.ModelForm):
    class Meta:
        model = Atencione
        fields = ('__all__')
        exclude = ('id',)

class ArtAtencion(forms.ModelForm):
    class Meta:
        model = ArticuloAtencion
        fields = ('__all__')
        exclude = ('id',)

ArtAtencionFormSet = inlineformset_factory(Atencione, ArticuloAtencion, form=ArtAtencion, extra=2,can_delete=True)

