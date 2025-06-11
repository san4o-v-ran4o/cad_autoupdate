from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('calculator/', views.calculator, name='calculator'),
    path('calculator/hs-diagram/', views.hs_diagram, name='hs_diagram'),
    path('calculator/saturation-line/', views.saturation_line, name='saturation_line'),
]