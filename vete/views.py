from django.shortcuts import render, redirect
from .forms import EmpleadoForm, AdelantoFormSet, AtencionForm, ArtAtencionFormSet, PedidoForm, DetallePedidoFormSet, VentaForm, VentaFormSet
from .models import Empleado, Adelanto, Articulo, Proveedore, Cliente, Mascota, Atencione, ArticuloAtencion, Pedido, DetallePedido, Venta
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy


# ----------------------------- Index -----------------------------------
def index_public(request):
    return render(request,"index.html")

def index_private(request): 
    return render(request, 'Admin/index_admin.html')
# ----------------------------------------------------------------------[End]

# --------------------> Articulos
class Articulos_vista:
    model = Articulo
    fields = ('__all__')
    success_url = reverse_lazy('Articulos')

class Art_list(Articulos_vista, ListView):
    template_name = 'admin/Articulos/Lista.html'
    context_object_name = "Art"
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(nombre__icontains=query) | Q(descripcion__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Enviar el valor de la búsqueda al contexto
        return context

class Art_Create(Articulos_vista, CreateView):
    template_name = 'admin/Articulos/form.html'

class Art_Update(Articulos_vista, UpdateView):
    template_name = 'admin/Articulos/form.html'

class Art_Delete(Articulos_vista, DeleteView):
    template_name = 'admin/Articulos/delete.html'
# ---------------------> Articulos [End]



# --------------------> Empleados <----------------------------
class EmpViews(ListView):
    model = Empleado
    template_name = "admin/Empleados/empleado.html"
    context_object_name = "emp"
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(nombre__icontains=query) | Q(TurnoChoice__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Enviar el valor de la búsqueda al contexto
        return context


    
def empleado_create(request):
    if request.method == 'POST':
        empleado_form = EmpleadoForm(request.POST)
        adelanto_formset = AdelantoFormSet(request.POST)
        
        if empleado_form.is_valid() and adelanto_formset.is_valid():
            emp = empleado_form.save()
            adelanto_formset.instance = emp
            adelanto_formset.save()
          
            return redirect('/Empleado/Lista/')
        else:
            return redirect('/index-admin/')  # Cambia 'success_url' por la URL a la que quieras redirigir
    else:
        empleado_form = EmpleadoForm()
        adelanto_formset = AdelantoFormSet()
    
    return render(request, 'Admin/Empleados/empleado_form.html', {
        'empleado_form': empleado_form,
        'adelanto_formset': adelanto_formset,
    })

def empleado_modif(request, pk):
    ins = Empleado.objects.get(pk=pk)
    if request.method == 'POST':
        empleado_form = EmpleadoForm(request.POST, instance=ins)
        adelanto_formset = AdelantoFormSet(request.POST, instance=ins)
        if empleado_form.is_valid() and adelanto_formset.is_valid():
            empleado = empleado_form.save()
            adelanto_formset.instance = empleado
            adelanto_formset.save()
            return redirect('/Empleado/Lista/')
        return redirect('/index-admin/')

    else:
        empleado_form = EmpleadoForm(instance=ins)
        adelanto_formset = AdelantoFormSet(instance=ins)
        return render(request, 'Admin/Empleados/empleado_form.html',{
            'empleado_form': empleado_form,
            'adelanto_formset': adelanto_formset,"var":"edit"
    })
def empleado_delete(request, pk):
    emp = Empleado.objects.get(pk=pk)
    if request.method == 'POST':
        emp.delete()
        return redirect('/Empleado/Lista/')
    return render(request, 'Admin/Empleados/delete.html', {'emp': emp})
# -------------------------> Emplados <-------------------------------


# ------------------------- Proveedores ------------------------------
class proveedor_mainclass:
    model = Proveedore
    fields = ('__all__')
    success_url = reverse_lazy('/Proveedor')

class Prov_List(proveedor_mainclass, ListView):
    template_name = "Admin/Proveedor/lista.html"
    context_object_name = "proveedores"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(nombre__icontains=query) | Q(cuit__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Enviar el valor de la búsqueda al contexto
        return context

class Prov_Create(proveedor_mainclass, CreateView):
    template_name = "Admin/Proveedor/form.html"
    success_url = '/Proveedor/Lista/'

class Prov_Update(proveedor_mainclass, UpdateView):
    template_name = "Admin/Proveedor/form.html"
    success_url = '/Proveedor/Lista/'

class Prov_Delete(proveedor_mainclass, DeleteView):
    template_name = "Admin/Proveedor/delete.html"
    success_url = '/Proveedor/Lista/'

# ------------------------- Proveedores ------------------------------[end]


# -------------------------   Cliente   ------------------------------
class cliente_mainclass:
    model = Cliente
    fields = ('__all__')
    exclude = ('id',)
    success_url = reverse_lazy("/Cliente")

class Client_List(cliente_mainclass, ListView):
    template_name = "Admin/Cliente/lista.html"
    context_object_name = "Cliente"

class Client_Create(cliente_mainclass, CreateView):
    template_name = "Admin/Cliente/form.html"
    success_url = "/Cliente/Lista/"

class Client_Update(cliente_mainclass, UpdateView):
    template_name = "Admin/Cliente/form.html"

class Client_Delete(cliente_mainclass, DeleteView):
    template_name = "Admin/Cliente/lista.html"
# -------------------------   Cliente   ------------------------------[End]




# ------------------------   Mascota ----------------------------------
class mascota_mainclass:
    model = Mascota
    fields = ('__all__')
    exclude = ('id',)
    success_url = reverse_lazy('/Mascota/Lista')

class Masc_List(mascota_mainclass, ListView):
    template_name = "Admin/Mascota/lista.html"
    context_object_name = "Mascota"

class Masc_Create(mascota_mainclass, CreateView):
    template_name = "Admin/Mascota/form.html"

class Masc_Update(mascota_mainclass, UpdateView):
    template_name = "Admin/Mascota/form.html"

class Masc_Delete(mascota_mainclass, DeleteView):
    template_name = "Admin/Mascota/delete.html"
# ------------------------------- Mascota --------------------------------------[End]



# ---------------------------- Atencion ----------------------------------------
class Atencion_List(ListView):
    model = Atencione
    template_name = "Admin/Atencion/lista.html"
    paginate_by = 3
    context_object_name = "Atencion"

def Atencion_Create(request):
    if request.method == "POST":
        form = AtencionForm(request.POST)
        formset = ArtAtencionFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            form = form.save()
            formset.instance = form
            formset.save()
    else:
        form = AtencionForm()
        formset = ArtAtencionFormSet()
        return render(request, 'Admin/Atencion/form.html',{"form":form, "formset":formset})

def Atencion_Update(request, pk):
    ins = Atencione.objects.get(pk=pk)
    if request.method == "POST":
        form = AtencionForm(request.POST, instance=ins)
        formset = ArtAtencionFormSet(request.POST, instance=ins)
        if form.is_valid() and formset.is_valid():
            form = form.save()
            formset.instance = form
            formset.save()
            return redirect('/Atencion/Lista/')
    else:
        form = AtencionForm(instance=ins)
        formset = ArtAtencionFormSet(instance=ins)
        return render(request, 'Admin/Atencion/form.html',{"form":form, "formset":formset})
def Atencion_Delete(request, pk):
    obj = Atencione.objects.get(pk=pk)
    if request.method == "POST":
        try:
            obj.delete()
            return redirect('/Atenciones/Lista')
        except:
            print("Ta mal wacho")
    return render(request, 'Admin/Atencion/delete.html')
# ---------------------------- Atencion ----------------------------------------[End]

# ---------------------------- Pedidos -------------------------------------------
class Pedidos_List(ListView):
    model = Pedido
    template_name = "Admin/Pedidos/lista.html"
    paginate_by = 3
    context_object_name = "Pedidos"

def Pedidos_Create(request):
    if request.method == "POST":
        form = PedidoForm(request.POST)
        formset = DetallePedidoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            form = form.save()
            formset.instance = form
            formset.save()
            return redirect('/Pedidos/Lista/')
    else:
        form = PedidoForm()
        formset = DetallePedidoFormSet()
        return render(request, 'Admin/Pedidos/form.html',{"form":form, "formset":formset})

def Pedidos_Update(request, pk):
    ins = Pedido.objects.get(pk=pk)
    if request.method == "POST":
        form = PedidoForm(request.POST, instance=ins)
        formset = DetallePedidoFormSet(request.POST, instance=ins)
        if form.is_valid() and formset.is_valid():
            form = form.save()
            formset.instance = form
            formset.save()
            return redirect('/Pedidos/Lista/')
    else:
        form = PedidoForm(instance=ins)
        formset = DetallePedidoFormSet(instance=ins)
        return render(request, 'Admin/Pedidos/form.html',{"form":form, "formset":formset})

def Pedidos_Delete(request, pk):
    obj = Pedido.objects.get(pk=pk)
    if request.method == "POST":
        try:
            obj.delete()
            return redirect('/Atenciones/Lista')
        except:
            print("Ta mal wacho")
    return render(request, 'Admin/Pedidos/delete.html')
# ---------------------------- Pedidos -------------------------------------------[End]

# ---------------------------- Ventas --------------------------------------------
class Ventas_List(ListView):
    model = Venta
    template_name = "Admin/Ventas/lista.html"
    paginate_by = 3
    context_object_name = "Ventas"

def Ventas_Create(request):
    if request.method == "POST":
        form = VentaForm(request.POST)
        formset = VentaFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            form = form.save()
            formset.instance = form
            formset.save()
        return redirect('/Ventas/Lista/')
    else:
        form = VentaForm()
        formset = VentaFormSet()
        return render(request, 'Admin/Ventas/form.html',{"form":form, "formset":formset})

def Ventas_Update(request, pk):
    ins = Venta.objects.get(pk=pk)
    if request.method == "POST":
        form = VentaForm(request.POST, instance=ins)
        formset = VentaFormSet(request.POST, instance=ins)
        if form.is_valid() and formset.is_valid():
            form = form.save()
            formset.instance = form
            formset.save()
            return redirect('/Ventas/Lista/')
    else:
        form = VentaForm(instance=ins)
        formset = VentaFormSet(instance=ins)
        return render(request, 'Admin/Ventas/form.html',{"form":form, "formset":formset})

def ventas_Delete(request, pk):
    obj = Venta.objects.get(pk=pk)
    if request.method == "POST":
        try:
            obj.delete()
            return redirect('/Ventas/Lista/')
        except:
            print("Ta mal wacho")
    return render(request, 'Admin/Ventas/delete.html')
# ---------------------------- Ventas --------------------------------------------[End]