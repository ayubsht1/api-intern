from django.urls import path
from .views import (CategoryListCreateView, ProductListCreateView,CartDetailView, CartItemListCreateView, CartItemDetailView, OrderListCreateView, OrderDetailView, ShippingAddressAPIView,
                     BundleListCreateView, CategoryDetailView, ProductDetailView, BundleDetailView)
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('cart/', CartDetailView.as_view(), name='cart_detail'), 
    path('cart/items/', CartItemListCreateView.as_view(), name='cart_item_list_create'),  
    path('cart/items/<int:pk>/', CartItemDetailView.as_view(), name='cart_item_detail'), 
    path('orders/', OrderListCreateView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('shipping-addresses/', ShippingAddressAPIView.as_view(), name='shipping_address_list'),
    path('bundles/', BundleListCreateView.as_view(), name='bundle_list'),
    path('bundles/<int:pk>/', BundleDetailView.as_view(), name='bundle-detail'),

]