import json
import CONSTS

from sorting_inventory import Sort
from pricing_skin_system import SkinPricer
from wallet import Wallet
from utils import clear_console, update_json

class Inventory:
    def __init__(self):
        self._skin_pricer = SkinPricer()
        self._wallet = Wallet()
        self._sort_instance = Sort()
        self._inventory_data = []
        self._current_index_of_items = 0
        self._total_inventory_value = 0
        self._total_items = 0
        

    def _save_in_inventory(self, random_weapon, random_skin, skin_condition, float_value, rarity):
        if random_weapon is None or random_skin is None:
            print("No skin won yet. Open a case first!")
            return
         
        try:
            with open(CONSTS.INVENTORY_FILENAME, 'r') as file:
                if file.read().strip():
                    file.seek(0)
                    self._inventory_data = json.load(file)
                else:
                    self._inventory_data = []
        except FileNotFoundError:
            print('No inventory existed!')
    
        skin_data = {
            'Weapon': random_weapon,
            'Skin': random_skin,
            'Float': [skin_condition, float_value],
            'Rarity': rarity 
        }
        
        self._inventory_data.append(skin_data)

        update_json(CONSTS.INVENTORY_FILENAME, self._inventory_data)
        
        print('Skin saved in Inventory')



    def _load_inventory(self):
        try:
            with open(CONSTS.INVENTORY_FILENAME, 'r') as file:
                if file.read().strip():
                    file.seek(0)
                    self._inventory_data = json.load(file)
                else:
                    self._inventory_data = []

        except FileNotFoundError:
            print('No inventory file found!')
            self._inventory_data = []

        self._skin_pricer.activate_skin_pricing(self._inventory_data) # This updates prices in _inventory_data

        update_json(CONSTS.INVENTORY_FILENAME, self._inventory_data)

        return self._inventory_data
    
    def _delete_from_inventory(self):
        self._inventory_data = self._load_inventory()
        del_item = input('\nChoose which item you want to delete or q to quit!> ').upper()
        

        if del_item.isdigit():
            del_item = int(del_item) - 1
            if 0 <= del_item < len(self._inventory_data):
                removed_item = self._inventory_data.pop(del_item)
                print('\n' * 2)
                print(f':{removed_item} successfully removed!')

                update_json(CONSTS.INVENTORY_FILENAME, self._inventory_data)
                
                print('Inventory was updated')
            else:
                print('Invalid index! Please insert a valid one.')       
        elif del_item.isalpha() and del_item == 'Q':
            return
        
    def _display_inventory(self):
        self._load_inventory()

        print(f'{'='* 110}')
        if not self._inventory_data:
            print('Your inventory in empty\n')
        else: 
            # current_items = self._load_more_items()
            for i, item in enumerate(self._inventory_data, start = 1):
                print(f"{i}: Weapon: {item['Weapon']} | Skin: {item['Skin']} | Float: {item['Float']} | Rarity: [{item['Rarity']}] | 'Price: [{item['Price']}$]'")

    # def _load_more_items(self):  
    #     pulled_items = 20
    #     total_items = len(self._inventory_data)

    #     if self._current_index_of_items + pulled_items <= total_items:
    #         current_items = list(islice(self._inventory_data, self._current_index_of_items, self._current_index_of_items + pulled_items))
    #         self._current_index_of_items += pulled_items
    #         return current_items
    #     else: 
    #         print('No more items in the inventory!')
    #         return []

    #This function sum the total items and value of the inventory items
    def _total_inventory_items_and_value_func(self):
        self._inventory_data = self._load_inventory()
        total_inventory_value = 0  
        
        for item in self._inventory_data:
            total_inventory_value += item.get('Price', 0)
        self._total_items = len(self._inventory_data)
        self._total_inventory_value = total_inventory_value
           

    def _display_inventory_menu(self):
        self._total_inventory_items_and_value_func()
        while True:
            print(f'''Menu:
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
| 1. Sort by Condition | 2. Sort by Float | 3. Sort by Rarity | 4. Sort by Weapon name | 5. Sort by Skin name | 6. Delete skin | 7. Selling skins  | 8. Go Back |
-----------------------------------------------------------------------------------------------------------------------------------------------------------------\n
Total skins [{self._total_items}]
Total inventory value [{CONSTS.GREEN}{self._total_inventory_value}${CONSTS.RESET}]''')
            print(f"\n{' '*45}Inventory\n")
            self._display_inventory()
            print('\n9. Load more....')
        
        
            menu_option = int(input('\nChoose from the menu> '))
            if menu_option == 1:
                self._sort_instance._sort_by_condition(self._inventory_data)
                clear_console()
                continue
            elif menu_option == 2:
                self._sort_instance._sort_by_float(self._inventory_data)
                clear_console()
                continue
            elif menu_option == 3:
                self._sort_instance._sort_by_rarity(self._inventory_data, return_result = False)
                clear_console()
                continue
            elif menu_option == 4:
                self._sort_instance._sort_by_key_name('Weapon', self._inventory_data)
                clear_console()
                continue
            elif menu_option == 5:
                self._sort_instance._sort_by_key_name('Skin', self._inventory_data)
                clear_console()
                continue
            elif menu_option == 6:
                self._delete_from_inventory()
                clear_console()
                continue
            elif menu_option == 7:
                self._wallet._selling_skins_for_money(self._inventory_data)
                clear_console()
                continue
            elif menu_option == 8:
                clear_console()
                return
            # elif menu_option == 9:
            #     self._load_more_items()
            #     self._display_inventory()
            else:
                print('Invalid option!')

    