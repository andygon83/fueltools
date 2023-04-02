from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import OuterRef, Subquery, Max
from django.template.defaultfilters import floatformat
from .models import CustomerAirport, FuelPrice, Customer, Airport
from .forms import FuelPriceForm, AirportForm, SingleFuelUpdate, SingleAirportUpdate, CustomerForm, SingleCustomerUpdate, CustAirForm, SingleCustAirUpdate
from .utils import handle_fuel_price_file, handle_airport_file, handle_customer_file, handle_customerairport_file



def index(request):
    # Retrieve a list of all customers and airports from the database
    customers = Customer.objects.all()
    airports = Airport.objects.all()
    
    # Render the index.html template with the customers and airports as context
    context = {'customers': customers, 'airports': airports}
    return render(request, 'index.html', context)

# Universal view to route every update form to their processing script in utils.py. 
# Can be parcelled out if updates are split to different routes
def upload_file(request):
    if request.method == 'POST':
        fuel_price_form = FuelPriceForm(request.POST, request.FILES)
        sing_fuel_price_form = SingleFuelUpdate(request.POST)
        airport_form = AirportForm(request.POST, request.FILES)
        sing_airport_form = SingleAirportUpdate(request.POST)
        customer_form = CustomerForm(request.POST, request.FILES)
        sing_customer_form = SingleCustomerUpdate(request.POST)
        custair_form = CustAirForm(request.POST, request.FILES)
        sing_custair_form = SingleCustAirUpdate(request.POST)

        # Validation and passing thru of FuelPrice updates
        if fuel_price_form.is_valid():
            handle_fuel_price_file(request.FILES['fuel_price_csv'])
            return redirect("success")
        elif sing_fuel_price_form.is_valid():
            FuelPrice.objects.update_or_create(
                airport=sing_fuel_price_form.cleaned_data['airport'],
                date=sing_fuel_price_form.cleaned_data['date'],
                defaults={
                    'supplier': sing_fuel_price_form.cleaned_data['supplier'],
                    'price': sing_fuel_price_form.cleaned_data['price'],
                    'fee': sing_fuel_price_form.cleaned_data['fee'],
                    'note': sing_fuel_price_form.cleaned_data['note'],
                    'other_variable': sing_fuel_price_form.cleaned_data['other_variable']
                }
            )
            return redirect("success")
        
        # Validation and passing thru of Airport updates        
        elif airport_form.is_valid():
            handle_airport_file(request.FILES['airport_csv'])
            return redirect("success")
        elif sing_airport_form.is_valid():
            Airport.objects.update_or_create(
                iata_code=sing_airport_form.cleaned_data['iata_code'],
                defaults={
                    'name': sing_airport_form.cleaned_data['name'],
                    'city': sing_airport_form.cleaned_data['city'],
                    'state': sing_airport_form.cleaned_data['state'],
                    'country': sing_airport_form.cleaned_data['country'],
                }
            )
            return redirect("success")
        
        # Validation and passing thru of Customer updates
        elif customer_form.is_valid():
            handle_customer_file(request.FILES['customer_csv'])
            return redirect("success")                
        elif sing_customer_form.is_valid():
            Customer.objects.update_or_create(
                cust_id=sing_customer_form.cleaned_data['cust_id'],
                defaults={
                    'name': sing_customer_form.cleaned_data['name'],
                    'email': sing_customer_form.cleaned_data['email'],
                }
            )
            return redirect("success")
        
        # Validation and passing thru of CustomerAirport updates
        elif custair_form.is_valid():
            handle_customerairport_file(request.FILES['custair_csv'])
            return redirect("success")                
        elif sing_custair_form.is_valid():
            CustomerAirport.objects.update_or_create(
                customer=sing_custair_form.cleaned_data['customer'],
                airport= sing_custair_form.cleaned_data['airport']
            )
            return redirect("success")

    # Render empty forms and upload fields
    else:
        fuel_price_form = FuelPriceForm()
        sing_fuel_price_form = SingleFuelUpdate()
        airport_form = AirportForm()
        sing_airport_form = SingleAirportUpdate()
        customer_form = CustomerForm()
        sing_customer_form = SingleCustomerUpdate()
        custair_form = CustAirForm()
        sing_custair_form = SingleCustAirUpdate()

    return render(request, 'upload_file.html', {'fuel_price_form': fuel_price_form, 'airport_form': airport_form, 
                                                'sing_fuel_price_form':sing_fuel_price_form, 'sing_airport_form':sing_airport_form, 
                                                'sing_customer_form':sing_customer_form, 'customer_form':customer_form, 
                                                'custair_form': custair_form, "sing_custair_form": sing_custair_form,
                                                'error_message': 'Invalid file format.'})   


# View returning single station and client historical price data
def query_results(request):
    if request.method == 'POST':
        # Retrieve the selected customer and airport IDs from the request object
        customer_id = request.POST['customer_id']
        airport_id = request.POST['airport_id']


        # Query the CustomerAirport model to check if the customer has a relationship with the airport
        customer_airport_exists = CustomerAirport.objects.filter(airport_id=airport_id, customer_id=customer_id).exists()
        
        if customer_airport_exists:
            # Query the FuelPrice model for the desired information
            prices = FuelPrice.objects.filter(airport_id=airport_id)
            for row in prices:
                row.total_price = row.price + row.fee
                row.total_price_format = floatformat(row.total_price, 4)
            
            # Render the results.html template with the query results as context
            context = {'prices': prices}
            return render(request, 'query_results.html', context)
        else:
            # If the customer does not have a relationship with the selected airport, show an error message
            error_message = "Selected customer does not have a relationship with the selected airport."
            context = {'error_message': error_message}
            return render(request, 'query_results.html', context)
    else:
        # Redirect the user back to the index page if they accessed this view via GET request
        return HttpResponseRedirect(reverse('index'))


def success(request):
    return render(request, 'success.html')


# def price_list(request):
#     if request.method == 'POST':
#         # Retrieve the selected customer and airport IDs from the request object
#         customer_id = request.POST['customerprice_id']

#         customer_airports = CustomerAirport.objects.filter(customer_id=customer_id)
#         fuel_prices = FuelPrice.objects.filter(airport__in=customer_airports.values_list('airport_id', flat=True))
#         for row in fuel_prices:
#                 row.total_price = row.price + row.fee
#                 row.total_price_format = floatformat(row.total_price, 4)
#         context ={'fuel_prices': fuel_prices}
#         return render(request, 'price_list.html', context)
#     else:
#         return HttpResponseRedirect(reverse('index'))




def price_list(request):
    if request.method == 'POST':
        # Retrieve the selected customer and airport IDs from the request object
        customer_id = request.POST['customerprice_id']

        customer_airports = CustomerAirport.objects.filter(customer_id=customer_id)
        
        # annotate each airport with the max date of FuelPrice and filter by it
        fuel_prices = FuelPrice.objects.filter(
            airport__in=customer_airports.values_list('airport_id', flat=True),
            date=Subquery(
                FuelPrice.objects.filter(
                    airport=OuterRef('airport')
                ).values('airport').annotate(max_date=Max('date')).values('max_date')[:1]
            )
        )
        
        for row in fuel_prices:
            row.total_price = row.price + row.fee
            row.total_price_format = floatformat(row.total_price, 4)
        
        context = {'fuel_prices': fuel_prices}
        return render(request, 'price_list.html', context)
    else:
        return HttpResponseRedirect(reverse('index'))
