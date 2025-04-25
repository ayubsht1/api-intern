from rest_framework.response import Response
from rest_framework import generics, status, permissions
# from rest_framework.filters import SearchFilter
from django.db import transaction
from .models import (Category, Product, ProductGallery, WishList, Cart, CartItem, Order, OrderItem, ShippingAddress, Bundle)
from .serializers import (CategorySerializer, ProductSerializer, ProductGallerySerializer, WishListSerializer, CartSerializer, CartItemSerializer,
OrderSerializer, ShippingAddressSerializer, BundleSerializer)
from django.http import HttpResponse
from django.utils.timezone import now, timedelta

def home (request):
    return HttpResponse('Welcome to the home page!')

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'uuid'
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductImageUploadView(generics.ListCreateAPIView):
    queryset = ProductGallery.objects.all()
    serializer_class = ProductGallerySerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductGallery.objects.all()
    serializer_class = ProductGallerySerializer
    lookup_field = 'pk'
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class WishListListCreateView(generics.ListCreateAPIView):
    serializer_class = WishListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishList.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WishListDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WishListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishList.objects.filter(user=self.request.user)

class BundleListCreateView(generics.ListCreateAPIView):
    queryset = Bundle.objects.prefetch_related('products').all()
    serializer_class = BundleSerializer

    # def get_permissions(self):
    #     if self.request.method == 'POST':
    #         return [permissions.IsAdminUser()]
    #     return [permissions.AllowAny()]
    
    def list(self, request, *args, **kwargs):
        bundles = self.get_queryset()
        data = []
        for bundle in bundles:
            total_price = bundle.calculate_price() if hasattr(bundle, 'calculate_price') else 0
            data.append({
                'id': bundle.id,
                'name': bundle.name,
                'products': ProductSerializer(bundle.products.all(), many=True).data if bundle.products.exists() else [],
                'total_price': total_price
            })
        return Response(data)
    
class BundleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bundle.objects.prefetch_related('products').all()
    serializer_class = BundleSerializer
    lookup_field = 'uuid'

    # def get_permissions(self):
    #     if self.request.method in ['PUT', 'DELETE']:
    #         return [permissions.IsAdminUser()]
    #     return [permissions.AllowAny()]
    
    def retrieve(self, request, *args, **kwargs):
        bundle = self.get_object()
        total_price = bundle.calculate_price() if hasattr(bundle, 'calculate_price') else 0
        data = {
            'id': bundle.id,
            'name': bundle.name,
            'products': ProductSerializer(bundle.products.all(), many=True).data if bundle.products.exists() else [],
            'total_price': total_price,
        }
        return Response(data)

class CartDetailView(generics.RetrieveUpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = 'uuid'
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart
    
class CartItemListCreateView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    # permission_classes = [permissions.IsAuthenticated]

class ShippingAddressListCreateView(generics.ListCreateAPIView):
    serializer_class = ShippingAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ShippingAddressDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ShippingAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retrieve a shipping address for the authenticated user."""
        return ShippingAddress.objects.filter(user=self.request.user)

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return Response({"error": "Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        payment_method = request.data.get('payment_method')
        shipping_address_id = request.data.get('shipping_address_id', None)
        cart_serializer = CartSerializer(cart)
        total = cart_serializer.data['total_price']

        recent_order = Order.objects.filter(
            user=user,
            total_price=total,
            payment_method=payment_method,
            shipping_address_id = shipping_address_id,
            created_at__gte=now() - timedelta(minutes=1)  # Prevents duplicate orders within 1 minute
        ).first()

        if recent_order:
            return Response(
                {"error": "Duplicate order detected. Please wait before placing another order."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        shipping_address = None
        if shipping_address_id:
            try:
                shipping_address = ShippingAddress.objects.get(id=shipping_address_id, user=user)
            except ShippingAddress.DoesNotExist:
                return Response({"error":"Shipping address not found."},status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            order = Order.objects.create(
                user=user, 
                payment_method=payment_method,
                total_price=total,
                shipping_address=shipping_address
            )

            for item in cart_items:
                if item.product:
                    # Check stock for normal products
                    if item.quantity > item.product.stock:
                        return Response(
                            {"error": f"Not enough stock for {item.product.name}"}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    # Create order item for normal product
                    OrderItem.objects.create(
                        order=order, 
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price * item.quantity
                    )

                    # Reduce stock for the product
                    item.product.stock -= item.quantity
                    item.product.save()

                elif item.bundle:
                    # Get all products inside the bundle
                    bundle_products = item.bundle.products.all()

                    # Step 1: Check if all products have enough stock
                    for product in bundle_products:
                        if item.quantity > product.stock:
                            return Response(
                                {"error": f"Not enough stock for {product.name} in bundle {item.bundle.name}"},
                                status=status.HTTP_400_BAD_REQUEST
                            )

                    # Step 2: Create an order item for the bundle
                    OrderItem.objects.create(
                        order=order,
                        bundle=item.bundle,
                        quantity=item.quantity,
                        price=item.bundle.calculate_price() * item.quantity
                    )

                    # Step 3: Reduce stock for all products inside the bundle
                    for product in bundle_products:
                        product.stock -= item.quantity  # Reduce stock based on bundle quantity
                        product.save()

            # Step 4: Clear the cart after order creation
            cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'uuid'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    