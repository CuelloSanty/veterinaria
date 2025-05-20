from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmpleadoForm, AdelantoFormSet, AtencionForm, ArtAtencionFormSet, PedidoForm, DetallePedidoFormSet, VentaForm, VentaFormSet, FormSubscription
from .models import Empleado, Adelanto, Articulo, Proveedore, Cliente, Mascota, Atencione, ArticuloAtencion, Pedido, DetallePedido, Venta, DetalleVenta, Subscription
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.forms.models import model_to_dict
from django.urls import reverse_lazy
from datetime import datetime



########################################################
def function(db_formset_after, db_formset_before,DbToChanged, op_select=True):
    def GetData(cleaned_form):
        return {"id":cleaned_form.get('id'),"cantidad": cleaned_form.get('cantidad'),"art":cleaned_form.get('articulo')}
    def PushToDb(id, cantidad, operation, db_to_change, op_select):
    
        try:
            db = db_to_change.objects.get(pk=id)
            if not op_select:  # Si op_select es False, invertir operaciones
                if operation == 1: 
                    operation = 2
                else: operation = 1 
                print(operation)

            if operation == 1:
                db.cantidad += cantidad
                db.save()
            elif operation == 2:
                try: 
                    if cantidad <= db.cantidad: # Corregido la condición de comparación
                        db.cantidad -= cantidad
                        db.save()
                except: pass 
        except: pass

    def GetPreviousToCompare(db_formset_after,id_before, before):
        op = None
        cantidad = None
        if  id_before == None: 
            return PushToDb(before["art"].codigo, before["cantidad"], 2, DbToChanged, op_select)
        if not id_before == None:
            db_prev = db_formset_after.get(id=int(str(id_before)))
            after = {"id":db_prev.id,"cantidad":db_prev.cantidad,"art":db_prev.articulo}
        # Operations
            if after["cantidad"] < before["cantidad"]:
                cantidad = after["cantidad"] - before["cantidad"]
                op = 1
            if after["cantidad"] > before["cantidad"]:
                cantidad = before["cantidad"] - after["cantidad"]
                op = 2
            if before["cantidad"] == 0: 
                PushToDb(before["art"].codigo,after["cantidad"],1 , DbToChanged, op_select)
            PushToDb(before["art"].codigo, cantidad ,op,DbToChanged, op_select)

    deleted_forms = db_formset_before.deleted_forms
    if deleted_forms:
        for form in deleted_forms:
            data = GetData(form.cleaned_data)
            print(data)
            PushToDb(data['art'].codigo, data["cantidad"], 1, DbToChanged, op_select)
    if db_formset_before:
        for form in db_formset_before:
            if form.has_changed():   
                data = GetData(form.cleaned_data)
                GetPreviousToCompare(db_formset_after, data["id"], data)
    # ----------------------------- Index -----------------------------------

def splash_view(request):
    return render(request, "splash.html")


def index_public(request):
    if request.method == 'POST':
        form = FormSubscription(request.POST)
        if form.is_valid():
            form = form.save()
            print(form)
            return redirect("/")
    else:
        form = FormSubscription()
    return render(request,"index.html", {"form":form})

def LogOut(request):
    return render(request, 'registration/close-session.html') 

# ----------------------------------------------------------------------[End]



# General fuction for internal database currency
def SupRegToDb(request, pk, db):
    set_db = {"Empleado":Empleado, "Adelanto":Adelanto, "Articulo":Articulo, "Proveedore":Proveedore, "Cliente":Cliente, "Mascota":Mascota}

    set_url = {"Articulo":"/Articulos/Lista/", "Proveedore":"/Proveedor/Lista/", "Cliente":"/Cliente/Lista/", "Empleado":"/Empleado/Lista/", "Mascota":"/Mascota/Lista/"}

    set_template = {"Articulo":'admin/Articulos/delete.html', "Proveedore":'Admin/Proveedor/delete.html', "Cliente":'Admin/Cliente/delete.html',"Empleado":'Admin/Empleados/delete.html', "Mascota":'Admin/Mascota/delete.html'}

    if request.method == "POST":
        db_to_change = set_db[db].objects.get(pk=pk)
        db_to_change.delete_1 = True
        db_to_change.save()
        return redirect(set_url[db])
    else:
        return render(request,set_template[db])

# --------------------> Articulos
class Articulos_vista:
    model = Articulo
    fields = ('__all__')
    success_url = reverse_lazy('Articulos')

class Art_list(Articulos_vista,ListView):
    model = Articulo
    template_name = 'admin/Articulos/Lista.html'
    context_object_name = "Art"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        categoria = self.kwargs.get('categoria')

        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(descripcion__icontains=query) |
                Q(tipo__icontains=query) |
                Q(marca__icontains=query)
            )
        
        if categoria:
            queryset = queryset.filter(tipo=categoria)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['categoria'] = self.kwargs.get('categoria', '')
        return context
    
class Art_list_tarjeta(ListView):
    model = Articulo
    template_name = 'Clientes/articulos.html'
    context_object_name = "obj"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        categoria = self.kwargs.get('categoria')

        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(descripcion__icontains=query) |
                Q(tipo__icontains=query) |
                Q(marca__icontains=query)
            )
        
        if categoria:
            queryset = queryset.filter(tipo=categoria)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['categoria'] = self.kwargs.get('categoria', '')
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
    paginate_by = 10

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
    paginate_by = 10

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
    template_name = 'Admin/Proveedor/delete.html'
    success_url = '/Proveedor/Lista/'

# ------------------------- Proveedores ------------------------------[end]


# -------------------------   Cliente   ------------------------------
class cliente_mainclass:
    model = Cliente
    fields = ('__all__')
    success_url = reverse_lazy("/Cliente")

class Client_List(cliente_mainclass, ListView):
    template_name = "Admin/Cliente/lista.html"
    paginate_by = 10
    context_object_name = "Cliente"
    
    def get_queryset(self):
        queryset = super().get_queryset()
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
    template_name = 'Admin/Cliente/delete.html'
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
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
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
    paginate_by = 10
    context_object_name = "Atencion"
  

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(tipo__icontains=query) | Q(mascota__nombre__icontains=query))
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
            function([],formset, Articulo)
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
    ins_formset = ArticuloAtencion.objects.filter(pedido=ins.id)

    if request.method == "POST":
        form = AtencionForm(request.POST, instance=ins)
        formset = ArtAtencionFormSet(request.POST, instance=ins)
        if form.is_valid() and formset.is_valid():
            function(ins_formset, formset, Articulo)
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
    paginate_by = 10
    context_object_name = "Pedidos"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(tipo__icontains=query) | Q(proveedor__nombre__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Enviar el valor de la búsqueda al contexto
        return context

def Pedidos_Create(request):
    try:
        if request.method == "POST":
            form = PedidoForm(request.POST)
            formset = DetallePedidoFormSet(request.POST)
            if form.is_valid() and formset.is_valid():
                function([], formset, Articulo, op_select=False)
                form = form.save()
                formset.instance = form
                formset.save()
                return redirect('/Pedidos/Lista/')
        else:
            form = PedidoForm()
            formset = DetallePedidoFormSet()
            return render(request, 'Admin/Pedidos/form.html', {"form": form, "formset": formset})
    except Exception as e:
        # Manejo de errores
        print(f"Error: {e}")
        return render(request, 'Admin/Pedidos/error.html', {"error": str(e)})

def imp_pedido(request, pk):
    try:
        obj = Pedido.objects.get(pk=pk)
        product = DetallePedido.objects.filter(pedido=obj)
        total = 0
        p = []
        for x in product:
            total += (x.articulo.precio * x.cantidad)
            p.append({
                "id": x.id,
                "nombre": x.articulo,
                "precio": x.articulo.precio,
                "total": x.articulo.precio * x.cantidad,
                "descripcion": x.articulo.descripcion,
                "cantidad": x.cantidad
            })
        return render(request, "Admin/Pedidos/imp.html", {"obj": obj, "total": total, "p": p})
    except Exception as e:
        # Manejo de errores
        print(f"Error: {e}")
        return render(request, 'Admin/Pedidos/Lista.html', {"error": str(e)})


def Pedidos_Update(request, pk):
    ins = Pedido.objects.get(pk=pk)
    ins_formset = DetallePedido.objects.filter(pedido=ins.id)

    if request.method == "POST":
        form = PedidoForm(request.POST, instance=ins)
        formset = DetallePedidoFormSet(request.POST, instance=ins)
        if form.is_valid() and formset.is_valid():
            function(ins_formset,formset, Articulo, op_select=False)
            form = form.save()
            formset.instance = form
            formset.save()
            return redirect('/Pedidos/Lista/')
    else:
        form = PedidoForm(instance=ins)
        formset = DetallePedidoFormSet(instance=ins)
        return render(request, 'Admin/Pedidos/form.html',{"form":form, "formset":formset, "id":pk})

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
    paginate_by = 10
    context_object_name = "Ventas"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(cliente__nombre__icontains=query) | Q(empleado__nombre__icontains=query))
            print([queryset])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Enviar el valor de la búsqueda al contexto
        return context

    

def Ventas_Create(request):
    if request.method == "POST":
        form = VentaForm(request.POST)
        formset = VentaFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            function([],formset,Articulo)
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
            return redirect('/')
    return render(request, 'Admin/Ventas/delete.html')
# ---------------------------- Ventas --------------------------------------------[End]

# ---------------------------- subs ----- 
class subscription_mainclass:
    model = Subscription
    fields = ('__all__')
    exclude = ('id',)

class subs_list(subscription_mainclass, ListView):
    template_name = 'Admin/subscription/lista.html'
    paginate_by = 10
    context_object_name = "obj"
    success_url = '/Subscription/Lista/'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(Nombre__icontains=query) | Q(Gmail__icontains=query))
            print([queryset])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Enviar el valor de la búsqueda al contexto
        return context



class subs_delete(subscription_mainclass, DeleteView):
    template_name = "Admin/subscription/delete.html"
    success_url = "/Subscription/Lista/"
    
def subs_detail(request, pk):
    subs = Subscription.objects.get(pk=pk)
    return render(request, "Admin/subscription/detalle.html", {"obj": subs})
# ----subs[end]


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

def sitemap(request):
    return render(request, 'sitemap.html')