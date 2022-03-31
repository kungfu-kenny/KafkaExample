import os
import json
import random
import string
import statistics
from uuid import uuid4
from datetime import datetime

string_range = 30
value_folder = 'analysis'
value_file = 'sent.json'
value_selected = os.path.join(os.getcwd(), value_folder)
value_selected_file = os.path.join(value_selected, value_file)

def develop_random_data(index:int=0) -> dict:
    """
    Function which is about the usage of the random data
    Input:  None
    Output: dictionary with the selected values of the random data
    """
    return {
        "index": index,
        "uuid": str(uuid4()),
        "name_person": ''.join(random.choice(string.ascii_lowercase) for _ in range(string_range)),
        "date_created": str(datetime.utcnow())
    }

def develop_folder(folder:str=value_selected):
    """
    Fucntion which is dedicated to add the creation of the
    Input:  folder = folder developed the values
    Output: we created folder
    """
    os.path.exists(folder) or os.mkdir(folder)

def check_presence_used(uuid):
    with open(value_selected_file, "r") as file:
        value_list = [f.get('uuid') for f in json.load(file)]
    return uuid in value_list

def insert_used_db(value_dict):
    with open(value_selected_file, "r") as file:
        value_list = json.load(file)
        value_list.append(value_dict)
    with open(value_selected_file, "w") as file:
        json.dump(value_list, file)

def check_value_file():
    develop_folder()
    if not os.path.exists(value_selected_file):
        with open(value_selected_file, "w") as file:
            json.dump([], file)

