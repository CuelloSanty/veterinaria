from django.shortcuts import render, redirect
from .forms import EmpleadoForm, AdelantoFormSet, AtencionForm, ArtAtencionFormSet, PedidoForm, DetallePedidoFormSet, VentaForm, VentaFormSet
from .models import Empleado, Adelanto, Articulo, Proveedore, Cliente, Mascota, Atencione, ArticuloAtencion, Pedido, DetallePedido, Venta, DetalleVenta
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.forms.models import model_to_dict
from django.urls import reverse_lazy
from datetime import datetime

def function(db_formset_after, db_formset_before,DbToChanged):
    
    def GetData(cleaned_form):
        return {"id":cleaned_form.get('id'),"cantidad": cleaned_form.get('cantidad'),"art":cleaned_form.get('articulo')}
    def PushToDb(id, cantidad, operation, db_to_change):
        db = db_to_change.objects.get(pk=id)
        if operation == 1:
            db.cantidad += cantidad
            db.save()

        if operation == 2:
            if not cantidad > db.cantidad:
                db.cantidad -= cantidad
                db.save()
            else: return None
        else: pass
    def GetPreviousToCompare(db,key_prev, db_formset_after, param=None):
        op = None
        db_prev = db.get(id=key_prev)
        after = {"id":db_prev.id,"cantidad":db_prev.cantidad,"art":db_prev.articulo}
        
        # Operations
        if after["cantidad"] < param["cantidad"]:op = 2
        if after["cantidad"] > param["cantidad"]:op = 1
        if after["cantidad"] == param["cantidad"]:op = 0
        if after["art"] != param["art"]: PushToDb(after['art'].codigo, after['cantidad'], 1, DbToChanged)

        PushToDb(param["art"].codigo, param["cantidad"],op,DbToChanged)

    deleted_forms = db_formset_before.deleted_forms
    if deleted_forms:
        for form in deleted_forms:
            cleaned_form = form.cleaned_data
            data = GetData(cleaned_form)
            PushToDb(data['art'].codigo, data["cantidad"], 1, DbToChanged)
    if db_formset_before:
        for form in db_formset_before:
            if form.has_changed(): 
                cleaned_form = form.cleaned_data
                data = GetData(cleaned_form)
                if not form in db_formset_after: PushToDb(data['art'].codigo, data["cantidad"],1, DbToChanged)
                if not data["id"] == None: GetPreviousToCompare(db_formset_after,int(str(data["id"])),db_formset_after,data)





# ----------------------------- Index -----------------------------------
def index_public(request):
    return render(request,"index.html")

def LogOut(request):
    return render(request, 'registration/close-session.html') 

# ----------------------------------------------------------------------[End]

# --------------------> Articulos
class Articulos_vista:
    model = Articulo
    fields = ('__all__')
    success_url = reverse_lazy('Articulos')

class Art_list(Articulos_vista, ListView):
    template_name = 'admin/Articulos/Lista.html'
    context_object_name = "Art"
    paginate_by = 10

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
    success_url = '/Articulos/Lista/'

class Art_Update(Articulos_vista, UpdateView):
    template_name = 'admin/Articulos/form.html'
    success_url = '/Articulos/Lista/'
    

class Art_Delete(Articulos_vista, DeleteView):
    template_name = 'admin/Articulos/delete.html'
    success_url = '/Articulos/Lista/'
    
# ---------------------> Articulos [End]



# --------------------> Empleados <----------------------------
class EmpViews(ListView):
    model = Empleado
    template_name = "admin/Empleados/empleado.html"
    context_object_name = "emp"
    paginate_by = 1

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
    paginate_by = 1
    context_object_name = "Cliente"
    
    def get_queryset(self):
        queryset = Cliente.objects.all().order_by('id')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(nombre__icontains=query) | Q(telefono__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Enviar el valor de la búsqueda al contexto
        return context

class Client_Create(cliente_mainclass, CreateView):
    template_name = "Admin/Cliente/form.html"
    success_url = "/Cliente/Lista/"

class Client_Update(cliente_mainclass, UpdateView):
    template_name = "Admin/Cliente/form.html"
    success_url = "/Cliente/Lista/"


class Client_Delete(cliente_mainclass, DeleteView):
    template_name = "Admin/Cliente/lista.html"
    success_url = "/Cliente/Lista/"

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
    paginate_by = 7

    def get_queryset(self):
        queryset = Mascota.objects.all().order_by('id')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(nombre__icontains=query) | Q(raza__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Enviar el valor de la búsqueda al contexto
        return context

class Masc_Create(mascota_mainclass, CreateView):
    template_name = "Admin/Mascota/form.html"
    success_url = "/Mascota/Lista/"

class Masc_Update(mascota_mainclass, UpdateView):
    template_name = "Admin/Mascota/form.html"
    success_url = "/Mascota/Lista/"


class Masc_Delete(mascota_mainclass, DeleteView):
    template_name = "Admin/Mascota/delete.html"
    success_url = "/Mascota/Lista/"

# ------------------------------- Mascota --------------------------------------[End]



# ---------------------------- Atencion ----------------------------------------
class Atencion_List(ListView):
    model = Atencione
    template_name = "Admin/Atencion/lista.html"
    paginate_by = 1
    context_object_name = "Atencion"
    # def get_queryset(self): 
        # Ordena el queryset por el campo 'id' 
        # return Atencione.objects.all().order_by('id')



    def get_queryset(self):
        queryset = Atencione.objects.all().order_by('id')

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(nombre__icontains=query) | Q(raza__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Enviar el valor de la búsqueda al contexto
        return context



def Atencion_Create(request):
    if request.method == "POST":
        form = AtencionForm(request.POST)
        formset = ArtAtencionFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            form = form.save()
            formset.instance = form
            formset.save()
        return redirect('/Atencion/Lista/')
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
            return redirect('/Atencion/Lista')
        except:
            print("Ta mal wacho")
    return render(request, 'Admin/Atencion/delete.html')

class Atencion_Calendar(ListView):
    extra_context = {"filter_data":Atencione.objects.filter(dia=(datetime.now().date()))}
    model = Atencione
    template_name = "Admin\Atencion\calendar.html"
    context_object_name = "obj"

def Atencion_detalle(request, pk):
    get_atention = Atencione.objects.get(id=pk)
    context = {'atencion': get_atention}
    return render(request, 'Admin\Atencion\detalle.html',context)
# ---------------------------- Atencion ----------------------------------------[End]

# ---------------------------- Pedidos -------------------------------------------
class Pedidos_List(ListView):
    model = Pedido
    template_name = "Admin/Pedidos/lista.html"
    paginate_by = 3
    context_object_name = "Pedidos"

    def get_queryset(self): 
        # Ordena el queryset por el campo 'id' 
        return Venta.objects.all().order_by('id')


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
            return redirect('/Pedidos/Lista')
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

    def get_queryset(self): 
        # Ordena el queryset por el campo 'id' 
        return Venta.objects.all().order_by('id')

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
    ins_formset = DetalleVenta.objects.filter(venta=ins.id)
   

    if request.method == "POST":
        form = VentaForm(request.POST, instance=ins)
        formset = VentaFormSet(request.POST, instance=ins)
        
        if form.is_valid() and formset.is_valid():
    
            function(ins_formset,formset,Articulo)
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


# --------------------------- Clientes Vistas ------------------------------------
def contact(request):
    return render(request, 'Clientes/contact.html')

def service(request):
    return render(request, 'Clientes/service.html')

def articulos(request):
    art = Articulo.objects.all()
    context = {'obj': art}
    return render(request, 'Clientes/articulos.html',context)

def articulos_detalle(request,pk):
    art_selected = Articulo.objects.get(pk=pk)
    context = {"obj": art_selected}
    print(art_selected.codigo)
    return render(request, 'Clientes/aticulodetalle.html', context)

# W