from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/<slug>/', views.ProductDetailView.as_view(), name='product'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('product/add-product/<slug>/', views.add_to_cart, name='add_product')
]
