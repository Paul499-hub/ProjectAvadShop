import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Product, Booking
from django.http import HttpResponseNotFound
from datetime import datetime
# Create your views here.

#SSL NOT CERTIFIED YET. LOOK FOR WEBHOSTING INSTRUCTIONS ON HOW TO INSTALL SSL

def product_list(request):
    products=Product.objects.all()
    return render(request, 'shop/product_page.html', {'products':products})


def home(request):
    products=Product.objects.all()
    timestamp = datetime.now().timestamp()
    return render(request, 'shop/home_page.html', {'products':products, 'timestamp':timestamp})


stripe.api_key = settings.STRIPE_SECRET_KEY

def book_seminar(request):
    if request.method == 'POST':
        customer_name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        
        booking = Booking.objects.create(
            customer_name=customer_name,
            email=email,
            phone=phone,
            product=product
        )

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency' : 'eur',
                    'product_data' : {
                        'name': f'Seminar Booking:{product.name}'
                    },
                    'unit_amount': int(product.price*100)
                },
                'quantity':1
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/success/') + f"?booking_id={booking.id}",
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        return redirect(session.url, code=303)
    
    product_id=request.GET.get('product_id')
    timestamp = datetime.now().timestamp()
    return render(request, 'shop/booking_form.html', {'product_id':product_id, 'timestamp':timestamp})


def payment_success(request):
    booking_id = request.GET.get('booking_id')
    if booking_id:
        booking = Booking.objects.get(id=booking_id)
        booking.paid = True
        booking.save()
        return render(request, 'shop/success.html')
    else:
        return HttpResponseNotFound("ERROR: Missing Booking id. Try resubmitting the form")
    

def payment_cancel(request):
    return render(request,'shop/cancel.html')