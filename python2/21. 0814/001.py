class ShoppingCart:
    
    def __init__(self):
        self.items = {}
        self.total = 0  # 총매출

    def add_item(self, item_id, name, price, quantity=1):
        
        if item_id in self.items:
            self.items[item_id]['quantity'] += quantity
        else:
            self.items[item_id] = {
                'name':name,
                'price':price,
                'quantity':quantity
            }
        self.calculate_total()

    def remove_item(self, item_id, quantity=1):
        
        if item_id in self.items:
            self.items[item_id]['quantity'] -= quantity
            if self.items[item_id]['quantity'] <= 0:
                del self.items[item_id]
            self.calculate_total()

    def calculate_total(self):
        self.total = sum(item['price'] * item['quantity'] for item in self.items.values())

    def apply_discount(self, percent):
        self.total *= (1 - (percent/100))