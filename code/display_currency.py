from datetime import datetime
from forex_python.converter import CurrencyRates
from telebot import types
import helper

spend_display_option = ["Day", "Month"]
selection = ""
rate = 1
total = ""
bud = ""
c = CurrencyRates()
try:
    DOLLARS_TO_RUPEES = c.get_rate('USD', 'INR')
    DOLLARS_TO_EUROS = c.get_rate('USD', 'EUR')
    DOLLARS_TO_SWISS_FRANC = c.get_rate('USD', 'CHF')
except:
    DOLLARS_TO_RUPEES = 84
    DOLLARS_TO_EUROS = 0.95
    DOLLARS_TO_SWISS_FRANC = 0.9


def run(message, bot):
    helper.read_json()
    chat_id = message.chat.id
    history = helper.getUserExpenseHistory(chat_id)
    if history is None:
        bot.send_message(chat_id, "Sorry, there are no records of the spending!")
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = 2
        choices = ["INR", "EUR", "CHF"]
        for c in choices:
            markup.add(c)
        choice = bot.reply_to(
            message, "Which currency to you want to convert to?", reply_markup=markup
        )
        bot.register_next_step_handler(choice, run_display, bot)


def run_display(message, bot):
    global selection
    global rate
    helper.read_json()
    chat_id = message.chat.id
    selection = message.text
    if selection == "INR":
        try:
            rate = DOLLARS_TO_RUPEES
        except:
            rate = 84
    if selection == "EUR":
        try:
            rate = DOLLARS_TO_EUROS
        except:
            rate = 0.95
    if selection == "CHF":
        try:
            rate = DOLLARS_TO_SWISS_FRANC
        except:
            rate = 0.9
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for mode in helper.getSpendDisplayOptions():
        markup.add(mode)
    # markup.add('Day', 'Month')
    msg = bot.reply_to(message, 'Please select a category to see details', reply_markup=markup)
    bot.register_next_step_handler(msg, display_total_currency, bot)


def display_total_currency(message, bot):
    global total
    global bud
    try:
        chat_id = message.chat.id
        DayWeekMonth = message.text

        if DayWeekMonth not in helper.getSpendDisplayOptions():
            raise Exception("Sorry I can't show spendings for \"{}\"!".format(DayWeekMonth))

        history = helper.getUserExpenseHistory(chat_id)
        if history is None:
            raise Exception("Oops! Looks like you do not have any spending records!")

        bot.send_message(chat_id, "Hold on! Calculating...")
        total_text = ""
        # get budget data
        budgetData = {}
        if helper.isOverallBudgetAvailable(chat_id):
            budgetData = helper.getOverallBudget(chat_id)
        elif helper.isCategoryBudgetAvailable(chat_id):
            budgetData = helper.getCategoryBudget(chat_id)

        if DayWeekMonth == 'Day':
            query = datetime.now().today().strftime(helper.getDateFormat())
            # query all that contains today's date
            queryResult = [value for index, value in enumerate(history) if str(query) in value]
        elif DayWeekMonth == 'Month':
            query = datetime.now().today().strftime(helper.getMonthFormat())
            # query all that contains today's date
            queryResult = [value for index, value in enumerate(history) if str(query) in value]

        total_text = calculate_spendings(queryResult)
        total = total_text
        bud = budgetData
        spending_text = display_budget_by_text(history, budgetData)
        if len(total_text) == 0:
            spending_text += "----------------------\nYou have no spendings for {}!".format(DayWeekMonth)
            bot.send_message(chat_id, spending_text)
        else:
            spending_text += "\n----------------------\nHere are your total spendings for the {}:\nCATEGORIES\tAMOUNT \n----------------------\n{}".format(
                DayWeekMonth.lower(), total_text)
            bot.send_message(chat_id, spending_text)
    except Exception as e:
        bot.reply_to(message, 'Oh no! ' + str(e))


def calculate_spendings(queryResult):
    total_dict = {}

    for row in queryResult:
        # date,cat,money
        s = row.split(',')
        # cat
        cat = s[1]
        if cat in total_dict:
            # round up to 2 decimal
            total_dict[cat] = round(total_dict[cat] + float(s[2]), 2)
        else:
            total_dict[cat] = float(s[2])
    total_text = ""
    for key, value in total_dict.items():
        if selection == "INR":
            value = round(value * rate, 2)
            total_text += str(key) + " ₹" + str(value) + "\n"
        elif selection == "EUR":
            value = round(value * rate, 2)
            total_text += str(key) + " €" + str(value) + "\n"
        elif selection == "CHF":
            value = round(value * rate, 2)
            total_text += str(key) + " ₣" + str(value) + "\n"
        else:
            total_text += str(key) + " $" + str(value) + "\n"
    return total_text


def display_budget_by_text(history, budget_data) -> str:
    try:
        query = datetime.now().today().strftime(helper.getMonthFormat())
        # query all expense history that contains today's date
        queryResult = [value for index, value in enumerate(history) if str(query) in value]
        total_text = calculate_spendings(queryResult)
        budget_display = ""
        total_text_split = [line for line in total_text.split('\n') if line.strip() != '']

        if isinstance(budget_data, str):
            # if budget is string denoting it is overall budget
            budget_val = float(budget_data)
            budget_val = round(budget_val * rate, 2)
            total_expense = 0
            # sum all expense
            for expense in total_text_split:
                a = expense.split(' ')
                amount = a[1].replace("$", "").replace("₹", "").replace("€", "", ).replace("₣", "")
                total_expense += float(amount)
            # calculate the remaining budget
            remaining = round(budget_val - total_expense,2)
            # set the return message
            budget_display += "Overall Budget is: " + str(
                budget_val) + "\n----------------------\nRemaining Budget is " + str(
                remaining) + "\n"
        elif isinstance(budget_data, dict):

            budget_display += "Budget by Categories in " + str(selection) + " are:\n"
            categ_remaining = {}
            # categorize the budgets by their categories
            for key in budget_data.keys():
                budget_display += key + ":" + str(round(rate*float(budget_data[key]),2)) + "\n"
                categ_remaining[key] = round(rate*float(budget_data[key]),2)
                print(categ_remaining)
                print(budget_data[key])
            #  calculate the remaining budgets by categories
            for i in total_text_split:
                # the expense text is in the format like "Food $100"
                a = i.split(' ')
                a[1] = a[1].replace("$", "").replace("₹", "").replace("€", "").replace("₣", "")
                categ_remaining[a[0]] = categ_remaining[a[0]] - float(a[1]) if a[0] in categ_remaining else -float(a[1])
            budget_display += "----------------------\nCurrent remaining budget is: \n"
            # show the remaining budgets
            for key in categ_remaining.keys():
                budget_display += key + ":" + str(categ_remaining[key]) + "\n"
        return budget_display
    except Exception as e:
        return str(e)