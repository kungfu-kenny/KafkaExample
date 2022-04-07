import json, statistics
from pprint import pprint  
import matplotlib.pyplot as plt  
from data_development import (
    develop_folder,
    develop_file_json,
    check_value_file,
    value_selected_file,
    value_selected_file_analyzed,
    value_selected_file_plot
)
from config import (
    topic_test, 
    value_selected_storage
)


def develop_stats_delta(topic:str, delta:str):
    check_value_file(topic)
    with open(value_selected_file(topic), 'r') as file:
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
    check_value_file(topic)
    with open(value_selected_file(topic), 'r') as file:
        value_delta = [f.get(delta, -1) for f in json.load(file)]
    value_x = [10, 25, 50, 75, len(value_delta)] #TODO change it after
    value_plot_mean = plt.scatter(
        value_x, 
        [
            statistics.mean(value_delta[:i])
            for i in value_x
        ]
    )
    plt.close()
    
    value_plot_var = plt.scatter(
        value_x, 
        [
            statistics.variance(value_delta[:i])
            for i in value_x
        ]
    )
    plt.close()

    value_plot_dev = plt.scatter(
        value_x, 
        [
            statistics.stdev(value_delta[:i])
            for i in value_x
        ]
    )
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
    pprint(develop_stats('message_test'))#topic_test))
    develop_plot('message_test')#topic_test)