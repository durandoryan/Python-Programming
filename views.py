from django.shortcuts import render

def home(request):
    return render(request, 'orders/home.html')

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Product
from .forms import OrderItemForm

@login_required
def create_order(request):
    order = Order.objects.create(customer=request.user)
    return redirect('add_item', order_id=order.id)

@login_required
def add_item(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.order = order
            item.save()
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderItemForm()
    return render(request, 'orders/add_item.html', {'form': form, 'order': order})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})
