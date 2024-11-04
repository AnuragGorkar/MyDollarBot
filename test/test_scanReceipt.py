import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from code import scan_receipt  # Adjust import to match your actual module structure

class TestReceiptProcessor(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.mock_bot = Mock()
        self.chat_id = "123456"
        self.mock_message = Mock()
        self.mock_message.chat.id = self.chat_id
        
        # Clear receipt_data before each test
        if hasattr(self, 'receipt_data'):
            self.receipt_data = {}

    @patch('telebot.TeleBot')
    def test_run_function(self, mock_telebot):
        """Test the run function initiates receipt scanning process"""
        # Arrange
        mock_bot = mock_telebot.return_value

        # Act
        scan_receipt.run(self.mock_message, mock_bot)

        # Assert
        mock_bot.send_message.assert_called_once_with(
            self.chat_id,
            'Please send me a photo of your receipt.'
        )
        mock_bot.register_next_step_handler.assert_called_once()

    @patch('gemini_helper.process_receipt_image')
    def test_handle_receipt_image_success(self, mock_process_receipt):
        """Test successful receipt image processing"""
        # Arrange
        self.mock_message.photo = [Mock(file_id='123')]
        mock_file_info = Mock(file_path='path/to/file')
        self.mock_bot.get_file.return_value = mock_file_info
        
        mock_result = {
            'date': '2024-03-21',
            'amount': 100.50,
            'category': 'Groceries'
        }
        mock_process_receipt.return_value = (mock_result, None)

        # Act
        scan_receipt.handle_receipt_image(self.mock_message, self.mock_bot)

        # Assert
        self.mock_bot.get_file.assert_called_once_with('123')
        mock_process_receipt.assert_called_once()

    def test_handle_receipt_image_no_photo(self):
        """Test handling when no photo is provided"""
        # Arrange
        self.mock_message.photo = []

        # Act
        scan_receipt.handle_receipt_image(self.mock_message, self.mock_bot)

        # Assert
        self.mock_bot.send_message.assert_called_once_with(
            self.chat_id,
            'Please send a valid receipt photo.'
        )
        self.mock_bot.register_next_step_handler.assert_called_once()

    @patch('gemini_helper.process_receipt_image')
    def test_handle_receipt_image_processing_error(self, mock_process_receipt):
        """Test handling of receipt processing error"""
        # Arrange
        self.mock_message.photo = [Mock(file_id='123')]
        mock_file_info = Mock(file_path='path/to/file')
        self.mock_bot.get_file.return_value = mock_file_info
        mock_process_receipt.return_value = (None, "Processing error")

        # Act
        scan_receipt.handle_receipt_image(self.mock_message, self.mock_bot)

        # Assert
        self.mock_bot.send_message.assert_called_once_with(
            self.chat_id,
            'Processing error'
        )

    @patch('helper.read_json')
    @patch('helper.write_json')
    @patch('telebot.TeleBot.send_message')  # Mocking the send_message to avoid actual API calls
    def test_add_user_record_new_user(self, mock_send_message, mock_write_json, mock_read_json):
        """Test adding a record for a new user"""
        # Arrange
        mock_read_json.return_value = {}
        record = {
            'date': '2024-03-21',
            'amount': 100.50,
            'category': 'Groceries'
        }

        # Act
        result = scan_receipt.add_user_record(self.chat_id, record)

        # Assert
        self.assertIn(str(self.chat_id), result)
        expected_record = '21-Mar-2024 00:00,Groceries,100.5'
        self.assertIn(expected_record, result[str(self.chat_id)]['data'])
        mock_write_json.assert_called_once()
        mock_send_message.assert_called_once()  # Ensure send_message is called, but doesn't send to Telegram

    @patch('helper.read_json')
    @patch('helper.write_json')
    @patch('telebot.TeleBot.send_message')  # Mocking the send_message to avoid actual API calls
    def test_add_user_record_existing_user(self, mock_send_message, mock_write_json, mock_read_json):
        """Test adding a record for an existing user"""
        # Arrange
        existing_data = {
            str(self.chat_id): {
                'data': ['20-Mar-2024 00:00,Food,50.0'],
                'income_data': [],
                'budget': {'overall': None, 'category': None, 'max_per_txn_spend': None}
            }
        }
        mock_read_json.return_value = existing_data
        
        record = {
            'date': '2024-03-21',
            'amount': 100.50,
            'category': 'Groceries'
        }

        # Act
        result = scan_receipt.add_user_record(self.chat_id, record)

        # Assert
        self.assertEqual(len(result[str(self.chat_id)]['data']), 2)
        expected_record = '21-Mar-2024 00:00,Groceries,100.5'
        self.assertIn(expected_record, result[str(self.chat_id)]['data'])
        mock_write_json.assert_called_once()
        mock_send_message.assert_called_once()  # Ensure send_message is called, but doesn't send to Telegram


if __name__ == '__main__':
    unittest.main()
