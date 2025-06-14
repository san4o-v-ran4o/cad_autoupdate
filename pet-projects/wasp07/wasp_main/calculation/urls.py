from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('calculation/', views.calculator, name='calculation'),
    path('calculation/hs-diagram/', views.hs_diagram, name='hs_diagram'),
    path('calculation/saturation-line/', views.saturation_line, name='saturation_line'),
]
