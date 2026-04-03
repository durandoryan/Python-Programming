from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass, field
import json

class OrderStatus(Enum):
    """Enum for order statuses"""
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass
class MenuItem:
    """Represents a menu item"""
    item_id: str
    name: str
    price: float
    category: str
    description: str = ""
    
    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")

@dataclass
class OrderItem:
    """Represents an item in an order"""
    menu_item: MenuItem
    quantity: int
    
    def get_subtotal(self) -> float:
        return self.menu_item.price * self.quantity

@dataclass
class Order:
    """Represents a customer order"""
    order_id: str
    table_number: int
    items: List[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    discount_percent: float = 0.0
    
    def add_item(self, menu_item: MenuItem, quantity: int) -> None:
        """Add item to order"""
        order_item = OrderItem(menu_item, quantity)
        self.items.append(order_item)
    
    def remove_item(self, item_id: str) -> bool:
        """Remove item from order by menu item ID"""
        self.items = [item for item in self.items if item.menu_item.item_id != item_id]
        return True
    
    def get_subtotal(self) -> float:
        """Calculate order subtotal before discount"""
        return sum(item.get_subtotal() for item in self.items)
    
    def get_discount_amount(self) -> float:
        """Calculate discount amount"""
        return self.get_subtotal() * (self.discount_percent / 100)
    
    def get_total(self) -> float:
        """Calculate order total after discount"""
        return self.get_subtotal() - self.get_discount_amount()
    
    def complete_order(self) -> None:
        """Mark order as completed"""
        self.status = OrderStatus.COMPLETED
        self.completed_at = datetime.now()
    
    def cancel_order(self) -> None:
        """Cancel the order"""
        self.status = OrderStatus.CANCELLED

class Menu:
    """Manages restaurant menu"""
    def __init__(self):
        self.items: Dict[str, MenuItem] = {}
    
    def add_item(self, menu_item: MenuItem) -> None:
        """Add item to menu"""
        self.items[menu_item.item_id] = menu_item
    
    def remove_item(self, item_id: str) -> bool:
        """Remove item from menu"""
        if item_id in self.items:
            del self.items[item_id]
            return True
        return False
    
    def get_item(self, item_id: str) -> Optional[MenuItem]:
        """Get menu item by ID"""
        return self.items.get(item_id)
    
    def get_items_by_category(self, category: str) -> List[MenuItem]:
        """Get all items in a category"""
        return [item for item in self.items.values() if item.category == category]
    
    def display_menu(self) -> None:
        """Display entire menu"""
        if not self.items:
            print("Menu is empty")
            return
        
        categories = {}
        for item in self.items.values():
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item)
        
        for category, items in categories.items():
            print(f"\n--- {category.upper()} ---")
            for item in items:
                print(f"{item.name} (${item.price:.2f}) - {item.description}")

class RevenueManager:
    """Manages restaurant revenue and orders"""
    def __init__(self):
        self.orders: Dict[str, Order] = {}
        self.menu = Menu()
        self.cash_register: float = 0.0
    
    def create_order(self, order_id: str, table_number: int) -> Order:
        """Create a new order"""
        order = Order(order_id, table_number)
        self.orders[order_id] = order
        return order
    
    def get_order(self, order_id: str) -> Optional[Order]:
        """Retrieve order by ID"""
        return self.orders.get(order_id)
    
    def complete_order(self, order_id: str) -> bool:
        """Complete an order and add to register"""
        order = self.get_order(order_id)
        if order and order.status == OrderStatus.PENDING:
            order.complete_order()
            self.cash_register += order.get_total()
            return True
        return False
    
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        order = self.get_order(order_id)
        if order:
            order.cancel_order()
            return True
        return False
    
    def get_daily_revenue(self) -> float:
        """Calculate today's total revenue"""
        today = datetime.now().date()
        total = 0.0
        for order in self.orders.values():
            if order.status == OrderStatus.COMPLETED and order.completed_at.date() == today:
                total += order.get_total()
        return total
    
    def get_revenue_by_status(self) -> Dict[str, float]:
        """Get revenue breakdown by order status"""
        revenue = {
            "completed": 0.0,
            "pending": 0.0,
            "cancelled": 0.0
        }
        for order in self.orders.values():
            if order.status == OrderStatus.COMPLETED:
                revenue["completed"] += order.get_total()
            elif order.status == OrderStatus.PENDING:
                revenue["pending"] += order.get_total()
            elif order.status == OrderStatus.CANCELLED:
                revenue["cancelled"] -= order.get_total()
        return revenue
    
    def get_category_revenue(self) -> Dict[str, float]:
        """Get revenue breakdown by menu category"""
        revenue = {}
        for order in self.orders.values():
            if order.status == OrderStatus.COMPLETED:
                for item in order.items:
                    category = item.menu_item.category
                    if category not in revenue:
                        revenue[category] = 0.0
                    revenue[category] += item.get_subtotal()
        return revenue
    
    def get_top_items(self, limit: int = 5) -> List[tuple]:
        """Get top selling items"""
        item_sales = {}
        for order in self.orders.values():
            if order.status == OrderStatus.COMPLETED:
                for item in order.items:
                    name = item.menu_item.name
                    if name not in item_sales:
                        item_sales[name] = {"quantity": 0, "revenue": 0.0}
                    item_sales[name]["quantity"] += item.quantity
                    item_sales[name]["revenue"] += item.get_subtotal()
        
        sorted_items = sorted(item_sales.items(), 
                            key=lambda x: x[1]["revenue"], 
                            reverse=True)
        return sorted_items[:limit]
    
    def generate_report(self) -> Dict:
        """Generate comprehensive revenue report"""
        return {
            "total_orders": len(self.orders),
            "completed_orders": sum(1 for o in self.orders.values() if o.status == OrderStatus.COMPLETED),
            "cancelled_orders": sum(1 for o in self.orders.values() if o.status == OrderStatus.CANCELLED),
            "daily_revenue": self.get_daily_revenue(),
            "revenue_by_status": self.get_revenue_by_status(),
            "revenue_by_category": self.get_category_revenue(),
            "cash_register": self.cash_register,
            "top_items": self.get_top_items()
        }

# Example usage
if __name__ == "__main__":
    # Initialize restaurant system
    restaurant = RevenueManager()
    
    # Add menu items
    restaurant.menu.add_item(MenuItem("1", "Burger", 12.99, "Entrees", "Classic beef burger"))
    restaurant.menu.add_item(MenuItem("2", "Caesar Salad", 8.99, "Salads", "Fresh caesar salad"))
    restaurant.menu.add_item(MenuItem("3", "Pasta Carbonara", 14.99, "Entrees", "Traditional Italian pasta"))
    restaurant.menu.add_item(MenuItem("4", "Iced Tea", 3.99, "Beverages", "Refreshing iced tea"))
    restaurant.menu.add_item(MenuItem("5", "Cheesecake", 6.99, "Desserts", "New York style cheesecake"))
    
    # Display menu
    restaurant.menu.display_menu()
    
    # Create orders
    order1 = restaurant.create_order("ORD001", 1)
    order1.add_item(restaurant.menu.get_item("1"), 2)
    order1.add_item(restaurant.menu.get_item("4"), 2)
    
    order2 = restaurant.create_order("ORD002", 2)
    order2.add_item(restaurant.menu.get_item("3"), 1)
    order2.add_item(restaurant.menu.get_item("5"), 2)
    
    # Complete orders
    restaurant.complete_order("ORD001")
    restaurant.complete_order("ORD002")
    
    # Print report
    print("\n" + "="*50)
    print("RESTAURANT REVENUE REPORT")
    print("="*50)
    report = restaurant.generate_report()
    print(f"Total Orders: {report['total_orders']}")
    print(f"Completed Orders: {report['completed_orders']}")
    print(f"Daily Revenue: ${report['daily_revenue']:.2f}")
    print(f"Cash Register: ${report['cash_register']:.2f}")
    print(f"\nTop Items:")
    for item, data in report['top_items']:
        print(f"  {item}: {data['quantity']} sold - ${data['revenue']:.2f}")
    print(f"\nRevenue by Category: {report['revenue_by_category']}")