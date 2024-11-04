# DollarBot Email Sender

This document provides an overview of the Python script for sending budget reports via email using the "DollarBot" application. This script uses the Gmail SMTP server to send emails with budget reports as attachments.

## Functions and Methods

### send_email(user_email, subject, message, attachment_path)
This function sends an email to the specified user.

- `user_email`: The recipient's email address.
- `subject`: The subject of the email.
- `message`: The main body of the email.
- `attachment_path`: The path to the file to be attached to the email.

### run(message, bot)
This function initiates the main process. It prompts the user to enter their email address.

- `message`: The message object.
- `bot`: A reference to the chatbot.

### process_email_input(message, bot)
This function processes the user's email input and sends the budget report.

- `message`: The message object containing the user's email input.
- `bot`: A reference to the chatbot.

### Main Workflow
1. The user is prompted to enter their email address.
2. If the "data.csv" file exists in the "code" directory, it is attached to the email and sent.
3. If the "data.csv" file is not found, the script calls the `extract.run()` function to generate the file and then sends the email.
4. The email is sent to the user with the budget report as an attachment.

### Variables
- `smtp_port`: The standard secure SMTP port (587).
- `smtp_server`: The Google SMTP server ("smtp.gmail.com").
- `email_from`: The sender's email address.
- `email_to`: The recipient's email address.
- `pswd`: The application password used to authenticate with Gmail.
- `body`: The email message body.
- `msg`: The MIME object to define email parts.
- `filename`: The path to the attachment file.
- `attachment_package`: The MIMEBase object for the attachment.
- `text`: The email content as a string.
- `TIE_server`: The SMTP server connection.

### Dependencies
- The script relies on the `smtplib`, `email.mime`, and `extract` modules.
- The script also uses a Gmail account and an application-specific password for email sending.

## Usage
1. Run the script, which will prompt the user to enter their email address.
2. The script will check if the "data.csv" file exists, and if so, it will be sent as an attachment.
3. If the file does not exist, the script will call the `extract.run()` function to generate the file and then send the email.

Remember to set up the Gmail account and application-specific password before using the script.

This script is designed for use with the DollarBot application to send budget reports to users via email.
You can use this Markdown document as a README to describe the functionality and usage of your script on GitHub.

## Test

The tests checks is the http client connection has been correctly configured or not.
