-# DollarBot Bulk Insert

This document provides an overview of the Python script for inserting bulk of daily transactions and saving users time and effort by removing the need of performing each of them individually.

## Functions and Methods

### save_file(message,bot)
This function saves the csv file send by the user on to the server.

- `message`: The message object.
- `bot`: A reference to the chatbot.

### process_csv_file(message, bot)
This function initiates the main process of saving the transactions by first calling save_file function and then reads the file to update the database.

- `message`: The message object.
- `bot`: A reference to the chatbot.