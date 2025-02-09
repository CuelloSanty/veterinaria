from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Empleado, Adelanto, Atencione, ArticuloAtencion, Pedido, DetallePedido, Venta, DetalleVenta, Subscription
from django.contrib.auth.forms import AuthenticationForm
# Empleado Form
class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'FechaContratacion', 'TurnoChoice', 'sueldo']
class FormSubscription(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ["Gmail","asunto", "Nombre"]
        widgets = {
        "Gmail":forms.TextInput(attrs={"type":"email", "placeholder":"Example@Gmail.com"}),
        "asunto":forms.TextInput(attrs={"type":"text", "placeholder":"Boletin de productos"}),
        "Nombre":forms.TextInput(attrs={"type":"text", "placeholder":"Nombre"})

        }

        
class AdelantoForm(forms.ModelForm):
    class Meta:
        model = Adelanto
        fields = ['Monto', 'FechaAdelanto']
        widgets = {
        "Monto":forms.TextInput(attrs={"type":"number"}),
        "FechaAdelanto":forms.TextInput(attrs={"type":"date"})
        }
AdelantoFormSet = inlineformset_factory(Empleado,Adelanto, form=AdelantoForm, extra=2, can_delete=True)

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )
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


# Pedidos Forms
class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ('__all__')
        exclude = ('id',)

class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ('__all__')
        exclude = ('id',)
DetallePedidoFormSet = inlineformset_factory(Pedido, DetallePedido, form=DetallePedidoForm, extra=2, can_delete=True)

# Ventas Forms 
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ('__all__')
        exclude = ('id',)

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ('__all__')
        exclude = ('id',)

VentaFormSet = inlineformset_factory(Venta, DetalleVenta, form=DetalleVentaForm, extra=2, can_delete=True)