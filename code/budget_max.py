import helper
import logging
from telebot import types

def run(message, bot):
    chat_id = message.chat.id
    if helper.isMaxTransactionLimitAvailable(chat_id):
        maxLimit = helper.getMaxTransactionLimit(chat_id)
        msg_string = 'Current Limit is ${}\n\nHow much is your new Max limit per transaction? \n(Enter numeric values only)'
        message = bot.send_message(chat_id, msg_string.format(maxLimit))
    else:
        message = bot.send_message(chat_id, 'How much is your new Max limit per transaction? \n(Enter numeric values only)')
    bot.register_next_step_handler(message, post_max_budget, bot)

def post_max_budget(message, bot):
    try:
        chat_id = message.chat.id
        amount_value = helper.validate_entered_amount(message.text)
        if amount_value == 0:
            raise Exception("Invalid amount.")
        user_list = helper.read_json()
        if str(chat_id) not in user_list:
            user_list[str(chat_id)] = helper.createNewUserRecord()
        user_list[str(chat_id)]['budget']['max_per_txn_spend'] = amount_value
        helper.write_json(user_list)
        bot.send_message(chat_id, 'Max Limit Updated!')
        print('deb: ')
        print(user_list)
        return user_list
    except Exception as e:
        helper.throw_exception(e, message, bot, logging)