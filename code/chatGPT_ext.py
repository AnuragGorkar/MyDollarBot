import helper
from hugchat import hugchat
from hugchat.login import Login


def run(message, bot):
    helper.read_json()
    chat_id = message.chat.id
    history = helper.getUserExpenseHistory(chat_id)

    if history is None:
        bot.send_message(chat_id, "Sorry, there are no records of the spending!")
    else:
        bot.send_message(chat_id, "Hi, I am your AI finance assistant. I can help you with your spendings and "
                                  "budgeting. Please type 'exit' to stop chatting with me.")
        # added by Jay for chatbot integration
        sign = Login('airtelbharti9004@gmail.com', 'J@yesh17598')
        cookies = sign.login()
        # Save cookies to the local directory
        cookie_path_dir = "./cookies_snapshot"
        sign.saveCookiesToDir(cookie_path_dir)
        # Create a chatbot connection
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        # New a conversation (ignore error)
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
        bot.register_next_step_handler(message, run_display, bot, chatbot)


def run_display(message, bot, chatbot):
    helper.read_json()
    chat_id = message.chat.id
    user_input = message.text
    user_history = helper.getUserExpenseHistory(chat_id)

    # get history of user
    spend_total_str = ""
    # Amount for each month
    Dict = {'Jan': 0.0, 'Feb': 0.0, 'Mar': 0.0, 'Apr': 0.0, 'May': 0.0, 'Jun': 0.0, 'Jul': 0.0, 'Aug': 0.0,
            'Sep': 0.0, 'Oct': 0.0, 'Nov': 0.0, 'Dec': 0.0}

    if user_input == 'exit':
        bot.send_message(chat_id, 'Nice talking to you. Happy Finance!')
        return

    history_strings = []

    for rec in user_history:
        history_strings.append(str(rec))
        av = str(rec).split(",")
        ax = av[0].split("-")
        am = ax[1]
        Dict[am] += float(av[2])

    # get history of user
    query = '''Consider below monthly expense and give me a response to my query based on it.\n'''
    spend_total_str = '\n'.join(history_strings)
    user_input = query + spend_total_str + ' ' + user_input

    # Generate a response from ChatGPT
    try:
        response = str(chatbot.chat(user_input))
        bot.send_message(chat_id, response)
        bot.register_next_step_handler(message, run_display, bot, chatbot)
    except Exception as ex:
        bot.send_message(chat_id, str(ex))
