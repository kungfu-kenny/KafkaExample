import json, statistics
from pprint import pprint    
from data_development import (
    check_value_file,
    value_selected_file
)


def develop_stats_relative():
    check_value_file()
    with open(value_selected_file, 'r') as file:
        value_delta = [f.get('delta', -1) for f in json.load(file)]
    value_revision = [value_delta[0]]
    for value_old, value_new in zip(value_delta[:-1], value_delta[1:]):
        value_revision.append(value_new-value_old)
    return {
        "Maximum Value": max(value_revision),
        "Minimum Value": min(value_revision),
        "Mean Value of it": statistics.mean(value_revision),
        "Median Value of it": statistics.median(value_revision),
        "Mode Value of it": statistics.mode(value_revision),
        "Standard Deviation Value of it": statistics.stdev(value_revision),
        "Variance": statistics.variance(value_revision),
        "Length": len(value_revision),
    }

def develop_stats_absolute():
    check_value_file()
    with open(value_selected_file, "r") as file:
        value_list = [f.get('delta', -1) for f in json.load(file)]
    value_list = [f for f in value_list if f != -1]
    return {
        "Maximum Value": max(value_list),
        "Minimum Value": min(value_list),
        "Mean Value of it": statistics.mean(value_list),
        "Median Value of it": statistics.median(value_list),
        "Mode Value of it": statistics.mode(value_list),
        "Standard Deviation Value of it": statistics.stdev(value_list),
        "Variance": statistics.variance(value_list),
        "Length": len(value_list),
    }

def develop_stats():
    return {
        "Absolute Parameters": develop_stats_absolute(),
        "Relative Delta Parameters": develop_stats_relative(),
    }


if __name__ == '__main__':
    pprint(develop_stats())