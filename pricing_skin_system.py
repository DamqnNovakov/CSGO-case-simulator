class SkinPricer:
    def __init__(self, rarity = None, condition = None):
        self._rarity = rarity
        self._condition = condition
        self._skin_price = 0


    # Sets a price on every item in inventory based on its rarity and increase or decrease this price depending on the condition factor
    def _skin_pricing(self, inventory_data):
        _inventory = inventory_data

        _price_by_rarity = {
            'Mil-Spec' : 0.50,
            'Restricted' : 2,
            'Classified' : 5,
            'Covert' : 20,
            'Rare Special Item': 300
        } 

        _price_manipulation_by_condition = {
            'Battle-Scarred' : 0.5,
            'Well-Worn' : 0.8,
            'Field-Tested' : 1,
            'Minimal Wear' : 1.4,
            'Factory New' : 2
        }
         
        for item in _inventory:
            if 'Rarity' not in item or 'Float' not in item:
                print("Missing 'Rarity' or 'Float' in item:", item)
                continue  

            self._rarity = item['Rarity']
            self._condition = item['Float'][0]
            if self._rarity in _price_by_rarity and self._condition in _price_manipulation_by_condition:
                item_price = _price_by_rarity[self._rarity]
                condition_factor = _price_manipulation_by_condition[self._condition]
                self._skin_price = float(item_price) * float(condition_factor)
                item['Price'] = self._skin_price

            else:
                print('Can not set a price on this skine')  

        return self._skin_price
    
    def activate_skin_pricing(self, inventory_data):
        return self._skin_pricing(inventory_data)


        