from django.contrib import admin
from .models import Empleado, Adelanto

class AdelantoInline(admin.TabularInline):
    model = Adelanto
    extra = 1

class EmpleadoAdmin(admin.ModelAdmin):
    inlines = [AdelantoInline]

admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Adelanto)
