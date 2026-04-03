import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
dice.setup()

from myapp.models import Revenue, RevenueCategory, Transaction

# Test the models
cat = RevenueCategory.objects.create(name="Sales")
rev = Revenue.objects.create(amount=1000.50, category=cat)
trans = Transaction.objects.create(revenue=rev, notes="Test transaction")

print("✓ Category created:", cat.name)
print("✓ Revenue created: $", rev.amount)
print("✓ Transaction created:", trans.notes)