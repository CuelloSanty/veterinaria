from django.contrib import admin
from .models import Empleado, Adelanto, Proveedore, Articulo, Cliente, Mascota, Atencione, ArticuloAtencion, Pedido, DetallePedido, Venta, DetalleVenta, Subscription

class AdelantoInline(admin.TabularInline):
    model = Adelanto
    extra = 1

class EmpleadoAdmin(admin.ModelAdmin):
    inlines = [AdelantoInline]

class ArtAteInline(admin.TabularInline):
    model = ArticuloAtencion
    extra = 1

class ArtAtenAdmin(admin.ModelAdmin):
    inlines = [ArtAteInline]

class PedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 2

class PedidoAdmin(admin.ModelAdmin):
    inlines = [PedidoInline]

class VentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 2

class VentaAdmin(admin.ModelAdmin):
    inlines = [VentaInline]


admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Adelanto)

admin.site.register(Atencione, ArtAtenAdmin)
admin.site.register(ArticuloAtencion)

admin.site.register(Pedido, PedidoAdmin)
admin.site.register(DetallePedido)

admin.site.register(Venta, VentaAdmin)
admin.site.register(DetalleVenta)

admin.site.register(Proveedore)
admin.site.register(Articulo)

admin.site.register(Cliente)
admin.site.register(Mascota)

admin.site.register(Subscription)