from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('', views.home, name='home' ),
    path('book/', views.book_seminar, name='book_seminar'),
    path('success/', views.payment_success, name='payment_success'),
    path('payment_cancel/', views.payment_cancel, name='payment_cancel'),
]