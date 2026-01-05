from django import forms
from .models import UserRegistrationModel


class UserRegistrationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'pattern': '[a-zA-Z]+'}), required=True, max_length=100)
    loginid = forms.CharField(widget=forms.TextInput(attrs={'pattern': '[a-zA-Z]+'}), required=True, max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'pattern': '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}',
                                                                 'title': 'Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters'}),
                               required=True, max_length=100)
    mobile = forms.CharField(widget=forms.TextInput(attrs={'pattern': '[56789][0-9]{9}'}), required=True,
                             max_length=100)
    email = forms.CharField(widget=forms.TextInput(attrs={'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'}),
                            required=True, max_length=100)
    locality = forms.CharField(widget=forms.TextInput(), required=True, max_length=100)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 22}), required=True, max_length=250)
    city = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'pattern': '[A-Za-z ]+', 'title': 'Enter Characters Only '}), required=True,
        max_length=100)
    state = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'pattern': '[A-Za-z ]+', 'title': 'Enter Characters Only '}), required=True,
        max_length=100)
    status = forms.CharField(widget=forms.HiddenInput(), initial='waiting', max_length=100)

    class Meta():
        model = UserRegistrationModel
        fields = '__all__'


class ShipConfigForm(forms.Form):
    max_simulation_time = forms.FloatField(label="Simulation duration (hours)", initial=24, min_value=1)
    time_step = forms.FloatField(label="Time step (minutes)", initial=5, min_value=0.1)
    ship_type = forms.CharField(label="Ship type", initial="Cargo Vessel")
    max_speed = forms.FloatField(label="Maximum speed (knots)", initial=20.0)
    fuel_capacity = forms.FloatField(label="Initial fuel level (%)", initial=100.0, min_value=0, max_value=100)
    battery_capacity = forms.FloatField(label="Battery capacity (kWh)", initial=100.0)
    solar_panel_capacity = forms.FloatField(label="Solar panel capacity (kW)", initial=50.0)
    wind_turbine_capacity = forms.FloatField(label="Wind turbine capacity (kW)", initial=30.0)
    initial_battery_level = forms.FloatField(label="Initial battery level (%)", initial=80.0, min_value=0,
                                             max_value=100)
    communication_range = forms.FloatField(label="Communication range (nautical miles)", initial=50.0)
    initial_satellite_signal = forms.FloatField(label="Initial satellite signal (%)", initial=85.0, min_value=0,
                                                max_value=100)
    initial_cellular_signal = forms.FloatField(label="Initial cellular signal (%)", initial=70.0, min_value=0,
                                               max_value=100)
    weather_condition = forms.ChoiceField(choices=[('sunny', 'Sunny'), ('cloudy', 'Cloudy'), ('stormy', 'Stormy')],
                                          initial='sunny')
    wind_speed = forms.FloatField(label="Average wind speed (m/s)", initial=10.0)
    sea_condition = forms.ChoiceField(choices=[('calm', 'Calm'), ('moderate', 'Moderate'), ('rough', 'Rough')],
                                      initial='calm')



from django import forms

SECURITY_DOMAINS = [
    ('malware', 'Malware'),
    ('phishing', 'Phishing'),
    ('ddos', 'DDoS'),
    ('ransomware', 'Ransomware'),
    ('apt', 'APT'),
    ('insider_threat', 'Insider Threat'),
    ('zero_day', 'Zero Day'),
    ('supply_chain', 'Supply Chain'),
]

class OrgInputForm(forms.Form):
    name = forms.CharField(
        label='Organization Name',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-300 rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter organization name'
        })
    )

    infrastructure_profile = forms.CharField(
        label='Technologies (comma-separated)',
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-300 rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'e.g. web,cloud,mobile'
        })
    )

    security_domains = forms.MultipleChoiceField(
        choices=SECURITY_DOMAINS,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'space-y-2'
        }),
        label="Security Domains"
    )

    threat_data_quality = forms.FloatField(
        min_value=0,
        max_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'border border-gray-300 rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )

    sharing_willingness = forms.FloatField(
        min_value=0,
        max_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'border border-gray-300 rounded-md p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )


class EvidenceForm(forms.Form):
    evidence_id = forms.CharField(label="Evidence ID", max_length=100)
    evidence_type = forms.CharField(label="Evidence Type", max_length=100)
    description = forms.CharField(label="Description", widget=forms.Textarea)
    source = forms.CharField(label="Source", max_length=100)