import os
import json
from pprint import pprint
import random
import string
from uuid import uuid4
from datetime import datetime
from config import(
    string_range,
    topic_test,
    value_selected,
    value_selected_storage
)


def value_selected_file(x):
    return os.path.join(
        value_selected, 
        f"sent_{x}_{datetime.utcnow().strftime('%Y_%m_%d_%H')}_{int(datetime.utcnow().strftime('%M'))}.json"
    )

def value_selected_file_merged(x):
    return os.path.join(
        value_selected,
        f"sent_{x}_merged.json"
    )

def value_selected_file_check(x):
    return os.path.join(
        value_selected, 
        f"check_{x}_{datetime.utcnow().strftime('%Y_%m_%d_%H')}_{int(datetime.utcnow().strftime('%M'))}.json"
    )

def value_selected_file_analyzed(x):
    path = os.path.join(value_selected, f"analyzed_{x}.json")
    if os.path.exists(path):
        os.remove(path)
    return path

def value_selected_file_plot(topic:str, delta:str, name:str) -> str:
    return os.path.join(value_selected_storage, f"{topic}_{delta}_{name}.png")

def develop_file_json(file_path:str, value_check:bool=True, value_use:object=None) -> None:
    """
    Function which is dedicated for checking files
    Input:  file_path = file of the json values
            value_check = check parameter for the
    Output: we created files if have to
    """
    if not os.path.exists(file_path):    
        if value_check == True:
            value_use = [] 
        elif value_check == False: 
            value_use = {}
        with open(file_path, "w") as file:
            json.dump(
                value_use, 
                file,
                indent=4
            )

def develop_file_check(topic:str, value_uuid:str) -> bool:
    """
    Function which is dedicated to check values
    Input:  topic = topic which we are used and search of the file
            value_uuid = uuid which shows values
    Output: boolean value to get it
    """
    with open(value_selected_file_check(topic), 'r') as json_file:
        value_dict = json.load(json_file)
    return value_dict.get(value_uuid, False)

def develop_file_check_new(topic:str, value_uuid:str) -> bool:
    """
    Function which is dedicated to check presence
    Input:  topic = topic path value which could be used
            value_uuid = uuid value which is searched 
    Output: we inserted values
    """
    check_value_file(topic)
    value_elements = [f for f in os.listdir(value_selected) if f'check_{topic}_' in f]
    for files in value_elements:
        with open(os.path.join(value_selected, files), 'r') as json_file:
            if json.load(json_file).get(value_uuid, False):
                return True
    return False

def develop_file_insert(value_file:dict, value_bool:bool=True, topic:str=topic_test) -> None:
    """
    Function which is about the insertion values
    Input:  value_path = path of the selected file
            value_file = dictionary to develop
            value_bool = boolean value to develop append or update
    Output: we inserted values of the 
    """
    value_path = value_selected_file(topic) if value_bool else value_selected_file_check(topic)
    if not os.path.exists(value_path):
        value_dict = [value_file] if value_bool else value_file
        with open(value_path, 'w') as write:
            json.dump(
                value_dict, 
                write, 
                indent=4
            )
        return
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

def check_value_file(topic:str) -> None:
    """
    Function which is dedicated to develop value files in cases of the absence
    Input:  value_selected_file = value file where to store selected values
            value_selected_check = value file where to stor checked values
    Output: we developed previously required files
    """
    develop_folder() 
    develop_file_json(value_selected_file(topic), True)
    develop_file_json(value_selected_file_check(topic), False)

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
        "date_created": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
    }

def develop_folder(folder:str=value_selected):
    """
    Fucntion which is dedicated to add the creation of the
    Input:  folder = folder developed the values
    Output: we created folder
    """
    os.path.exists(folder) or os.mkdir(folder)

def merge_file_topic(topic:str) -> None:
    """
    Function which is dedicated to merge the topic files into one
    Input:  topic = string with the topic which is used
    Output: we merged all possible values
    """
    value_search_types = ['check', 'sent']
    for types in value_search_types:
        value_files = [
            k for k in os.listdir(value_selected) 
            if f"{types}_{topic}_" in k 
            and (k.replace(f"{types}_{topic}_", '').split('_')[0].isalnum()
            and len(k.replace(f"{types}_{topic}_", '').split('_')[0]) == 4) 
            or k.replace(f"{types}_{topic}_", '').split('_')[0] == 'merged.json'
        ]
        if types == 'check':
            result = {}
        elif types == 'sent':
            result = []
        for f in value_files:
            with open(os.path.join(value_selected, f), "r") as infile:
                if types == 'check':
                    result.update(json.load(infile))
                elif types == 'sent':
                    result.extend(json.load(infile))
        with open(os.path.join(value_selected, f"{types}_{topic}_merged.json"), "w") as outfile:
            json.dump(result, outfile, indent=4)
        for f in value_files:
            if '_merged.json' not in f:
                os.remove(os.path.join(value_selected, f))
        print('We merged files:', types)

if __name__ == '__main__':
    merge_file_topic(topic_test)