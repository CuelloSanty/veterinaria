from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_public, name='Inicio'),
    path('index-admin/', views.index_private, name='cosas'),

    path('Empleado/Lista' ,views.EmpViews.as_view(), name="empleados lista" ),
    path('Empleado/create/', views.empleado_create, name="empleado_create"),
    path('Empleado/modif/<int:pk>/', views.empleado_modif, name="empleado_mofif"),
    path('Empleado/delete/<int:pk>/', views.empleado_delete, name="empleado_mofif"),

    path('Articulos/Lista/', views.Art_list.as_view(), name="list empleado"),
    path('Articulos/add/', views.Art_Create.as_view(), name="Add"),
    path('Articulos/<int:pk>/edit/', views.Art_Update.as_view(), name="Update"),
    path('Articulos/<int:pk>/delete/', views.Art_Delete.as_view(), name="Delete"),

    path('Proveedor/Lista/', views.Prov_List.as_view(), name="lista Proveedor"),
    path('Proveedor/add/', views.Prov_Create.as_view(), name="Add"),
    path('Proveedor/<int:pk>/edit/', views.Prov_Update.as_view(), name="Update"),
    path('Proveedor/<int:pk>/delete/', views.Prov_Delete.as_view(), name="Delete"),

    path('Cliente/Lista/', views.Client_List.as_view(), name="lista Cliente"),
    path('Cliente/add/', views.Client_Create.as_view(), name="Add"),
    path('Cliente/<int:pk>/edit/', views.Client_Update.as_view(), name="Update"),
    path('Cliente/<int:pk>/delete/', views.Client_Delete.as_view(), name="Delete"),

    path('Mascota/Lista/', views.Masc_List.as_view(), name="lista Mascota"),
    path('Mascota/add/', views.Masc_Create.as_view(), name="Add"),
    path('Mascota/<int:pk>/edit/', views.Masc_Update.as_view(), name="Update"),
    path('Mascota/<int:pk>/delete/', views.Masc_Delete.as_view(), name="Delete"),


    path('Atenciones/Lista/' ,views.Atencion_List.as_view(), name="Atencion lista" ),
    path('Atencion/create/', views.Atencion_Create, name="empleado_create"),
    path('Atencion/edit/<int:pk>/', views.Atencion_Update, name="empleado_mofif"),
    path('Atencion/delete/<int:pk>/', views.Atencion_Delete, name="empleado_mofif"),

    path('Pedidos/Lista/' ,views.Pedidos_List.as_view(), name="Atencion lista" ),
    path('Pedidos/create/', views.Pedidos_Create, name="empleado_create"),
    path('Pedidos/edit/<int:pk>/', views.Pedidos_Update, name="empleado_mofif"),
    path('Pedidos/delete/<int:pk>/', views.Pedidos_Delete, name="empleado_mofif"),

    path('Ventas/Lista/' ,views.Ventas_List.as_view(), name="Atencion lista" ),
    path('Ventas/create/', views.Ventas_Create, name="empleado_create"),
    path('Ventas/edit/<int:pk>/', views.Ventas_Update, name="empleado_mofif"),
    path('Ventas/delete/<int:pk>/', views.ventas_Delete, name="empleado_mofif"),

]

