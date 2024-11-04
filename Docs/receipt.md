# About MyDollarBot's /receipt Feature
This feature enables the user to retrieve receipts in an image format of their expenses for a particular date.
Currently we have the following expense categories set by default:

# Location of Code for this Feature
The code that implements this feature can be found [here](https://github.com/anuj672/MyDollarBot-BOTGo/blob/main/code/receipt.py)

## Core Descriptions and functions

1. command_receipt(message, bot):
Accepts a `message` object and a `bot` instance as parameters. Requests the user to input a date in the format `YYYY-MM-DD` or `YYYYMMDD`.

2. process_date_input(message):
Accepts a `message` objects. Formats the date given by the user as per the naming convention of the stored receipts. Searches the receipt for the given date in the receipts folder and returns all receipts for the given date. If there are no receipts for that date it'll return `None`.

# How to run this feature?
Once the project is running(please follow the instructions given in the main README.md for this), please type /receipt into the telegram bot.
Below you can see the example in the text format.:

Bhavesh Ittadwar, [Oct 19, 2023 at 4:55:58 PM]:
/receipt

Pegasus, [Oct 19, 2023 at 4:55:59 PM]:
Please enter the date (YYYY-MM-DD or YYYYMMDD) for which you want to retrieve receipts:

Bhavesh Ittadwar, [Oct 19, 2023 at 4:56:07 PM]:
2023-10-18

[[Receipt Image]] sent in chat.
