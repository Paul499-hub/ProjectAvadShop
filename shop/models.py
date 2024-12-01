from django.db import models

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    date=models.DateTimeField()
    event_location = models.CharField(max_length=200, default='Location not set yet.')
    picture=models.CharField(max_length=400, default='No picture') #/shop/img/BEARD.jpg
    def __str__(self):
        return self.name
    

class Booking(models.Model):
    # VISIBLE FIELDS
    customer_name = models.CharField(max_length=255)
    email= models.EmailField()
    phone = models.CharField(max_length=20)

    # INVISIBLE FIELDS
    paid = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bookings')
    def __str__(self):
        return  f"{self.customer_name} - {self.product.name}"
