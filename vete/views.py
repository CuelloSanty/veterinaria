from django.shortcuts import render, redirect
from .forms import EmpleadoForm, AdelantoFormSet
from .models import Empleado, Adelanto
def index(request):

    return render(request, 'index.html', {"emp":Empleado.objects.all()})



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
            return redirect('/emp')  # Cambia 'success_url' por la URL a la que quieras redirigir
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
            return redirect('/emp')

    else:
        empleado_form = EmpleadoForm(instance=ins)
        adelanto_formset = AdelantoFormSet()
        return render(request, 'empleado_form.html',{
            'empleado_form': empleado_form,
            'adelanto_formset': adelanto_formset,
    })
