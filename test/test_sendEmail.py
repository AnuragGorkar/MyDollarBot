import unittest
from unittest.mock import patch, Mock, MagicMock, call
import os
import pandas as pd
from datetime import datetime
import logging
from code import sendEmail  # type: ignore
import matplotlib.pyplot as plt

class TestSendEmailFunctions(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.test_file = 'test_attachment.txt'
        with open(self.test_file, 'w') as f:
            f.write("Test content")
            
        self.test_data = pd.DataFrame({
            'Date': ['2024-10-01', '2024-10-02'],
            'Category': ['Food', 'Transport'],
            'Amount': [100.0, 50.0]
        })

    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    @patch('code.sendEmail.smtplib.SMTP')
    def test_send_email_success(self, mock_smtp):
        """Test successful email sending"""
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        sendEmail.send_email(
            "test@example.com",
            "Test Subject",
            "Test Message",
            [self.test_file]
        )

        mock_smtp.assert_called_once_with("smtp.gmail.com", 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()
        mock_server.sendmail.assert_called_once()


    @patch('code.sendEmail.smtplib.SMTP')
    def test_send_email_smtp_error(self, mock_smtp):
        """Test email sending with SMTP error"""
        mock_smtp.return_value.__enter__.side_effect = Exception("SMTP Error")
        
        with self.assertLogs(level='ERROR') as log:
            sendEmail.send_email(
                "test@example.com",
                "Test Subject",
                "Test Message",
                [self.test_file]
            )
            self.assertIn("Error sending email", log.output[0])

    @patch('code.sendEmail.gemini_helper.initialize_gemini')
    def test_generate_spending_summary_success(self, mock_initialize_gemini):
        """Test successful spending summary generation"""
        mock_response = MagicMock()
        mock_response.text = "Generated Summary"
        mock_gemini = MagicMock()
        mock_gemini.generate_content.return_value = mock_response
        mock_initialize_gemini.return_value = mock_gemini
        
        user_data = [{'Date': '2024-10-01', 'Category': 'Food', 'Amount': 100.0}]
        result = sendEmail.generate_spending_summary(user_data)
        
        self.assertEqual(result, "Generated Summary")
        mock_initialize_gemini.assert_called_once()

    @patch('code.sendEmail.gemini_helper.initialize_gemini')
    def test_generate_spending_summary_error(self, mock_initialize_gemini):
        """Test spending summary generation with error"""
        mock_initialize_gemini.side_effect = Exception("Gemini Error")
        
        with self.assertLogs(level='ERROR') as log:
            result = sendEmail.generate_spending_summary([])
            self.assertIn("Error generating summary with Gemini", log.output[0])
            self.assertIn("Please review your financial data manually", result)

    @patch('sendEmail.plt')  # Adjust the import path to match your module structure
    def create_spending_charts(df):
        try:
            # Create monthly and categorized spending charts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            monthly_chart_path = f"monthly_spending_{timestamp}.pdf"
            category_chart_path = f"category_spending_{timestamp}.pdf"
            
            # Monthly Spending Plot
            df = df.copy()  # Create a copy to avoid modifying original
            df['Date'] = pd.to_datetime(df['Date'], format="%d-%b-%Y")
            df['Month'] = df['Date'].dt.to_period('M')
            monthly_data = df.groupby('Month')['Amount'].sum()
            
            plt.figure()
            monthly_data.plot(kind='bar')
            plt.title("Monthly Spending")
            plt.xlabel("Month")
            plt.ylabel("Amount Spent")
            plt.savefig(monthly_chart_path)
            plt.close()
            
            # Category Spending Plot
            plt.figure()
            category_data = df.groupby('Category')['Amount'].sum()
            category_data.plot(kind='pie', autopct='%1.1f%%', startangle=90)
            plt.title("Spending by Category")
            plt.savefig(category_chart_path)
            plt.close()

            return monthly_chart_path, category_chart_path

        except Exception as e:
            logging.error(f"Error creating charts: {str(e)}")
            return None, None
    
    @patch('code.sendEmail.plt')
    def test_create_spending_charts_error(self, mock_plt):
        """Test chart creation with error"""
        mock_plt.figure.side_effect = Exception("Plot Error")
        
        with self.assertLogs(level='ERROR') as log:
            result = sendEmail.create_spending_charts(self.test_data)
            self.assertIn("Error creating charts", log.output[0])
            self.assertEqual(result, (None, None))

    def test_save_data_to_excel_success(self):
        """Test successful Excel file creation"""
        expense_data = [['2024-10-01', 'Food', 100.0]]
        income_data = [['2024-10-01', 'Salary', 1000.0]]
        
        excel_file = sendEmail.save_data_to_excel(expense_data, income_data)
        
        try:
            self.assertTrue(os.path.exists(excel_file))
            # Verify both sheets exist and have correct data
            with pd.ExcelFile(excel_file) as xls:
                self.assertIn('Expenses', xls.sheet_names)
                self.assertIn('Income', xls.sheet_names)
                
                df_expenses = pd.read_excel(xls, 'Expenses')
                df_income = pd.read_excel(xls, 'Income')
                
                self.assertEqual(len(df_expenses), 1)
                self.assertEqual(len(df_income), 1)
                self.assertEqual(df_expenses.iloc[0]['Amount'], 100.0)
                self.assertEqual(df_income.iloc[0]['Amount'], 1000.0)
        finally:
            if os.path.exists(excel_file):
                os.remove(excel_file)

    def test_save_data_to_excel_empty_data(self):
        """Test Excel file creation with empty data"""
        excel_file = sendEmail.save_data_to_excel([], [])
        
        try:
            self.assertTrue(os.path.exists(excel_file))
            with pd.ExcelFile(excel_file) as xls:
                df_expenses = pd.read_excel(xls, 'Expenses')
                df_income = pd.read_excel(xls, 'Income')
                self.assertEqual(len(df_expenses), 0)
                self.assertEqual(len(df_income), 0)
        finally:
            if os.path.exists(excel_file):
                os.remove(excel_file)

    @patch('code.sendEmail.helper.getUserHistory')
    def test_process_email_input_success(self, mock_get_history):
        """Test successful email report processing"""
        mock_bot = MagicMock()
        mock_message = MagicMock()
        mock_message.chat.id = 123
        mock_message.text = "test@example.com"
        
        # Mock user history data
        mock_get_history.side_effect = [
            ["2024-10-01 12:00,Salary,1000", "2024-10-02 12:00,Bonus,500"],  # Income
            ["2024-10-01 12:00,Food,100", "2024-10-02 12:00,Transport,50"]   # Expense
        ]
        
        with patch('code.sendEmail.send_email') as mock_send_email:
            sendEmail.process_email_input(mock_message, mock_bot)
            mock_send_email.assert_called_once()
            mock_bot.send_message.assert_called_with(123, 'Email with report sent successfully!')

    @patch('code.sendEmail.helper.getUserHistory')
    def test_process_email_input_error(self, mock_get_history):
        """Test email report processing with error"""
        mock_bot = MagicMock()
        mock_message = MagicMock()
        mock_message.chat.id = 123
        mock_message.text = "test@example.com"
        
        mock_get_history.side_effect = Exception("Database Error")
        
        with self.assertLogs(level='ERROR') as log:
            sendEmail.process_email_input(mock_message, mock_bot)
            self.assertIn("Error", log.output[0])

    def test_run_function(self):
        """Test the main run function"""
        mock_bot = MagicMock()
        mock_message = MagicMock()
        mock_message.chat.id = 123
        
        sendEmail.run(mock_message, mock_bot)
        
        mock_bot.send_message.assert_called_once()
        mock_bot.register_next_step_handler.assert_called_once()

if __name__ == '__main__':
    unittest.main(verbosity=2)
