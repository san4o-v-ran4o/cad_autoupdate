from django import forms


class HSDiagramForm(forms.Form):
    pressure = forms.FloatField(label='Pressure (MPa)', min_value=0)
    enthalpy = forms.FloatField(label='Enthalpy (kJ/kg)', min_value=0)


class SaturationLineForm(forms.Form):
    INPUT_CHOICES = [
        ('pressure', 'Pressure (MPa)'),
        ('temperature', 'Temperature (°C)'),
    ]
    input_type = forms.ChoiceField(choices=INPUT_CHOICES, label='Input Type')
    value = forms.FloatField(label='Value', min_value=0)
