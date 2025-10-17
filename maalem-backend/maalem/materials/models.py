from django.db import models
from django.contrib.auth import get_user_model
from maalem.projects.models import Project

User = get_user_model()

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    website = models.URLField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Material(models.Model):
    UNIT_CHOICES = (
        ('piece', 'Pièce'),
        ('kg', 'Kilogramme'),
        ('m', 'Mètre'),
        ('m2', 'Mètre carré'),
        ('m3', 'Mètre cube'),
        ('l', 'Litre'),
        ('pack', 'Pack'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    specifications = models.JSONField(default=dict)  # Caractéristiques techniques
    created_at = models.DateTimeField(auto_now_add=True)

class MaterialPrice(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='prices')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='material_prices')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

class MaterialOrder(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Brouillon'),
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('shipped', 'Expédiée'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='material_orders')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    shipping_address = models.TextField()
    notes = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

class OrderItem(models.Model):
    order = models.ForeignKey(MaterialOrder, on_delete=models.CASCADE, related_name='items')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    received_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)

    @property
    def total_price(self):
        return self.quantity * self.unit_price

class MaterialInventory(models.Model):
    artisan = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'artisan'}
    )
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    last_updated = models.DateTimeField(auto_now=True)
    minimum_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('artisan', 'material', 'location')