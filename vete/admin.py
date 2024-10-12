from django.contrib import admin
from .models import Empleado, Adelanto, Proveedore, Articulo, Cliente, Mascota

class AdelantoInline(admin.TabularInline):
    model = Adelanto
    extra = 1

class EmpleadoAdmin(admin.ModelAdmin):
    inlines = [AdelantoInline]

admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Adelanto)

admin.site.register(Proveedore)
admin.site.register(Articulo)

admin.site.register(Cliente)
admin.site.register(Mascota)
