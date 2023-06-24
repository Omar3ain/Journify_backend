from django.shortcuts import render, redirect
from .models import Country
# Create your views here.

def country_list(request):
    countries = Country.objects.all()
    return render(request, 'country_list.html', {'countries': countries})

def country_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        code = request.POST['code']
        country = Country(name=name, code=code)
        country.save()
        return redirect('country_list')
    return render(request, 'country_create.html')

def country_update(request, pk):
    country = Country.objects.get(pk=pk)
    if request.method == 'POST':
        country.name = request.POST['name']
        country.code = request.POST['code']
        country.save()
        return redirect('country_list')
    return render(request, 'country_update.html', {'country': country})

def country_delete(request, pk):
    country = Country.objects.get(pk=pk)
    if request.method == 'POST':
        country.delete()
        return redirect('country_list')
    return render(request, 'country_delete.html', {'country': country})
