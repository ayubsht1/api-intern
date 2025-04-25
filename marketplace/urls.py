from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (CategoryListCreateView, ProductListCreateView,CartDetailView, CartItemListCreateView, CartItemDetailView, OrderListCreateView, OrderDetailView,
                     BundleListCreateView, CategoryDetailView, ProductDetailView, ProductImageUploadView, ProductImageDetailView, BundleDetailView, ShippingAddressListCreateView, ShippingAddressDetailView,
                     WishListListCreateView,WishListDetailView)
from . import views


urlpatterns = [
    path('',views.home, name='home'),
     path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<uuid:uuid>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/gallery/', ProductImageUploadView.as_view(), name='product-upload-image'),
    path('products/gallery/<int:pk>/', ProductImageDetailView.as_view(), name='product-upload-image'),
    path('wish/', WishListListCreateView().as_view(), name='wishlist-list-create'),
    path('wish/<int:pk>', WishListDetailView().as_view(), name='wishlist-detail'),
    path('cart/', CartDetailView.as_view(), name='cart_detail'), 
    path('cart/items/', CartItemListCreateView.as_view(), name='cart_item_list_create'),  
    path('cart/items/<int:pk>/', CartItemDetailView.as_view(), name='cart_item_detail'), 
    path('orders/', OrderListCreateView.as_view(), name='order_list'),
    path('orders/<uuid:uuid>/', OrderDetailView.as_view(), name='order_detail'),
    path('shipping-addresses/', ShippingAddressListCreateView.as_view(), name='shipping_address_list'),
    path('shipping-addresses/<int:pk>/', ShippingAddressDetailView.as_view(), name='shipping_address'),
    path('bundles/', BundleListCreateView.as_view(), name='bundle_list'),
    path('bundles/<uuid:uuid>/', BundleDetailView.as_view(), name='bundle-detail'),

]