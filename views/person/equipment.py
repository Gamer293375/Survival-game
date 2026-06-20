class Equipment:
    def __init__(self):
        self.equipment = {
            "food": 1,
            "water": 1,
            "sword": 1,
            "hammer": 0,
            "saw": 0,
            "map_piece": 0
        }

    def add_item(self, item_name, amount=1):
        if amount <= 0:
            return

        if item_name in self.equipment:
            self.equipment[item_name] += amount
        else:
            self.equipment[item_name] = amount

    def remove_item(self, item_name, amount=1):
        if amount <= 0:
            return

        if item_name not in self.equipment:
            return
        
        self.equipment[item_name] -= amount
    
    def get_items(self):
        return self.equipment.items()
    
    def has_item(self, item_name, amount=1):
        return self.equipment.get(item_name, 0) >= amount
        
    
    