from django.urls import path,include
from . import views


urlpatterns = [
    path('statesDisplay/', views.statesDisplay, name='statesDisplay'),
    path('cropList/', views.cropList, name='cropList'),
    path('cropDisplay/<int:pk>', views.cropDisplay, name='cropDisplay'),
]
