from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from django.db import transaction
from .models import (Category, Product, Cart, CartItem, Order, OrderItem, ShippingAddress, Bundle)
from .serializers import (CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer,
OrderSerializer, ShippingAddressSerializer, BundleSerializer)
from django.http import HttpResponse
from django.utils.timezone import now, timedelta


def home (request):
    return HttpResponse('Welcome to the home page!')

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [permissions.IsAuthenticated]

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
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CartDetailView(generics.RetrieveUpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Cart.objects.get(user= self.request.user)
    
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
        cart_serializer = CartSerializer(cart)
        total = cart_serializer.data['total_price']

        recent_order = Order.objects.filter(
            user=user,
            total_price=total,
            payment_method=payment_method,
            created_at__gte=now() - timedelta(minutes=1)  # Prevents duplicate orders within 1 minute
        ).first()

        if recent_order:
            return Response(
                {"error": "Duplicate order detected. Please wait before placing another order."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            order = Order.objects.create(
                user=user, 
                payment_method=payment_method,
                total_price=total
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
                        price=item.bundle.calculate_discounted_price() * item.quantity
                    )

                    # Step 3: Reduce stock for all products inside the bundle
                    for product in bundle_products:
                        product.stock -= item.quantity  # Reduce stock based on bundle quantity
                        product.save()

            # Step 4: Clear the cart after order creation
            cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    
class OrderDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class ShippingAddressAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        addresses = ShippingAddress.objects.filter(user=request.user)
        serializer = ShippingAddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ShippingAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            discounted_price = bundle.calculate_discounted_price() if hasattr(bundle, 'calculate_discounted_price') else 0
            data.append({
                'id': bundle.id,
                'name': bundle.name,
                'products': ProductSerializer(bundle.products.all(), many=True).data if bundle.products.exists() else [],
                'discount_percentage': bundle.discount_percentage,
                'discounted_price': discounted_price
            })
        return Response(data)
    
class BundleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bundle.objects.prefetch_related('products').all()
    serializer_class = BundleSerializer
    lookup_field = 'pk'

    # def get_permissions(self):
    #     if self.request.method in ['PUT', 'DELETE']:
    #         return [permissions.IsAdminUser()]
    #     return [permissions.AllowAny()]
    
    def retrieve(self, request, *args, **kwargs):
        bundle = self.get_object()
        discounted_price = bundle.calculate_discounted_price() if hasattr(bundle, 'calculate_discounted_price') else 0
        data = {
            'id': bundle.id,
            'name': bundle.name,
            'products': ProductSerializer(bundle.products.all(), many=True).data if bundle.products.exists() else [],
            'discount_percentage': bundle.discount_percentage,
            'discounted_price': discounted_price,
        }
        return Response(data)