import os
import json, statistics
from pprint import pprint  
import matplotlib.pyplot as plt  
from data_development import (
    merge_file_topic,
    develop_folder,
    develop_file_json,
    value_selected_file_merged,
    value_selected_file_analyzed,
    value_selected_file_plot
)
from config import (
    topic_test, 
    value_selected_storage
)


def develop_stats_delta(topic:str, delta:str):
    with open(value_selected_file_merged(topic), 'r') as file:
        value_revision = [f.get(delta, -1) for f in json.load(file)]
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

def develop_stats_plot(topic:str, delta:str):
    with open(value_selected_file_merged(topic), 'r') as file:
        value_delta = [f.get(delta, -1) for f in json.load(file)]
    value_x = [1000, 50000, 100000, 200000, 300000, 400000, 500000, 600000, len(value_delta)] #TODO change it after
    value_plot_mean = plt.scatter(
        value_x, 
        [
            statistics.mean(value_delta[:i])
            for i in value_x
        ]
    )
    
    if delta == 'delta_full':
        k = "Between send and inserting values"
    elif delta == 'delta_send':
        k = "Between sent and receive of the consumer"
    elif delta == 'delta_proccessed':
        k = "Between receive of the consumer and insert"
    
    plt.title(f'{k}: mean')
    plt.ylabel("Seconds")
    plt.xlabel("Number of elements")
    plt.close()
    
    value_plot_var = plt.scatter(
        value_x, 
        [
            statistics.variance(value_delta[:i])
            for i in value_x
        ]
    )

    plt.title(f'{k}: variance')
    plt.ylabel("Seconds")
    plt.xlabel("Number of elements")
    plt.close()

    value_plot_dev = plt.scatter(
        value_x, 
        [
            statistics.stdev(value_delta[:i])
            for i in value_x
        ]
    )

    plt.title(f'{k}: deviation')
    plt.ylabel("Seconds")
    plt.xlabel("Number of elements")
    plt.close()

    value_plot_mean.figure.savefig(value_selected_file_plot(topic, delta, 'mean'))
    value_plot_var.figure.savefig(value_selected_file_plot(topic, delta, 'variance'))
    value_plot_dev.figure.savefig(value_selected_file_plot(topic, delta, 'deviation'))

def develop_stats(topic:str):
    value_dict = {
        "Between send and inserting values": develop_stats_delta(topic, 'delta_full'),
        "Between sent and receive of the consumer": develop_stats_delta(topic, 'delta_send'),
        "Between receive of the consumer and insert": develop_stats_delta(topic, 'delta_proccessed'),
    }
    develop_file_json(     
        value_selected_file_analyzed(
            topic, 
        ),
        '1',
        value_dict
    )
    return value_dict

    
def develop_plot(topic:str):
    develop_folder(value_selected_storage)
    develop_stats_plot(topic, 'delta_full')
    develop_stats_plot(topic, 'delta_send')
    develop_stats_plot(topic, 'delta_proccessed')
    

if __name__ == '__main__':
    if not os.path.exists(value_selected_file_merged('message_2')):
        merge_file_topic('message_2')
    pprint(develop_stats('message_2'))
    develop_plot('message_2')