from django.urls import path
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index_public, name='Inicio'),
    
    path('login/', LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=LoginForm
    ), name='login'),
    path('Cerrar-session/', views.LogOut),

    path('Empleado/Lista/', login_required(views.EmpViews.as_view()), name="empleados lista" ),
    path('Empleado/create/',login_required(views.empleado_create), name="empleado_create"),
    path('Empleado/modif/<int:pk>/', login_required(views.empleado_modif), name="empleado_mofif"),
    path('Empleado/delete/<int:pk>/', login_required(views.empleado_delete), name="empleado_mofif"),

    path('Articulos/Lista/', login_required(views.Art_list.as_view()), name="list empleado"),
    path('Articulos/add/', login_required(views.Art_Create.as_view()), name="Add"),
    path('Articulos/<int:pk>/edit/', login_required(views.Art_Update.as_view()), name="Update"),
    path('Articulos/<int:pk>/delete/', login_required(views.Art_Delete.as_view()), name="Delete"),

    path('Proveedor/Lista/', login_required(views.Prov_List.as_view()), name="lista Proveedor"),
    path('Proveedor/add/', login_required(views.Prov_Create.as_view()), name="Add"),
    path('Proveedor/<int:pk>/edit/', login_required(views.Prov_Update.as_view()), name="Update"),
    path('Proveedor/<int:pk>/delete/', login_required(views.Prov_Delete.as_view()), name="Delete"),

    path('Cliente/Lista/', login_required(views.Client_List.as_view()), name="lista Cliente"),
    path('Cliente/add/', login_required(views.Client_Create.as_view()), name="Add"),
    path('Cliente/<int:pk>/edit/', login_required(views.Client_Update.as_view()), name="Update"),
    path('Cliente/<int:pk>/delete/', login_required(views.Client_Delete.as_view()), name="Delete"),

    path('Mascota/Lista/', login_required(views.Masc_List.as_view()), name="lista Mascota"),
    path('Mascota/add/', login_required(views.Masc_Create.as_view()), name="Add"),
    path('Mascota/<int:pk>/edit/', login_required(views.Masc_Update.as_view()), name="Update"),
    path('Mascota/<int:pk>/delete/', login_required(views.Masc_Delete.as_view()), name="Delete"),

    path('Atencion/Lista/', login_required(views.Atencion_List.as_view()), name="Atencion lista" ),
    path('Atencion/create/', login_required(views.Atencion_Create), name="empleado_create"),
    path('Atencion/edit/<int:pk>/', login_required(views.Atencion_Update), name="empleado_mofif"),
    path('Atencion/delete/<int:pk>/', login_required(views.Atencion_Delete), name="empleado_mofif"),
    path('Atencion/Calendar/', login_required(views.Atencion_Calendar.as_view()), name="empleado_mofif"),
    path('Atencion/detalle/<int:pk>/', login_required(views.Atencion_detalle), name="empleado_mofif"),


    path('Pedidos/Lista/' ,login_required(views.Pedidos_List.as_view()), name="Atencion lista" ),
    path('Pedidos/create/', login_required(views.Pedidos_Create), name="empleado_create"),
    path('Pedidos/edit/<int:pk>/', login_required(views.Pedidos_Update), name="empleado_mofif"),
    path('Pedidos/delete/<int:pk>/', login_required(views.Pedidos_Delete), name="empleado_mofif"),

    path('Pedidos/imp/<int:pk>/', login_required(views.imp_pedido), name="impress"),

    path('Ventas/Lista/', login_required(views.Ventas_List.as_view()), name="Atencion lista" ),
    path('Ventas/create/', login_required(views.Ventas_Create), name="empleado_create"),
    path('Ventas/edit/<int:pk>/', login_required(views.Ventas_Update), name="empleado_mofif"),
    path('Ventas/delete/<int:pk>/', login_required(views.ventas_Delete), name="empleado_mofif"),

    path('Subscription/Lista/', login_required(views.subs_list.as_view()), name="subs lista" ),
    path('Subscription/detail/<int:pk>/',login_required(views.subs_detail), name="detail"),
    # path('Subscription/modif/<int:pk>/', login_required(views.empleado_modif), name="empleado_mofif"),
    path('Subscription/delete/<int:pk>/', login_required(views.subs_delete.as_view()), name="empleado_mofif"),

    # Clientes Vistas
    path('Contact/', views.contact),
    path('Service/', views.service),

    path('Articulos/', views.articulos),
    path('Articulos/detalle/<int:pk>/', views.articulos_detalle),

]

