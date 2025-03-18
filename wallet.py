import json
import sys
import random
import CONSTS
import keyboard # type: ignore
from typing import Any

from utils import clear_console, update_json


class Wallet:
    def __init__(self):
        self._balance = 0


    def _gain_balance_by_clicking(self):   
        self._load_balance()
    
        print(f"{' '*15}🎉 {CONSTS.GREEN}FREE{CONSTS.RESET} Money!\n{' '*17}{'='*12}\nPress 'SPACE' to earn free balance. Press 'ESC' to go back.\n{'='*58}""")
        
        space_pressed = False
        clicks = 0

        while True:
            event = keyboard.read_event()

            if event.event_type == keyboard.KEY_DOWN and event.name == "space" and not space_pressed:
                space_pressed = True
                clicks += 1
                self._balance += CONSTS.ADDITIONAL_BALANCE

                # BONUS chance (1 in 50 chance)
                if random.randint(1, 50) == 1:
                    self._balance += CONSTS.ADDITIONAL_BINUS_ON_50_KLICKS
                    print(f"\n🎉 BONUS! You earned an extra {CONSTS.GREEN}1,00${CONSTS.RESET}! 🎉")
                
                # BONUS chance (1 in 200 chance)
                if random.randint(1, 200) == 1:
                    self._balance += CONSTS.ADDITIONAL_BINUS_ON_200_KLICKS
                    print(f"\n🎉 BONUS! You earned an extra {CONSTS.GREEN}5,00${CONSTS.RESET}! 🎉")

                if random.randint(1, 500) == 1:
                    # Need to add functionallity for a chance of entering a game to win more additional balance
                    pass

                sys.stdout.write(f"\r💰 Balance: {self._balance:.2f}$ <-- + {CONSTS.GREEN}{CONSTS.ADDITIONAL_BALANCE}${CONSTS.RESET} ")  # Updates balance on the same line
                sys.stdout.flush()  # Ensure it gets printed immediately               
                self._save_balance()
                
            elif event.event_type == keyboard.KEY_UP:
                space_pressed = False
                continue      
            elif event.name == 'esc':
                clear_console() 
                print(f'Your new balance is {CONSTS.GREEN}{self._balance:.2f}${CONSTS.RESET}')
                return  
                                                                                                                                                                                               
                        
    def _save_balance(self): 
        if self._balance is None:
            print('No balance available!')
            return                                                                                            

        try:
            update_json(CONSTS.WALLET_FILENAME, {"balance": round(self._balance, 2)})
        except Exception as e:
            print(f"Error saving balance: {e}")


    def _load_balance(self):
        try:
            with open(CONSTS.WALLET_FILENAME, 'r') as file:
                data = json.load(file)
                self._balance = data.get("balance", 0)
                return self._balance
        except FileNotFoundError:
            print('No balance found!')   


    def _add_balance(self, amount):
        self._load_balance()     
        self._balance += amount
        self._save_balance()  

    def _remove_balance(self, amount):
        self._load_balance()     
        self._balance -= amount
        self._save_balance() 


    def _show_balance(self):
        self._load_balance()
        return (f'Balance: {CONSTS.GREEN}{self._balance:.2f}${CONSTS.RESET}\n\n'), self._balance


    def _selling_skins_for_money(self, inventory_data):
        if not inventory_data:
            print("Inventory is empty, cannot sell.")
            return
        

        while True:
            try:
                chosen_item = input("Choose an item to SELL  or go 'BACK'> ")
                
                if chosen_item.upper() == 'BACK':
                    return
               
                if chosen_item.isdigit():
                    chosen_item = int(chosen_item) 
                    if 0 < chosen_item <= len(inventory_data):
                        item = inventory_data[chosen_item - 1]         
                        price = item.get('Price', 0)
                        self._add_balance(price)
                        print(f"""Weapon: {item['Weapon']} | Skin: {item['Skin']} | Float: {item['Float']} | Rarity: [{item['Rarity']}] | 'Price: [{item['Price']}$]\n Item successfully sold!\n{item['Price']}$ added to your balance'""")
                        inventory_data.pop(chosen_item - 1)

                        update_json(CONSTS.INVENTORY_FILENAME, inventory_data)
                      
                else:
                    print(f'Choose in item from (1-{int(len(inventory_data))})') 
                    continue   
            except ValueError:
                print('Invalid value! Please enter a number.')
                


    
   
