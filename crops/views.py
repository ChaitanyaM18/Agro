from django.shortcuts import render,get_object_or_404
from .models import States,StateCrops

def statesDisplay(request):
    states = States.objects.all()
    crops = StateCrops.objects.all()
    context = {
        'states' : states,
        'crops' : crops,
    }
    return render(request,'crops/states.html',context)

def cropList(request):
    crops = StateCrops.objects.all()
    context = {
        'crops' : crops,
    }
    return render(request,'crops/listCrops.html',context)

def cropDisplay(request, pk):
    crops = StateCrops.objects.filter(state__id = pk)
    context = {
        'crops' : crops,
    }
    return render(request,'crops/crops.html',context)
