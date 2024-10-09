from django.urls import path
from . import views

urlpatterns = [
    path('' ,views.index, name="index" ),
    path('emp/', views.empleado_create, name="empleado_create"),
    path('modif/<int:pk>', views.modif, name="empleado_mofif")
]
