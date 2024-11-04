from code import process_csv
import os
import json
import time
import csv
from telebot import types
from unittest.mock import ANY
from unittest.mock import patch

class obj:
    def __init__(self, dict1):
        self.__dict__.update(dict1)
  
def dict2obj(dict1):
    return json.loads(json.dumps(dict1), object_hook=obj)

@patch('telebot.telebot')
def test_process_csv_save_file_function(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mc.get_file.return_value=dict2obj({'file_path':'temp.csv'})
    mc.download_file.return_value=create_csv()

    message = create_message("hello from testing!")
    process_csv.save_file(message,mc)
    time.sleep(3)

    assert(os.path.isfile('./data/11_records.csv'))

@patch('telebot.telebot')
def test_process_csv_main_fucntion(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mc.get_file.return_value=dict2obj({'file_path':'temp.csv'})
    mc.download_file.return_value=create_csv()

    message = create_message("hello from testing!")
    process_csv.process_csv_file(message,mc)

    assert(mc.send_message.called)

def create_csv():
    with open('data/test_records.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["date(mm/dd/yy)","category","amount"]
        
        writer.writerow(field)
        writer.writerow(["01/01/2020", "Food", "10"])
        writer.writerow(["02/01/2020", "Groceries", "0"])
        writer.writerow(["03/01/2020", "Wrong_Category", "12"])

    with open('data/test_records.csv', 'rb') as file:    
        return file.read()
    
def create_message(text):
    params = {'messagebody': text,'document':dict2obj({'file_id':'file_id'})}
    chat = types.User(11, False, 'test')
    message = types.Message(1, None, None, chat, 'text', params, "")
    message.text = text
    
    return message

