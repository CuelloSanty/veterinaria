from django.urls import path
from . import views

urlpatterns = [
    path('' ,views.EmpViews.as_view(), name="index" ),
    path('emp/', views.empleado_create, name="empleado_create"),
    path('emp/modif/<int:pk>', views.modif, name="empleado_mofif")
]
