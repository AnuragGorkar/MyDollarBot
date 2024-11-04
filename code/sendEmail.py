import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import threading
import extract
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import helper
import gemini_helper

extract_complete = threading.Event()

# Function to send an email
def send_email(user_email, subject, message, attachments):
    smtp_port = 587                 # Standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # Google SMTP Server

    email_from = "dollarbot123@gmail.com"
    pswd = "tsvueizeuvzivtjo"   # App password 

    # Create a MIME multipart message
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = user_email
    msg['Subject'] = subject

    # Attach the body of the message as HTML
    msg.attach(MIMEText(message, 'html'))

    # Attach all files provided in the attachments list
    for attachment_path in attachments:
        with open(attachment_path, 'rb') as attachment:
            filename = os.path.basename(attachment_path)
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={filename}")
            msg.attach(part)

    # Connect to server and send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_from, pswd)
            server.sendmail(email_from, user_email, msg.as_string())
            logging.info(f"Email sent to {user_email}")
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")

# Generate summary with Gemini
def generate_spending_summary(user_data):
    """Use Gemini API to generate a spending summary from the user's financial data."""
    try:
        model = gemini_helper.initialize_gemini()  # Initialize Gemini if not already done
        
        # Combine prompt with user data
        prompt = (
            "Generate a friendly and engaging HTML-formatted financial summary for the user based on the following data. "
            "Include total spending, significant spending categories with their percentages, "
            "unusual spending trends, and actionable recommendations. "
            "Ensure that currency values are formatted correctly (e.g., $473.22), and avoid using any content tags. "
            "Structure it in a clear format using HTML tags for headings and paragraphs.\n\n"
            f"Data: {user_data}"
        )

        response = model.generate_content(prompt)

        return response.text if response else "Unable to generate summary."
    except Exception as e:
        logging.error(f"Error generating summary with Gemini: {str(e)}")
        return "Error in generating summary. Please review your financial data manually."

# Function to create spending charts as PDFs
def create_spending_charts(df):
    try:
        # Create monthly and categorized spending charts
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        monthly_chart_path = f"monthly_spending_{timestamp}.pdf"
        category_chart_path = f"category_spending_{timestamp}.pdf"
        
        # Monthly Spending Plot
        df['Date'] = pd.to_datetime(df['Date'], format="%d-%b-%Y", errors='coerce')
        df.dropna(subset=['Date'], inplace=True)  # Remove rows with invalid dates
        df['Month'] = df['Date'].dt.to_period('M')
        monthly_data = df.groupby('Month')['Amount'].sum()
        
        plt.figure()
        monthly_data.plot(kind='bar', color='skyblue', title="Monthly Spending")
        plt.xlabel("Month")
        plt.ylabel("Amount Spent")
        plt.savefig(monthly_chart_path)
        plt.close()
        
        # Category Spending Plot
        category_data = df.groupby('Category')['Amount'].sum()
        
        plt.figure()
        category_data.plot(kind='pie', autopct='%1.1f%%', startangle=90, title="Spending by Category")
        plt.ylabel('')
        plt.savefig(category_chart_path)
        plt.close()

        return monthly_chart_path, category_chart_path

    except Exception as e:
        logging.error(f"Error creating charts: {str(e)}")
        return None, None

# Function to save user data to Excel
def save_data_to_excel(expense_data, income_data):
    """Save expenses and income to an Excel file with separate sheets."""
    # print(expense_data, "\n\n\n", income_data)
    excel_filename = f"user_financial_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    with pd.ExcelWriter(excel_filename) as writer:
        expense_df = pd.DataFrame(expense_data, columns=['Date', 'Category', 'Amount'])
        income_df = pd.DataFrame(income_data, columns=['Date', 'Category', 'Amount'])
        expense_df.to_excel(writer, sheet_name='Expenses', index=False)
        income_df.to_excel(writer, sheet_name='Income', index=False)
    return excel_filename

# Main process function
def run(message, bot):
    try:
        chat_id = message.chat.id
        message = bot.send_message(chat_id, 'Please enter your email: ')
        bot.register_next_step_handler(message, process_email_input, bot)
    except Exception as e:
        logging.error(str(e))

# Process email input and send report
def process_email_input(message, bot):
    try:
        chat_id = message.chat.id
        user_email = message.text
        email_subject = "DollarBot Monthly Budget Report"

        # Get user data and create DataFrame
        # user_history = helper.getUserHistory(chat_id, 'Expense') + helper.getUserHistory(chat_id, 'Income')
        user_income_history = helper.getUserHistory(chat_id, 'Income')
        user_expense_history = helper.getUserHistory(chat_id, 'Expense')
        data = []
        income_data = []
        expense_data = []

        for record in user_income_history:
            try:
                date_time, category, amount = record.split(",")
                date, _ = date_time.split(" ")
                amount = float(amount)
                income_data.append([date, category, amount])
                data.append([date, category, amount])
            except ValueError:
                continue

        for record in user_expense_history:
            try:
                date_time, category, amount = record.split(",")
                date, _ = date_time.split(" ")
                amount = float(amount)
                expense_data.append([date, category, amount])
                data.append([date, category, amount])
            except ValueError:
                continue

        
        df = pd.DataFrame(data, columns=['Date', 'Category', 'Amount'])

        # Generate summary using Gemini
        summary = generate_spending_summary(df.to_dict(orient='records'))

        # Create charts for monthly and categorized spending
        monthly_chart, category_chart = create_spending_charts(df)

        # Save data to Excel file
        # print(expense_data, income_data)
        excel_file = save_data_to_excel(expense_data, income_data)

        # Prepare email message and attachments
        email_message = f"""
        <html>
        <body>
            <h2>Hello!</h2>
            <p>Here is your monthly financial summary:</p>
            <p>{summary}</p>
            <p>Best regards,<br>DollarBot</p>
        </body>
        </html>
        """
        
        # Prepare email message and attachments
        attachments = [file for file in [monthly_chart, category_chart, excel_file] if file]  # Only include non-None attachments
        # Include Excel file with the report

        # Send email with attachments
        send_email(user_email, email_subject, email_message, attachments)
        bot.send_message(chat_id, 'Email with report sent successfully!')

    except Exception as e:
        logging.error(str(e))
