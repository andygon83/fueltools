from django import forms
from .models import FuelPrice, Airport, Customer, CustomerAirport

# FuelPrice forms
class FuelPriceForm(forms.Form):
    fuel_price_csv = forms.FileField(label='Select a file')

class SingleFuelUpdate(forms.ModelForm):
    class Meta:
        model = FuelPrice
        fields = ['airport', 'date', 'supplier', 'price', 'fee', 'note', 'other_variable']

# Airport forms
class AirportForm(forms.Form):
    airport_csv = forms.FileField(label='Select a file')

class SingleAirportUpdate(forms.ModelForm):
    class Meta:
        model = Airport
        fields = ['icao', 'iata', 'name', 'city', 'state', 'country']
        labels = {'icao':'ICAO Code', 'iata':'IATA Code'}

# Customer forms
class CustomerForm(forms.Form):
    customer_csv = forms.FileField(label='Select a file')

class SingleCustomerUpdate(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['cust_id', 'name', 'email']
        labels = {'cust_id': 'Customer Code'}

# Customer-Airport forms
class CustAirForm(forms.Form):
    custair_csv = forms.FileField(label='Select a file')

class SingleCustAirUpdate(forms.ModelForm):
    class Meta:
        model = CustomerAirport
        fields = ['customer', 'airport']
        labels = {'customer': 'Customer Code', 'airport':'ICAO Code'}