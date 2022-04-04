import json, statistics
from pprint import pprint    
from data_development import (
    check_value_file,
    value_selected_file
)

def develop_stats():
    check_value_file()
    with open(value_selected_file, "r") as file:
        k = json.load(file)
        value_list = [f.get('delta', -1) for f in k]
    value_list = [f for f in value_list if f != -1]
    
    return {
        "Maximum Value": max(value_list),
        "Minimum Value": min(value_list),
        "Mean Value of it": statistics.mean(value_list),
        "Median Value of it": statistics.median(value_list),
        "Mode Value of it": statistics.mode(value_list),
        "Length": len(value_list),
    }


if __name__ == '__main__':
    pprint(develop_stats())