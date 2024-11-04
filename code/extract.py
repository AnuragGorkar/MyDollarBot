import helper
import logging
from telegram import InputFile
from telebot import types
import csv
import os

# The main funtion of category.py.
# User can start to manage their categories after calling it
def run(message, bot):
    try:
        chat_id = message.chat.id
        user_history = helper.getUserExpenseHistory(chat_id)
        if not user_history:
            bot.send_message(chat_id, "no data to generate csv")
            return None
        
        else:   
            file_path = 'code/data.csv'
            rows = [line.split(',') for line in user_history]
            column_names = ['Date and Time', 'Category', 'Amount']
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(column_names)
                writer.writerows(rows)
                
            # Send the file to the user
            with open(file_path, 'rb') as file:
                bot.send_document(chat_id, document=file)
                return file_path
            # os.remove(file_path)    
    except Exception as e:
        logging.error(str(e))
