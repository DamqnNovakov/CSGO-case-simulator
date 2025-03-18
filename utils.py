import os
import json
import random
import CONSTS

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def update_json(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent = 4)

def float_generator():
    float_num = random.random()
    if CONSTS.LOW_FACTORY_NEW < float_num < CONSTS.HIGH_FACTORY_NEW_LOW_MINIMAL_WEAR:
        return 'Factory New', float_num
    elif CONSTS.HIGH_FACTORY_NEW_LOW_MINIMAL_WEAR < float_num < CONSTS.HIGH_MINIMAL_WEAR_LOW_FIELD_TESTED:
        return 'Minimal Wear', float_num
    elif CONSTS.HIGH_MINIMAL_WEAR_LOW_FIELD_TESTED < float_num < CONSTS.HIGH_FIELD_TESTED_LOW_WELL_WORN:
        return 'Field-Tested', float_num
    elif CONSTS.HIGH_FIELD_TESTED_LOW_WELL_WORN < float_num < CONSTS.HIGH_WELL_WORN:
        return 'Well-Worn', float_num
    else:
        return 'Battle-Scarred', float_num