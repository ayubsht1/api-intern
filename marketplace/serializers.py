from rest_framework import serializers
from .models import (Category, Product, ProductGallery, WishList, Cart, CartItem, Order, 
OrderItem ,ShippingAddress, Bundle)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGallery
        fields = '__all__'

class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = '__all__'
        read_only_fields = ['user']

class BundleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bundle
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source="product.name")
    bundle_name = serializers.ReadOnlyField(source="bundle.name")
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'bundle', 'product_name', 'bundle_name', 'quantity', 'total_price']

    def validate(self, data):
        product = data.get('product')
        bundle = data.get('bundle')

        if not product and not bundle:
            raise serializers.ValidationError("You must provide either a product or a bundle.")
        if product and bundle:
            raise serializers.ValidationError("You can only provide either a product or a bundle, not both.")

        return data

    def get_total_price(self, obj):
        if obj.product:
            return obj.product.price * obj.quantity
        elif obj.bundle:
            return obj.bundle.calculate_price() * obj.quantity
        return 0

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['uuid', 'user', 'items', 'total_price']
        read_only_fields = ['uuid', 'user', 'items']

    def get_total_price(self, obj):
        return sum(item.product.price * item.quantity if item.product else item.bundle.calculate_price() * item.quantity
                   for item in obj.items.all())
        
class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    bundle_name = serializers.ReadOnlyField(source='bundle.name')
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'bundle', 'bundle_name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True, source='order_items')
    shipping_address = ShippingAddressSerializer(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['uuid', 'user', 'total_price', 'status', 'created_at', 'updated_at']

    def validate_payment_method(self, value):
        valid_methods = ['card','wallet']
        if value not in valid_methods:
            raise serializers.ValidationError('Invalid payment method.')
        return value
    