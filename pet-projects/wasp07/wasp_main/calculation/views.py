from django.shortcuts import render
from iapws import IAPWS97

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def calculator(request):
    return render(request, 'calculator/calculator.html')  # Новая view

def hs_diagram(request):
    results = None
    if request.method == 'POST':
        pressure = float(request.POST.get('pressure'))
        enthalpy = float(request.POST.get('enthalpy'))
        water = IAPWS97(P=pressure, h=enthalpy)
        results = {
            'pressure': round(water.P, 4),
            'enthalpy': round(water.h, 4),
            'temperature': round(water.T - 273.15, 4),
            'entropy': round(water.s, 4),
            'specific_volume': round(water.v, 6),
            'density': round(water.rho, 4),
            'quality': round(water.x, 4) if water.x is not None else 'N/A',
            'dynamic_viscosity': round(water.mu, 8),
            'kinematic_viscosity': round(water.nu, 8),
        }
    return render(request, 'calculator/hs_diagram.html', {'results': results})

def saturation_line(request):
    results_water = None
    results_steam = None
    if request.method == 'POST':
        input_type = request.POST.get('input_type')
        value = float(request.POST.get('value'))
        if input_type == 'pressure':
            water = IAPWS97(P=value, x=0)  # Liquid phase
            steam = IAPWS97(P=value, x=1)  # Vapor phase
            results_water = {
                'pressure': round(water.P, 4),
                'temperature': round(water.T - 273.15, 4),
                'enthalpy': round(water.h, 4),
                'entropy': round(water.s, 4),
                'specific_volume': round(water.v, 6),
                'density': round(water.rho, 4),
                'dynamic_viscosity': round(water.mu, 8),
                'kinematic_viscosity': round(water.nu, 8),
            }
            results_steam = {
                'pressure': round(steam.P, 4),
                'temperature': round(steam.T - 273.15, 4),
                'enthalpy': round(steam.h, 4),
                'entropy': round(steam.s, 4),
                'specific_volume': round(steam.v, 6),
                'density': round(steam.rho, 4),
                'dynamic_viscosity': round(steam.mu, 8),
                'kinematic_viscosity': round(steam.nu, 8),
            }
        else:  # Temperature
            value_k = value + 273.15  # Convert to Kelvin
            water = IAPWS97(T=value_k, x=0)
            steam = IAPWS97(T=value_k, x=1)
            results_water = {
                'pressure': round(water.P, 4),
                'temperature': round(water.T - 273.15, 4),
                'enthalpy': round(water.h, 4),
                'entropy': round(water.s, 4),
                'specific_volume': round(water.v, 6),
                'density': round(water.rho, 4),
                'dynamic_viscosity': round(water.mu, 8),
                'kinematic_viscosity': round(water.nu, 8),
            }
            results_steam = {
                'pressure': round(steam.P, 4),
                'temperature': round(steam.T - 273.15, 4),
                'enthalpy': round(steam.h, 4),
                'entropy': round(steam.s, 4),
                'specific_volume': round(steam.v, 6),
                'density': round(steam.rho, 4),
                'dynamic_viscosity': round(steam.mu, 8),
                'kinematic_viscosity': round(steam.nu, 8),
            }
    return render(request, 'calculator/saturation_line.html', {
        'results_water': results_water,
        'it': results_steam
    })
