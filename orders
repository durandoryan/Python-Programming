from django.db import models
from django.core.validators import MinValueValidator


# ---------------------------
# MENU
# ---------------------------
class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('entree', 'Entree'),
        ('salad', 'Salad'),
        ('beverage', 'Beverage'),
        ('dessert', 'Dessert'),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} (${self.price})"


# ---------------------------
# ORDER
# ---------------------------
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    table_number = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    discount_percent = models.FloatField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - Table {self.table_number}"

    # ---------------------------
    # BUSINESS LOGIC
    # ---------------------------
    def get_subtotal(self):
        return sum(item.get_subtotal() for item in self.items.all())

    def get_discount_amount(self):
        return self.get_subtotal() * (self.discount_percent / 100)

    def get_total(self):
        return self.get_subtotal() - self.get_discount_amount()

    def complete_order(self):
        from django.utils import timezone
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()

    def cancel_order(self):
        self.status = 'cancelled'
        self.save()


# ---------------------------
# ORDER ITEMS
# ---------------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

    def get_subtotal(self):
        return self.menu_item.price * self.quantity


# ---------------------------
# OPTIONAL: TRANSACTIONS
# ---------------------------
class Transaction(models.Model):
    order = models.ForeignKey(Order, related_name='transactions', on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Transaction for Order #{self.order.id}"
