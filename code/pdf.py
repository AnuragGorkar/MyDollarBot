import helper
import logging
from telebot import types
from datetime import datetime
from matplotlib import pyplot as plt

def run(message, bot):
    """
    Initial function to handle the /pdf command.
    """
    try:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        options = helper.getIncomeOrExpense()
        markup.row_width = 2
        for c in options.values():
            markup.add(c)
        msg = bot.reply_to(message, 'Select Income or Expense', reply_markup=markup)
        bot.register_next_step_handler(msg, post_type_selection, bot)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, f"Error in initial setup: {str(e)}")

def post_type_selection(message, bot):
    """
    Handles the selection of Income or Expense and prompts for the date range.
    """
    try:
        chat_id = message.chat.id
        selected_type = message.text
        bot.send_message(chat_id, "Please enter the start date in yyyy-mm-dd format.")
        bot.register_next_step_handler(message, get_start_date, bot, selected_type)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, f"Error in selection: {str(e)}")

def get_start_date(message, bot, selected_type):
    """
    Prompts the user to enter the start date and validates the input.
    """
    try:
        chat_id = message.chat.id
        start_date = message.text
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            bot.send_message(chat_id, "Invalid date format. Please enter the start date in yyyy-mm-dd format.")
            bot.register_next_step_handler(message, get_start_date, bot, selected_type)
            return
        bot.send_message(chat_id, "Please enter the end date in yyyy-mm-dd format.")
        bot.register_next_step_handler(message, get_end_date, bot, selected_type, start_date_obj)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, f"Error in start date input: {str(e)}")

def get_end_date(message, bot, selected_type, start_date_obj):
    """
    Prompts the user to enter the end date, validates the input, and generates the PDF.
    """
    try:
        chat_id = message.chat.id
        end_date = message.text
        try:
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            bot.send_message(chat_id, "Invalid date format. Please enter the end date in yyyy-mm-dd format.")
            bot.register_next_step_handler(message, get_end_date, bot, selected_type, start_date_obj)
            return

        if start_date_obj > end_date_obj:
            bot.send_message(chat_id, "End date must be after the start date. Please enter the end date again.")
            bot.register_next_step_handler(message, get_end_date, bot, selected_type, start_date_obj)
            return

        user_history = helper.getUserHistory(chat_id, selected_type)
        if user_history is None or len(user_history) == 0:
            bot.send_message(chat_id, f"No records found in the specified date range.")
            return

        # Filter records within date range and generate PDF
        generate_pdf(chat_id, bot, selected_type, user_history, start_date_obj, end_date_obj)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, f"Error in end date input: {str(e)}")

def generate_pdf(chat_id, bot, selected_type, user_history, start_date_obj, end_date_obj):
    """
    Generates and sends a PDF file based on the filtered user history within the date range.
    """
    try:
        data_filtered = []
        for record in user_history:
            try:
                date_time, category, amount = record.split(",")
                date, _ = date_time.split(" ")
                record_date = datetime.strptime(date, "%d-%b-%Y")

                if start_date_obj <= record_date <= end_date_obj:
                    data_filtered.append((record_date.strftime("%Y-%m-%d"), category, amount))
            except ValueError:
                logging.warning(f"Skipping malformed record: {record}")
                continue

        if not data_filtered:
            bot.send_message(chat_id, f"No records found within the selected date range!")
            return

        # Create PDF content with matplotlib
        fig = plt.figure(figsize=(8, len(data_filtered) * 0.5 + 1))
        ax = fig.add_subplot(1, 1, 1)
        top = 0.9

        for date, category, amount in data_filtered:
            entry = f"{amount}$ {category} on {date}"
            plt.text(
                0,
                top,
                entry,
                horizontalalignment="left",
                verticalalignment="center",
                transform=ax.transAxes,
                fontsize=12,
                bbox=dict(facecolor="lightblue", alpha=0.5),
            )
            top -= 0.1

        plt.axis("off")
        pdf_filename = f"history_{chat_id}.pdf"
        plt.savefig(pdf_filename, bbox_inches="tight")
        plt.close()

        with open(pdf_filename, "rb") as pdf_file:
            bot.send_document(chat_id, pdf_file, caption=f"{selected_type} history from {start_date_obj.date()} to {end_date_obj.date()}")
    except Exception as e:
        logging.exception(str(e))
        bot.send_message(chat_id, f"An error occurred while generating the PDF: {str(e)}")
