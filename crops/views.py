from django.shortcuts import render,get_object_or_404
from .models import States,StateCrops
from django.views import generic


class statesDisplay(generic.ListView):
    template_name = 'crops/states.html'
    model = States
    context_object_name = 'states'


class cropList(generic.TemplateView):
    template_name = 'crops/listCrops.html'
    model = StateCrops

    def get_context_data(self, *args, **kwargs):
        context = super(cropList,
                        self).get_context_data(*args, **kwargs)
        obj = self.kwargs['id']
        context['crops'] = StateCrops.objects.filter(state__id=obj)
        return context


class cropDisplay(generic.TemplateView):
    template_name = 'crops/crops.html'
    model = StateCrops

    def get_context_data(self, *args, **kwargs):
        context = super(cropDisplay,
                        self).get_context_data(*args, **kwargs)
        obj = self.kwargs['id']
        obj1 = self.kwargs['pk']
        context['crops'] = StateCrops.objects.filter(state__id=obj, id=obj1)
        return context
