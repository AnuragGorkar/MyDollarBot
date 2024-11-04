import unittest
from unittest.mock import patch, Mock
from code.extract import run

@patch('code.extract.helper.getUserExpenseHistory', return_value=["28-Oct-2021 15:27,Food,2.3", "28-Oct-2021 15:28,Groceries,20.0"])
@patch('telebot.telebot')
def test_csv_extraction_with_valid_data(mock_bot, mock_get_user_history):
    # Simulate a message that triggers the CSV extraction
    message = Mock()
    
    # Call the extraction function
    run(message, mock_bot)

    # Check if the bot's send_document method is called
    mock_bot.send_document.assert_called_once()
    mock_bot.send_message.assert_not_called()  # No message should be sent 

@patch('code.extract.helper.getUserExpenseHistory', return_value=[])
@patch('telebot.telebot')
def test_csv_extraction_with_no_data(mock_bot, mock_get_user_history):
    # Simulate a message that triggers the CSV extraction
    message = Mock()

    # Call the extraction function
    run(message, mock_bot)

    # Check if the bot sends a message indicating no data to extract
    mock_bot.send_message.assert_called_with(message.chat.id, "no data to generate csv")
    mock_bot.send_document.assert_not_called()  # No document should be sent

if __name__ == '__main__':
    unittest.main()
