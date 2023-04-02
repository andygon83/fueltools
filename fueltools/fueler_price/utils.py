from django.shortcuts import render
from .models import Airport, FuelPrice, Customer, CustomerAirport
import csv
import io


# script to handle upload of FuelPrice data 
def handle_fuel_price_file(f):
    decoded_f = f.read().decode('utf-8')
    io_string = io.StringIO(decoded_f)
    reader = csv.reader(io_string)
    expected_fields = 7  # expected number of fields in each row
    expected_headers = ['Airport ID', 'Date', 'Supplier', 'Price', 'Fee', 'Note', 'Other Variables']
    headers = next(reader)  # read the header row

    # Check the submitted csv's headers to make sure its right size and names
    if len(headers) != expected_fields or headers != expected_headers:
        raise ValueError('Incorrect CSV format. Please ensure the CSV file has the correct number of fields and headers.')

    # Checks the length of every row for odd shaped csv's and assigns the data to variables. Then calls on update_or_create to update the database
    for row in reader:
        if len(row) != expected_fields:
            raise ValueError('Incorrect CSV format. Please ensure all rows have the correct number of fields.')

        airport = Airport.objects.get(pk=row[0])
        date = row[1]
        supplier = row[2]
        price = row[3]
        fee = row[4]
        note = row[5]
        other_variable = row[6]


        fuel_price, created = FuelPrice.objects.update_or_create(
            airport=airport,
            date=date,
            defaults={
                'supplier': supplier,
                'price': price,
                'fee': fee,
                'note': note,
                'other_variable': other_variable
            }
        )

        if not created:
            print(f'Updated existing Fuel Price record: {fuel_price}')

# Script to handle update to Airport data
def handle_airport_file(f):
    decoded_f = f.read().decode('utf-8')
    io_string = io.StringIO(decoded_f)
    reader = csv.reader(io_string)
    expected_fields = 6  # expected number of fields in each row
    expected_headers = ['ICAO', 'IATA', 'Name', 'City', 'State', 'Country']
    headers = next(reader)  # read the header row

    # Check the submitted csv's headers to make sure its right size and names
    if len(headers) != expected_fields or headers != expected_headers:
        raise ValueError('Incorrect CSV format. Please ensure the CSV file has the correct number of fields and headers.')

    # Checks the length of every row for odd shaped csv's and assigns the data to variables. Then calls on update_or_create to update the database
    for row in reader:
        if len(row) != expected_fields:
            raise ValueError('Incorrect CSV format. Please ensure all rows have the correct number of fields.')

        icao = row[0]
        iata = row[1]
        name = row[2]
        city = row[3]
        state = row[4]
        country = row[5]

        airport, created = Airport.objects.update_or_create(
            icao=icao,
            defaults={
                'iata': iata,
                'name': name,
                'city': city,
                'state': state,
                'country': country
            }
        )
        if not created:
            print(f'Updated existing Airport record: {airport}')


# Script to handle update of Customer data
def handle_customer_file(f):
    decoded_f = f.read().decode('utf-8')
    io_string = io.StringIO(decoded_f)
    reader = csv.reader(io_string)
    expected_fields = 3  # expected number of fields in each row
    expected_headers = ['Customer Code','Name', 'Email']
    headers = next(reader)  # read the header row

    # Check the submitted csv's headers to make sure its right size and names
    if len(headers) != expected_fields or headers != expected_headers:
        raise ValueError('Incorrect CSV format. Please ensure the CSV file has the correct number of fields and headers.')

    # Checks the length of every row for odd shaped csv's and assigns the data to variables. Then calls on update_or_create to update the database
    for row in reader:
        if len(row) != expected_fields:
            raise ValueError('Incorrect CSV format. Please ensure all rows have the correct number of fields.')

        cust_id = row[0]
        name = row[1]
        email = row[2]

        customer, created = Customer.objects.update_or_create(
            cust_id=cust_id,
            defaults={
                'name': name,
                'email': email,
            }
        )

        if not created:
            print(f'Updated existing Customer record: {customer}')

# Script to handle Customer-Airport relationship data
def handle_customerairport_file(f):
    decoded_f = f.read().decode('utf-8')
    io_string = io.StringIO(decoded_f)
    reader = csv.reader(io_string)
    cust_id = next(reader)[0]  

    customer, _ =Customer.objects.get_or_create(cust_id=cust_id)

    for row in reader:
        
        airport, _ = Airport.objects.get_or_create(icao=row[0])

        CustomerAirport.objects.update_or_create(
            customer = customer, 
            airport=airport
        )

