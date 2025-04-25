from django.db import models
from django.conf import settings
# from authentication.models import User
from authentication.models import User
import uuid


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    tags = models.CharField(max_length=255, blank=True) 
    is_featured = models.BooleanField(default=False) 
    thumnail = models.ImageField(upload_to='static/images/products/thumbnails/', blank=True, null=True)

    def __str__(self):
        return self.name
    
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/images/products/gallery/')

    def __str__(self):
        return f"Image for {self.product.name}"
    
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} wishlisted {self.product.name}"
 
class Bundle(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255, unique=True)
    products = models.ManyToManyField(Product)

    def calculate_price(self):
        total = sum(product.price for product in self.products.all())
        return total
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)  # Allow for product
    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE, null=True, blank=True)  # Allow for bundle
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        if self.product:
            return f"{self.quantity}*{self.product.name}"
        elif self.bundle:
            return f"{self.quantity}*{self.bundle.name}"
       
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address_line = models.CharField(max_length=255, unique=True)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}, {self.address_line}, {self.city}, {self.country}"
    
class Order(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('wallet', 'Wallet'),
        ('cash', 'cash'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True, related_name='order_items')
    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE, null=True, blank=True, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        if self.product:
            return f"{self.quantity}*{self.product.name}"
        elif self.bundle:
            return f"{self.quantity}*{self.bundle.name}"