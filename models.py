from django.db import models

class Revenue(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey('RevenueCategory', related_name='revenues', on_delete=models.CASCADE)

class RevenueCategory(models.Model):
    name = models.CharField(max_length=100)

class Transaction(models.Model):
    revenue = models.ForeignKey(Revenue, related_name='transactions', on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=100)

class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=[('pending','Pending'),('completed','Completed')])
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
