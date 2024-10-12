from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Inicio'),
    path('emp/' ,views.EmpViews.as_view(), name="empleados lista" ),
    path('emp/create/', views.empleado_create, name="empleado_create"),
    path('emp/modif/<int:pk>/', views.empleado_modif, name="empleado_mofif"),
    path('emp/delete/<int:pk>/', views.empleado_delete, name="empleado_mofif"),

    path('Articulos/Lista/', views.Art_list.as_view(), name="list"),
    path('Articulos/add/', views.Art_Create.as_view(), name="Add"),
    path('Articulos/<int:pk>/edit/', views.Art_Update.as_view(), name="Update"),
    path('Articulos/<int:pk>/delete/', views.Art_Delete.as_view(), name="Delete"),



]
