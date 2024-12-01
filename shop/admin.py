from django.contrib import admin
from .models import Product, Booking

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=('name','price','date')
    search_fields=('name',)
admin.site.register(Product, ProductAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display=('customer_name','paid')
admin.site.register(Booking, BookingAdmin)