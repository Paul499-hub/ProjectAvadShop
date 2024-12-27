import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Product, Booking
from django.http import HttpResponseNotFound
from datetime import datetime
import os
from google.oauth2 import id_token
from google.auth.transport import requests
from django.http import JsonResponse
# Create your views here.

#SSL NOT CERTIFIED YET. LOOK FOR WEBHOSTING INSTRUCTIONS ON HOW TO INSTALL SSL
# EPIC FONTS -- Visit The League of Moveable Type’s official website.

def product_list(request):
    products=Product.objects.all()
    return render(request, 'shop/product_page.html', {'products':products})


def home(request):
    products=Product.objects.all()
    timestamp = datetime.now().timestamp()



    # GOOGLE LOGIN RESPONSE
        # Check if there is an authorization code in the request
    auth_code = request.GET.get('code')
    if auth_code:
        try:
            # Exchange the authorization code for an ID token
            token_url = "https://oauth2.googleapis.com/token"
            payload = {
                'code': auth_code,
                'client_id': settings.GOOGLE_CLIENT_ID,
                'client_secret': settings.GOOGLE_CLIENT_SECRET,
                'redirect_uri': 'https://8080-cs-3d8adc57-bf91-486e-bf47-651e90843cdd.cs-europe-west4-bhnf.cloudshell.dev/',
                'grant_type': 'authorization_code'
            }
            response = requests.post(token_url, data=payload)
            token_data = response.json()
            
            # Verify the ID token
            id_info = id_token.verify_oauth2_token(
                token_data['id_token'], requests.Request(), settings.GOOGLE_CLIENT_ID
            )
            # You now have user info from Google
            user_email = id_info.get('email')
            # Add logic here to log in the user or create a user account
            
            return redirect('/')  # Redirect back to the main page
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)




    # GET ALL IMG NAMES FROM media carousel folder -- FOR CAROUSEL IMGAGES DISPLAY
    carousel_folder_path = os.path.join(settings.MEDIA_ROOT, 'carousel_images')
    files = os.listdir(carousel_folder_path)

    # GET ALL VIDEOS FROM media video folder
    video_folder_path = os.path.join(settings.MEDIA_ROOT, 'videos')
    video_files = os.listdir(video_folder_path)
    print(f'video_files: {video_files}')

    return render(request, 'shop/home_page.html', {'products':products, 'timestamp':timestamp, 'carousel':files, 'videos':video_files}) #  'carousel':carousel


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