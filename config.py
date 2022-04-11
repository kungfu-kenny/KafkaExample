import os

string_range = 30
value_folder = 'analysis'
value_storage = 'storage'
value_selected = os.path.join(os.getcwd(), value_folder)
value_selected_storage = os.path.join(os.getcwd(), value_storage)

topic_test = 'message_3'#'message_test'
topic_start, topic_finish = 1,  50001
value_x = [1000, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000]