import re

class Sort:

    def _sort_by_condition(self, inventory_data):
        if not inventory_data:
            print("Inventory is empty, cannot sort.")
            return
        
        print('''Choose from conditions:

        1. Battle-Scarred
        2. Well-Worn              
        3. Field-Tested          
        4. Minimal Wear      
        5. Factory New 

        type (BACK) to exit!
        ''')

        _condition_map = {
            1: 'Battle-Scarred',
            2: 'Well-Worn',
            3: 'Field-Tested',
            4: 'Minimal Wear',
            5: 'Factory New'
        }
        

        while True:
            try:
                chosen_condition = input('Choose the skin condition you want (1-5) or BACK.> ')
                
                if chosen_condition.upper() == 'BACK':
                    return
                
                if chosen_condition.isdigit():
                    chosen_condition = int(chosen_condition)
                    if chosen_condition in _condition_map:
                        selected_condition = _condition_map[chosen_condition]

                        filtered_skins = [
                            item for item in inventory_data if item['Float'][0] == selected_condition
                        ]

                        if not filtered_skins:
                            print(f'No skins with {selected_condition} rarity')
                        else:
                            for i, item in enumerate(filtered_skins, start = 1):
                                print(f"{i}: Weapon: {item['Weapon']} | Skin: {item['Skin']} | Float: {item['Float']} | Rarity: [{item['Rarity']}]")      
                else:
                    continue
                    
            except ValueError: 
                print('Incorrect input!')
    

    def _sort_by_float(self, inventory_data):
        if not inventory_data:
            print("Inventory is empty, cannot sort.")
            return
        
        while True:
            try:
                selected_float = input('Choose the float value (0-1) you want to search for or BACK.> ')

                if selected_float.upper() == 'BACK':
                    return
                
                selected_float = float(selected_float)

                if not (0 <= selected_float <= 1):
                    print("Float value must be between 0 and 1. Try again.")
                    continue

            
                filtered_skins = [
                    item for item in inventory_data if abs(item['Float'][1] - selected_float) < 0.01
                ]

                if not filtered_skins:
                    print(f'No skins with float value of {selected_float}')
                else:
                    for i, item in enumerate(filtered_skins, start = 1):
                        print(f"{i}: Weapon: {item['Weapon']} | Skin: {item['Skin']} | Float: {item['Float']} | Rarity: [{item['Rarity']}]")


            except ValueError:
                print('Incorrect value! Choose a float value in the range from (0-1)')   
        

    def _sort_by_rarity(self, inventory_data, return_result = True):
        if not inventory_data:
            print("Inventory is empty, cannot sort.")
            return
        
        print('''Choose from rarity:

        1. Mil-Spec
        2. Restricted              
        3. Classified          
        4. Covert     
        5. Rare Special Item 

        type (BACK) to exit!
        ''')

        _rarity_map = {
            1: 'Mil-Spec',
            2: 'Restricted',
            3: 'Classified',
            4: 'Covert',
            5: 'Rare Special Item'
        }

        while True:
            try:
                chosen_rarity = input('Choose the skin rarity you want (1-5) or BACK.> ')

                if chosen_rarity.upper() == 'BACK':
                    return
                
                
                if chosen_rarity.isdigit():
                    chosen_rarity = int(chosen_rarity)
                    if chosen_rarity in _rarity_map:
                        selected_rarity = _rarity_map[chosen_rarity]

                        filtered_skins = [
                            item for item in inventory_data if item['Rarity'] == selected_rarity
                        ]
                        
                        reduced_list = filtered_skins[:15]

                        if not reduced_list:
                            print(f'No skins of rarity: {selected_rarity}')
                        else:
                            for i, item in enumerate(reduced_list, start = 1):
                                print(f"{i}: Weapon: {item['Weapon']} | Skin: {item['Skin']} | Float: {item['Float']} | Rarity: [{item['Rarity']}]")
                        
                        if return_result:
                            return (reduced_list, chosen_rarity, selected_rarity, _rarity_map) 
            except ValueError:
                print('Incorrect value! Choose from the available rarities.') 
            


    #This function sorts the inventory by weapon name ar skin name
    def _sort_by_key_name(self, argument, inventory_data):
        if not inventory_data:
            print("Inventory is empty, cannot sort.")
            return
        
        while True:
            search_term = input(f'Search for {argument} or BACK> ').strip().lower()
            if search_term.isdigit():
                return

            if search_term.upper() == 'BACK':
                return
            
            filtered_items = []
            if search_term.isalpha():
                for item in inventory_data:
                    key_name = item[argument].lower()
                    
                    
                    if re.findall(search_term, key_name): #this re.findall works by search a string for a first occurrence
                        filtered_items.append(item)
                        
                
                if not filtered_items:
                    print(f'No {search_term} in your inventory')
                else:
                    for i, item in enumerate(filtered_items, start = 1):
                        print(f"{i}: Weapon: {item['Weapon']} | Skin: {item['Skin']} | Float: {item['Float']} | Rarity: [{item['Rarity']}]")
            else:
                continue