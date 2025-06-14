from django.shortcuts import render
from .forms import HSDiagramForm, SaturationLineForm
from iapws import IAPWS97


def safe_round(value, digits):
    return round(value, digits) if value is not None else 'N/A'


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def calculator(request):
    return render(request, 'calculation/calculator.html')


def hs_diagram(request):
    form = HSDiagramForm(request.POST or None)
    results = None

    if request.method == 'POST' and form.is_valid():
        pressure = form.cleaned_data['pressure']
        enthalpy = form.cleaned_data['enthalpy']
        water = IAPWS97(P=pressure, h=enthalpy)

        results = {
            'pressure': safe_round(water.P, 4),
            'enthalpy': safe_round(water.h, 4),
            'temperature': safe_round(water.T - 273.15 if water.T is not None else None, 4),
            'entropy': safe_round(water.s, 4),
            'specific_volume': safe_round(water.v, 6),
            'density': safe_round(water.rho, 4),
            'quality': safe_round(water.x, 4),
            'dynamic_viscosity': safe_round(water.mu, 8),
            'kinematic_viscosity': safe_round(water.nu, 8),
        }

    return render(request, 'calculation/hs_diagram.html', {
        'form': form,
        'results': results
    })


def saturation_line(request):
    form = SaturationLineForm(request.POST or None)
    results_water = None
    results_steam = None

    if request.method == 'POST' and form.is_valid():
        input_type = form.cleaned_data['input_type']
        value = form.cleaned_data['value']

        if input_type == 'pressure':
            water = IAPWS97(P=value, x=0)
            steam = IAPWS97(P=value, x=1)
        else:
            value_k = value + 273.15
            water = IAPWS97(T=value_k, x=0)
            steam = IAPWS97(T=value_k, x=1)

        results_water = {
            'pressure': safe_round(water.P, 4),
            'temperature': safe_round(water.T - 273.15 if water.T is not None else None, 4),
            'enthalpy': safe_round(water.h, 4),
            'entropy': safe_round(water.s, 4),
            'specific_volume': safe_round(water.v, 6),
            'density': safe_round(water.rho, 4),
            'dynamic_viscosity': safe_round(water.mu, 8),
            'kinematic_viscosity': safe_round(water.nu, 8),
        }

        results_steam = {
            'pressure': safe_round(steam.P, 4),
            'temperature': safe_round(steam.T - 273.15 if steam.T is not None else None, 4),
            'enthalpy': safe_round(steam.h, 4),
            'entropy': safe_round(steam.s, 4),
            'specific_volume': safe_round(steam.v, 6),
            'density': safe_round(steam.rho, 4),
            'dynamic_viscosity': safe_round(steam.mu, 8),
            'kinematic_viscosity': safe_round(steam.nu, 8),
        }

    return render(request, 'calculation/saturation_line.html', {
        'form': form,
        'results_water': results_water,
        'results_steam': results_steam
    })
