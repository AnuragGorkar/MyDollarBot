import os
import json
from telebot import types
from unittest.mock import patch, mock_open, ANY, MagicMock
import pytest
from datetime import datetime

# Import the module containing get_csv functionality
from code import get_csv

def create_message(text, chat_id=11):
    """Helper function to create a mock message object"""
    params = {'messagebody': text}
    chat = types.User(chat_id, False, 'test')
    return types.Message(1, None, None, chat, 'text', params, "")

@patch('telebot.TeleBot')
def test_run_initial_setup(mock_telebot, mocker):
    """Test the initial setup of CSV generation with valid Income/Expense selection."""
    bot_instance = mock_telebot.return_value
    bot_instance.reply_to.return_value = True
    
    # Mock helper function
    mocker.patch.object(get_csv, 'helper')
    get_csv.helper.getIncomeOrExpense.return_value = {'1': 'Income', '2': 'Expense'}
    
    message = create_message("hello")
    get_csv.run(message, bot_instance)
    
    # Verify bot prompts for Income or Expense selection
    bot_instance.reply_to.assert_called_with(message, 'Select Income or Expense', reply_markup=ANY)
    assert bot_instance.register_next_step_handler.called

@patch('telebot.TeleBot')
def test_post_type_selection_no_expenses(mock_telebot, mocker):
    """Test response when there are no expense records."""
    bot_instance = mock_telebot.return_value
    test_chat_id = 1574038305
    
    # Mock helper functions and empty user history
    mocker.patch.object(get_csv, 'helper')
    get_csv.helper.read_json.return_value = True
    get_csv.helper.getUserHistory.return_value = []
    
    message = create_message("Expense", test_chat_id)
    
    get_csv.post_type_selection(message, bot_instance)
    
    # Confirm bot sends "No records found"
    bot_instance.send_message.assert_called_with(test_chat_id, "No records found!")
    bot_instance.send_document.assert_not_called()

@patch('telebot.TeleBot')
def test_post_type_selection_file_error(mock_telebot, mocker):
    """Test CSV generation when file operations encounter an error."""
    bot_instance = mock_telebot.return_value
    test_chat_id = 894127939
    
    # Mock helper functions and simulate file operation error
    mocker.patch.object(get_csv, 'helper')
    get_csv.helper.read_json.return_value = True
    get_csv.helper.getUserHistory.return_value = ["19-Oct-2023 15:27,Food,2.3"]
    
    message = create_message("Expense", test_chat_id)
    
    # Simulate file error
    with patch('builtins.open', side_effect=Exception("File error")):
        get_csv.post_type_selection(message, bot_instance)
    
    # Check error handling response from bot
    bot_instance.reply_to.assert_called_with(message, ANY)

@patch('telebot.TeleBot')
def test_post_type_selection_no_history_type_provided(mock_telebot, mocker):
    """Test bot's response when no Income or Expense is provided as a selection."""
    bot_instance = mock_telebot.return_value
    test_chat_id = 1574038305

    # Mock helper functions to return None for invalid history type
    mocker.patch.object(get_csv, 'helper')
    get_csv.helper.read_json.return_value = True
    get_csv.helper.getUserHistory.return_value = None  # Simulate no records found
    
    message = create_message("InvalidType", test_chat_id)
    
    get_csv.post_type_selection(message, bot_instance)
    
    # Check for appropriate bot message for no records found
    bot_instance.send_message.assert_called_with(test_chat_id, "No records found!")
    bot_instance.send_document.assert_not_called()
