from django.urls import path,include
from . import views


urlpatterns = [
    path('statesDisplay/', views.statesDisplay.as_view(), name='statesDisplay'),
    path('statesDisplay/<int:id>', views.cropList.as_view(), name='cropList'),
    path('statesDisplay/<int:id>/<int:pk>', views.cropDisplay.as_view(), name='cropDisplay'),
]
