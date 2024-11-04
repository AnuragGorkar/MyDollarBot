# Max Transaction Limit Management in Telegram Bot

This document provides an overview of the Python script used in a Telegram bot for managing the maximum transaction limit. Users can set their maximum transaction limit using this script.

## Functions and Methods

### run(message, bot)
This function initiates the process of managing the maximum transaction limit.

- `message`: The message object received from the user in the chat.
- `bot`: The bot instance used to interact with the Telegram API.

### post_max_budget(message, bot)
This function handles the user's input for setting the new maximum transaction limit and updates the user's records.

- `message`: The message object received from the user with the new maximum transaction limit.
- `bot`: The bot instance used to interact with the Telegram API.

### Main Workflow
1. Users initiate the process by calling the `run()` function.
2. The user's chat ID is obtained from the message.
3. The script checks if the user has set a maximum transaction limit.
4. If a limit is set, the current limit is displayed to the user.
5. The user is prompted to enter a new maximum transaction limit (numeric values only).
6. The script registers a handler for the next step to capture the user's input.
7. The `post_max_budget()` function handles the user's input, validates it, and updates the user's records.
8. The updated maximum limit is stored in the user's records.
9. When the user adds a new transaction, the entered transaction value is checked against the set maximum transaction limit.
10. If the value exceeds, then a warning message is sent to the user.
11. If not, then the expenditure is successfully recorded.

### Dependencies
- The script relies on the `helper` module for various functions such as checking the current maximum limit, validating user input, and updating user records.
- It uses the `telebot` module for interacting with the Telegram bot.

## Usage
1. Users initiate the process by calling the script.
2. If a maximum limit is set, the current limit is displayed to the user.
3. Users are prompted to enter a new maximum transaction limit (numeric values only).
4. The script validates the input and updates the user's records.
5. If the entered value exceeds the transaction limit, then warning message is displayed to the user.
6. If not, the the expenditure is successfully recorded.

This script is designed for users to manage their maximum transaction limits within the Telegram bot.

## Test
1. The tests for budget max has been set up to check two cases.
2. The first test checks for a budget where we display a warning.
3. The second tests checks for a budget which is below the threshold and should not display the message
