import os
import json
from unittest.mock import Mock
from unittest.mock import patch
from telebot import types
from code import category
from unittest.mock import ANY



dateFormat = '%d-%b-%Y'
timeFormat = '%H:%M'
monthFormat = '%b-%Y'


@patch('telebot.telebot')
def test_run(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("hello from test run!")
    category.run(message, mc)
    assert(mc.reply_to.called_with(ANY, 'Select Operation', ANY))

@patch('telebot.telebot')
def test_post_operation_selection_working(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    message = create_message("hello from testing!")
    category.post_operation_selection(message, mc, 'Income')
    assert(mc.send_message.called)

@patch('telebot.telebot')
def test_post_operation_selection_noMatchingCategory(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(category, 'helper')
    category.helper.getCategoryOptions.return_value = {}

    message = create_message("hello from test_category.py!")
    category.post_operation_selection(message, mc, 'Income')
    mc.send_message.assert_called_with(11, 'Invalid', reply_markup=ANY)

@patch('telebot.telebot')
def test_category_add_income(mock_telebot, mocker):
    mc = mock_telebot.return_value
    message = create_message("Test Category")
    message.text='Test Category'
    mocker.patch.object(category, 'getFileName')
    category.getFileName.return_value="test_income.txt"
    category.category_add(message, mc, 'Income')
    mc.send_message.assert_called_with(11, 'Add category "{}" successfully!'.format('Test Category'))

@patch('telebot.telebot')
def test_category_delete_income(mock_telebot, mocker):
    mc = mock_telebot.return_value
    message = create_message("Test Category")
    message.text='Test Category'
    mocker.patch.object(category, 'getFileName')
    category.getFileName.return_value="test_income.txt"
    category.category_delete(message, mc, 'Income')
    mc.send_message.assert_called_with(11, 'Delete category "{}" successfully!'.format('Test Category'))

@patch('telebot.telebot')
def test_category_not_income(mock_telebot, mocker):
    mc = mock_telebot.return_value
    message = create_message("Test Category")
    message.text='Test Category'
    mocker.patch.object(category, 'getFileName')
    category.getFileName.return_value="test_category.txt"
    category.category_add(message, mc, 'Not_Income')
    mc.send_message.assert_called_with(11, 'Add category "{}" successfully!'.format('Test Category'))

@patch('telebot.telebot')
def test_category_view(mock_telebot, mocker):
    mc = mock_telebot.return_value
    message = create_message("Test Category")
    message.text='Test Category'
    mocker.patch.object(category, 'getFileName')
    category.getFileName.return_value="test_category.txt"
    category.category_view(message, mc, 'Not_Income')
    assert(mc.send_message.called)


   
def create_message(text):
    params = {'messagebody': text}
    chat = types.User(11, False, 'test')
    return types.Message(1, None, None, chat, 'text', params, "")

