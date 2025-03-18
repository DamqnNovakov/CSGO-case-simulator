import random
import time
import CONSTS

from cases import cases
from inventory import Inventory
from trade_up_functionallity import TradeUps
from utils import clear_console, float_generator
from wallet import Wallet


class CaseSimulator:
    _rarity_probability = {
        "Rare Special Item": CONSTS.RARE_SPECIAL_ITEM,  
        "Covert": CONSTS.COVERT,               
        "Classified": CONSTS.CLOASSIFIED,           
        "Restricted": CONSTS.RESTRICTED,       
        "Mil-Spec": CONSTS.MIL_SPEC, 
    }

    def __init__(self):
        self._case = None
        self._rarity = None 
        self._random_weapon = None
        self._random_skin = None
        self._skin_condition = None
        self._float_value = None
        self._inventory = Inventory()
        self._trade_up = TradeUps()
        self._wallet = Wallet()

    def _choose_case(self):
    
        while True:
            case_available = 0
            print('''           🔥Choose Case🔥\n''')
            print("\n| No | Case Name              | Price |")
            print("|----|------------------------|-------|")
            for i, case_name in enumerate(cases.keys()):
                case_available += 1
                price = case_name[1]
                print(f"| {str(i + 1).ljust(2)} | {case_name[0].ljust(22)} | ${price:.2f} |")   
            
            choose_case = input(f'\nChoose a case to open (1-{case_available})> ')

            if choose_case.isalpha():
                clear_console()
                print('Please choose from available cases!\n')
                continue

            choose_case = int(choose_case) - 1
            if 0 <= choose_case < len(cases):
                case_name = list(cases.keys())[choose_case]
                self._case = cases[case_name]
                print("="*39)
                print(f"{' '*6}You chose {case_name[0]}\n\nCosts per case -{case_name[1]}$")
                print("="*39)
                return case_name
            else:
                clear_console()
                print('No such case exists yet. Try again!\n')
                continue

    def _opening(self):
        rarities = list(self._rarity_probability.keys())
        probabilities = list(self._rarity_probability.values())
        selected_rarity = random.choices(rarities, weights=probabilities, k=1)[0]
        self._rarity = selected_rarity
        self._skin_condition, self._float_value = float_generator()

        for rarity, skins in self._case.items():
            if rarity == selected_rarity:
                self._random_weapon, self._random_skin = random.choice(list(skins.items()))

        return self._random_weapon, self._random_skin
    

    def _winning(self):
        self._random_weapon, self._random_skin = self._opening()
        self._display_case_results(self._random_weapon, self._random_skin, self._skin_condition)

        self._inventory._save_in_inventory(self._random_weapon, self._random_skin, self._skin_condition, self._float_value, self._rarity)


    def _display_case_results(self, random_weapon, random_skin, skin_condition):
        print("===============================================")
        print(f"           🎉 CASE OPENING! 🎉")
        print("-" * 47)
        

        rolling_case = [(weapon, skin) for _ , skins in self._case.items() for weapon, skin in skins.items()]

        random.shuffle(rolling_case)

        for i in range(len(rolling_case) * 3):
            weapon, skin = rolling_case[i % len(rolling_case)]
            print(f"Rolling... {weapon} | {skin}")
            time.sleep(0.2)


        print("\n===============================================")
        print(f"           🎉 CONGRATULATIONS! 🎉")
        print(f"\nYou won a skin from the case!")
        print("-"*47)
        print(f"Weapon:    {random_weapon}")
        print(f"Skin:      {random_skin}")
        print(f"Condition: {skin_condition}")
        print("===============================================")

    def action(self):
        clear_console()
        while True:
            acc_balance, _ = self._wallet._show_balance()

            print("=" * 35)
            print(f"💰{acc_balance}".center(45))
            print("=" * 35)

            print(f"        CSGO Case Simulator\n\n1. Open cases!\n2. Inventory\n3. Trade up\n4. FREE Money\n5. Quit")
            action = int(input('\nChoose option (1-3)> '))
            
            clear_console()

            if action == 1:
                
                case_name = self._choose_case()
                while True:
                    option = input('Press ENTER to open or Q to quit!').strip().lower()
                    _, balance = self._wallet._show_balance()
                    if option == 'q':
                        clear_console()
                        break
                    else:
                        clear_console()
                        chosen_case_price = case_name[1]
                        if balance - chosen_case_price <= 0:
                            print(f'Limited balance amount: {CONSTS.GREEN}{balance:.2f}${CONSTS.RESET}\n')

                            print('1. Make money\n2. Go back\n')
                            while True:
                                option = input('Make free money -> 1 or Go back -> 2 > ')
                                if option.isalpha():
                                    print('Please choose from the options!')
                                    continue

                                option = int(option)
                                if option == 1:
                                    self._wallet._gain_balance_by_clicking() 
                                elif option == 2:
                                    break
                                else:
                                    print('Please choose from the options!')
                                    continue
                        else:
                            self._wallet._remove_balance(chosen_case_price)
                            self._winning()
                            continue
            elif action == 2:
                self._inventory._display_inventory_menu()
            elif action == 3:
                self._trade_up.start_trade_up()
            elif action == 4:
                self._wallet._gain_balance_by_clicking()
            elif action == 5:
                break
            else:
                print('Choose from the options')
                continue

# if __name__ == "__main__":
#     case = CaseSimulator()
#     case.action()