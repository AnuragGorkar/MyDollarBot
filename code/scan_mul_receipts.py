import helper
import gemini_helper
import logging
from telebot import types, telebot
from datetime import datetime
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import os
from jproperties import Properties
import zipfile
from io import BytesIO
from PIL import Image

configs = Properties()

with open('user.properties', 'rb') as read_prop:
    configs.load(read_prop)

# Temporary storage for receipt data
receipt_data = {}

api_token = str(configs.get('api_token').data)
bot = telebot.TeleBot(api_token)

def run(message, bot):
    """Start receipt scanning process"""
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Please upload a zip file or multiple images of your receipts.')
    bot.register_next_step_handler(message, handle_receipt_upload, bot)

def handle_receipt_upload(message, bot):
    """Handle the receipt upload (zip file or images)"""
    try:
        chat_id = message.chat.id

        # Check if the user sent a zip file
        if message.document and message.document.file_name.endswith('.zip'):
            file_id = message.document.file_id
            file_info = bot.get_file(file_id)
            file_path = file_info.file_path
            downloaded_file = bot.download_file(file_path)

            with open(f'receipts_{chat_id}.zip', 'wb') as f:
                f.write(downloaded_file)

            process_zip_file(f'receipts_{chat_id}.zip', chat_id, bot)
            os.remove(f'receipts_{chat_id}.zip')
            return

        # Check if the user sent multiple images
        if message.photo:
            process_multiple_images(message, chat_id, bot)
            return

        bot.send_message(chat_id, 'Please send a valid zip file or multiple images of your receipts.')
        bot.register_next_step_handler(message, handle_receipt_upload, bot)

    except Exception as e:
        logging.exception("Error in handle_receipt_upload")
        bot.send_message(chat_id, f'Error processing receipts: {str(e)}')

def process_zip_file(zip_file_path, chat_id, bot):
    """Process a zip file containing receipt images"""
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            for filename in zip_ref.namelist():
                if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
                    with zip_ref.open(filename) as file_data:
                        
                        image_data = BytesIO(file_data.read())
                        image = Image.open(image_data)

                        # Convert image data to a format suitable for processing
                        result, error = gemini_helper.process_receipt_image(image)
                        if error or not result:
                            bot.send_message(chat_id, error or "Image is not a receipt.")
                            continue

                        print("Extracted data: ", result)
                        add_user_record(chat_id, {
                            'date': result['date'],
                            'amount': result['amount'],
                            'category': result['category'],
                        })

        bot.send_message(chat_id, "All receipts from the zip file have been added to the database.")

    except Exception as e:
        logging.exception("Error in process_zip_file")
        bot.send_message(chat_id, f'Error processing zip file: {str(e)}')

def process_multiple_images(message, chat_id, bot):
    """Process multiple images of receipts"""
    try:
        for photo in message.photo:
            file_id = photo.file_id
            file_info = bot.get_file(file_id)
            file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}'

            result, error = gemini_helper.process_receipt_image(file_url)
            if error or not result:
                bot.send_message(chat_id, error or "Image is not a receipt.")
                continue

            print("Extracted data: ", result)
            add_user_record(chat_id, {
                'date': result['date'],
                'amount': result['amount'],
                'category': result['category'],
            })

        bot.send_message(chat_id, "All receipts have been added to the database.")

    except Exception as e:
        logging.exception("Error in process_multiple_images")
        bot.send_message(chat_id, f'Error processing images: {str(e)}')

def add_user_record(chat_id, record_to_be_added):
    user_list = helper.read_json()
    
    # If user is not in the list, create a new record
    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = helper.createNewUserRecord()
    
    original_date = datetime.strptime(record_to_be_added['date'], "%Y-%m-%d")
    formatted_date = original_date.strftime("%d-%b-%Y 00:00")
    upload_string = f'{formatted_date},{record_to_be_added["category"]},{record_to_be_added["amount"]}' 

    # Append the new record to the user's data
    user_list[str(chat_id)]['data'].append(upload_string)
    
    # Write the updated data back to JSON
    helper.write_json(user_list)
    
    msg_text = (
            "Added successfully! to the database.\n"
            "Receipt Details:\n"
            f"Date: {record_to_be_added['date']}\n"
            f"Amount: {record_to_be_added['amount']:.2f}\n"
            f"Category: {record_to_be_added['category']}"
        )
    bot.send_message(chat_id, msg_text)

    return user_list