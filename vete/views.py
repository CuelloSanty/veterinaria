from django.shortcuts import render, redirect
from .forms import EmpleadoForm, AdelantoFormSet
from .models import Empleado, Adelanto, Articulo
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy


def index(request):
    return render(request,'index.html')


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
        adelanto_formset = AdelantoFormSet(request.POST, queryset=Adelanto.objects.none())
        
        if empleado_form.is_valid() and adelanto_formset.is_valid():
            empleado = empleado_form.save()
            adelantos = adelanto_formset.save(commit=False)
            for adelanto in adelantos:
                adelanto.empleado = empleado
                adelanto.save()
            return redirect('')
        else:
            return redirect('')  # Cambia 'success_url' por la URL a la que quieras redirigir
    else:
        empleado_form = EmpleadoForm()
        adelanto_formset = AdelantoFormSet(queryset=Adelanto.objects.none())
    
    return render(request, 'Admin/Empleados/empleado_form.html', {
        'empleado_form': empleado_form,
        'adelanto_formset': adelanto_formset,
    })

def empleado_modif(request, pk):
    ins = Empleado.objects.get(pk=pk)
    if request.method == 'POST':
        empleado_form = EmpleadoForm(request.POST, instance=ins)
        adelanto_formset = AdelantoFormSet(request.POST)
        if empleado_form.is_valid() and adelanto_formset.is_valid():
            empleado = empleado_form.save()
            adelantos = adelanto_formset.save(commit=False)
            for adelanto in adelantos:
                adelanto.empleado = empleado
                adelanto.save()
            return redirect('/')
        return redirect('/')

    else:
        empleado_form = EmpleadoForm(instance=ins)
        adelanto_formset = AdelantoFormSet()
        return render(request, 'Admin/Empleados/empleado_form.html',{
            'empleado_form': empleado_form,
            'adelanto_formset': adelanto_formset,
    })
def empleado_delete(request, pk):
    emp = Empleado.objects.get(pk=pk)
    if request.method == 'POST':
        emp.delete()
        return redirect('/emp/')
    return render(request, 'Admin/Empleados/delete.html', {'emp': emp})
# -------------------------> Emplados <-------------------------------



