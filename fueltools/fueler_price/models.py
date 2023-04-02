from django.db import models


class Airport(models.Model):
    icao = models.CharField(max_length=4, primary_key=True)
    iata = models.CharField(max_length=3, blank=True)
    name = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.icao} - {self.name}, {self.city}, {self.country}"


class Customer(models.Model):
    cust_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.cust_id} - {self.name}"


class FuelPrice(models.Model):
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE)
    date = models.DateField()
    supplier = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    fee = models.DecimalField(max_digits=10, decimal_places=4)
    note = models.TextField(blank=True)
    #note = models.CharField(blank=True)
    other_variable = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.airport}: {self.supplier} - {self.price}"


class CustomerAirport(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer} - {self.airport}"
