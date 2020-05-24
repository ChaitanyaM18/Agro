from django.urls import path,include
from . import views


urlpatterns = [
    path('govt/', views.govtDetails, name='govt' )
]
