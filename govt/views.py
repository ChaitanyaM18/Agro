from django.shortcuts import render
from .models import GovtDetails
# Create your views here.

def govtDetails(request):
    model = GovtDetails.objects.all()
    return render(request,'govt/govtDetails.html',{'model': model})
