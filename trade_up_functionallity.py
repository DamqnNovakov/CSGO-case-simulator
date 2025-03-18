import CONSTS
import random

from inventory import Inventory
from sorting_inventory import Sort
from cases import cases
from utils import update_json, float_generator
from pricing_skin_system import SkinPricer

class TradeUps:
    def __init__(self):
        self._cases = cases
        self._inventory = Inventory()
        self._rarity_sort = Sort()
        self._skin_pricer = SkinPricer()
    
  
    def _trade_up_functionality(self):
        print(f'''{' '*45}⬆ Trade Up Section ⬆\nYour Inventory''')
        #Reusing the _load_inventory function 

        self._inventory_data = self._inventory._load_inventory()
        self._inventory._display_inventory()
        print('\n')
        
        #Reusing the rarity filtering 
        filtered_skins, chosen_rarity, selected_rarity, rarity_map = self._rarity_sort._sort_by_rarity(self._inventory_data, return_result = True)
    
        #Checks in the rarity_map to provide higher rarity for the trade up excluding covert and rare special items since they can not be traded up .
        if chosen_rarity + 1 < 4:
            upper_rarity = rarity_map[chosen_rarity + 1]
        else:
            print(f'You can not trade up items from {CONSTS.RED}{rarity_map[3]}{CONSTS.RESET} or {CONSTS.YELLOW}{rarity_map[4]}{CONSTS.RESET}')
            return
        
        # Picking 3 skins for the trade up in this while loop
        print(f'\nYou need to choose 3 skins from a {CONSTS.RED}{selected_rarity}{CONSTS.RESET} to trade them for a skin from {CONSTS.GREEN}{upper_rarity}{CONSTS.RESET}!\n')

        picked_skins = []
        while len(picked_skins) < 3:
            pick_skin = int(input('Choose the skins you want to trade up> '))
            
            #Rendering the filtered list and choosing items to trade up
            for i, item in enumerate(filtered_skins, start = 1):  
                if pick_skin == i :
                    picked_skins.append(item)
                    print(f"\r{i}: Weapon: {item['Weapon']} | Skin: {item['Skin']} | Float: {item['Float']} | Rarity: [{item['Rarity']}] successfully added in the trade up!\n")
                    continue

                if len(picked_skins) == 3:
                    break

        print('\nYou picked 3 skins to trade up!\n')
        for i, item in enumerate(picked_skins, start = 1):
            print(f"{i}: Weapon: {item['Weapon']} | Skin: {item['Skin']} | Float: {item['Float']} | Rarity: [{item['Rarity']}]")

                
        print(f'   \nOptions\n1. Trade up to {CONSTS.GREEN}{upper_rarity.upper()}{CONSTS.RESET}\n2. Go Back\n')
        while True:
            try:
                option = int(input('Choose from the options> '))
                if option not in [1, 2]:
                    break
                print("Choose from the options (1-2)!")
            except ValueError:
                print("Invalid input! Please enter a number.")

            if option == 1:
                skin_condition, float_val = float_generator()
                self.remove_items_from_inventory(picked_skins)

                random_case = random.choice(list(self._cases.values()))
                rarity = list(random_case[upper_rarity].items())
                skin_won = random.choice(rarity)
                
                traded_up_skin = {
                    'Weapon': skin_won[0],
                    'Skin': skin_won[1],
                    'Float': [skin_condition, float_val],
                    'Rarity': upper_rarity 
                }

                self._inventory_data.append(traded_up_skin)
                self._skin_pricer.activate_skin_pricing(self._inventory_data)

                update_json(CONSTS.INVENTORY_FILENAME, self._inventory_data)
                
                print(f"{CONSTS.GREEN}🎉 Congrats! You traded up to:{CONSTS.RESET}")
                print(f"{CONSTS.YELLOW} Weapon:  {skin_won[0]} | Skin: {skin_won[1]} | Rarity: {upper_rarity}{CONSTS.RESET}")

            elif option == 2:
                break
            else:
                print('Choose from the options(1-2)!')
                continue
    
    # This function check for the
    def remove_items_from_inventory(self, picked_skins):
        picked_floats = {item['Float'][1] for item in picked_skins}
    
        # Filter out items with matching float values
        self._inventory_data = list(filter(lambda item: item['Float'][1] not in picked_floats, self._inventory_data))
        update_json(CONSTS.INVENTORY_FILENAME, self._inventory_data)
       
        
    def start_trade_up(self):
        return self._trade_up_functionality()
    
               


            
                        



        

        