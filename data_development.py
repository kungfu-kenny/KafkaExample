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
value_file_check = 'check.json'

value_selected = os.path.join(os.getcwd(), value_folder)
value_selected_file = os.path.join(value_selected, value_file)
value_selected_check = os.path.join(value_selected, value_file_check)

def develop_file_json(file_path:str, value_check:bool=True) -> None:
    """
    Function which is dedicated for checking files
    Input:  file_path = file of the json values
    Output: we created files if have to
    """
    if not os.path.exists(file_path):    
        value_use = [] if value_check else {}
        with open(file_path, "w") as file:
            json.dump(
                value_use, 
                file,
                indent=4
            )

def develop_file_check(value_uuid:str) -> bool:
    """
    Function which is dedicated to check values
    Input:  value_uuid = uuid which shows values
    Output: boolean value to get it
    """
    with open(value_selected_check, 'r') as json_file:
        value_dict = json.load(json_file)
    return value_dict.get(value_uuid, False)

def develop_file_insert(value_file:dict, value_bool:bool=True) -> None:
    """
    Function which is about the insertion values
    Input:  value_path = path of the selected file
            value_file = dictionary to develop
            value_bool = boolean value to develop append or update
    Output: we inserted values of the 
    """
    value_path = value_selected_file if value_bool else value_selected_check
    with open(value_path, 'r') as read:
        value_dict = json.load(read)
    if value_bool:
        value_dict.append(value_file)
    else:
        value_dict.update(value_file)
    with open(value_path, 'w') as write:
        json.dump(
            value_dict, 
            write, 
            indent=4
        )

def check_value_file() -> None:
    """
    Function which is dedicated to develop value files
    Input:  None
    Output: we developed previously required files
    """
    develop_folder() 
    develop_file_json(value_selected_file, True)
    develop_file_json(value_selected_check, False)

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