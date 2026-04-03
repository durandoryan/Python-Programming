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
