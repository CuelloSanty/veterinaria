from django.shortcuts import render, redirect
from .forms import EmpleadoForm, AdelantoFormSet
from .models import Empleado, Adelanto, Articulo
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

class ArtViews(ListView):
    model = Articulo
    template_name = "ArtList.html"
    context_object_name = "Art"
    paginate_by = 20





class EmpViews(ListView):
    model = Empleado
    template_name = "index.html"
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
    
    return render(request, 'empleado_form.html', {
        'empleado_form': empleado_form,
        'adelanto_formset': adelanto_formset,
    })

def modif(request, pk):
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
        return render(request, 'empleado_form.html',{
            'empleado_form': empleado_form,
            'adelanto_formset': adelanto_formset,
    })
