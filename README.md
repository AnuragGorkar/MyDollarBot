# 💰 TrackMyDollar V5.0 - Budget On The Go(BOTGo) 💰

[https://www.youtube.com/watch?v=9fJScubX-cI](https://youtu.be/Kpe4u8LHseg)

This video shows only the new features and enhancement of some older features. All the other features from Project 3 are working as it is.
<hr>
<p align="center">
<a><img  height=360 width=550 
  src="https://github.com/deekay2310/MyDollarBot/blob/c56b4afd4fd5bbfffea0d0a4aade58596a5cb678/docs/0001-8711513694_20210926_212845_0000.png" alt="Expense tracking made easy!"></a>
</p>
<hr>

![MIT license](https://img.shields.io/badge/License-MIT-green.svg)
[![Platform](https://img.shields.io/badge/Platform-Telegram-blue)](https://desktop.telegram.org/)
![GitHub](https://img.shields.io/badge/Language-Python-blue.svg)
[![GitHub contributors](https://img.shields.io/github/contributors/CSC510SEFALL2024/MyDollarBot-BOTGo)](https://github.com/CSC510SEFALL2024/MyDollarBot-BOTGo/graphs/contributors)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10023576.svg)](https://doi.org/10.5281/zenodo.10023576)
[![Test and Formatting](https://github.com/CSC510SEFALL2024/MyDollarBot-BOTGo/actions/workflows/test.yml/badge.svg)](https://github.com/CSC510SEFALL2024/MyDollarBot-BOTGo/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/CSC510SEFALL2024/MyDollarBot-BOTGo/graph/badge.svg?token=E5235TMYDN)](https://codecov.io/gh/CSC510SEFALL2024/MyDollarBot-BOTGo)
[![GitHub issues](https://img.shields.io/github/issues/CSC510SEFALL2024/MyDollarBot-BOTGo)](https://github.com/CSC510SEFALL2024/MyDollarBot-BOTGo/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/CSC510SEFALL2024/MyDollarBot-BOTGo)](https://github.com/CSC510SEFALL2024/MyDollarBot-BOTGo/issues?q=is%3Aissue+is%3Aclosed)
![GitHub release (with filter)](https://img.shields.io/github/v/release/CSC510SEFALL2024/MyDollarBot-BOTGo)
![Fork](https://img.shields.io/github/forks/CSC510SEFALL2024/MyDollarBot-BOTGo)
![Discord](https://img.shields.io/discord/1163591668637896807?color=blueviolet&label=Discord%20Discussion%20Chat)

<hr>

## :money_with_wings: About TrackMyDollar

TrackMyDollar is an easy-to-use Telegram Bot that assists you in recording your daily expenses on a local system without any hassle 
With simple commands, this bot allows you to:
- Add/Record a new spending
- Show the sum of your expenditure for the current day/month
- Display your spending history
- Clear/Erase all your records
- Edit/Change any spending details if you wish to
- Add a recurring expense 
- User can add a new category and delete an existing category 
- User can see the budget value for the total expense 
- Added pie charts, bar graphs with and without budget lines
- Scan receipts using AI and add new transactions
- Send and Email to themselves with spend analysis using AI and spend graphs
- Export expenses and income to CSV with pivots and charts
- Deployment on GCP 



## :star: Whats New
## Project 2

- Scan Receipt: Use AI to extract the amount, date and category from any image of a receipt and add it to the transactions.
- Email Transaction History: Users can request their complete transaction history with graphs via email for easy access and record-keeping. Users get an analysis about their spends using AI.
- CSV Transaction History Extraction: Users can download their transaction history in CSV format, providing a versatile data export option for analysis along with charts and images.
- GitHub Actions Automation: Automated testing, code formatting, and syntax checks have been implemented through Github Actions. A minimum 80% code coverage is required for successful builds, ensuring code quality and testing standards are maintained.

## What more can be done?
Please refer to the issue list available [here](https://github.com/CSC510SEFALL2024/MyDollarBot-BOTGo/issues) to see what more can be done to make MyDollarBot better. Please refer to the MyDollarBot project present [here](https://github.com/orgs/CSC510SEFALL2024/projects/1) to have a look at the tasks done or in progress

## Demo

https://user-images.githubusercontent.com/72677919/140454147-f879010a-173b-47b9-9cfb-a389171924de.mp4

## 🚀 Installation Guide for TrackMyDollar BOTGo

Follow these instructions to set up the TrackMyDollar BOTGo on your local system in a few minutes.

### Step 1: Clone Repository
1. Open a terminal.
2. Clone this repository to your local system:
   ```bash
   git clone https://github.com/CSC510SEFALL2024/MyDollarBot-BOTGo/tree/main
   ```

### Step 2: Install Dependencies
1. Navigate to the project directory where the repository was cloned.
2. Install the required dependencies by running:
    ```bash
     pip install -r requirements.txt
     ```
### Step 3: Set Up Telegram Bot with BotFather
1. Open Telegram and search for "BotFather".
2. Click "Start" and enter the following command:
    ```bash
      /newbot
    ```
3. Follow the instructions to:
    * Name your bot.
    * Choose a username ending with "bot".
4. Copy the token BotFather provides for accessing the HTTP API.

### Step 4: Configure API Token
1. Create a user.properties in the repository folder.
    ```bash
    touch user.properties
    ```
2. Add the api key from telegram in the user.properties file
    ```bash
    api_token=<your_api_token>
    ```
### Step 5: Set Up Gemini API Key
1. Go to the Gemini Developer Console and log in or create an account.
2. Navigate to the API section and select Create New Project.
3. Name your project and select the appropriate settings for API access.
4. Once the project is created, go to the API Keys section within your project dashboard.
5. Generate a new API key and secret. Make sure to note down the key and secret as they will only be shown once.
6. Open the `user.properties` file in the project directory and add the Gemini API key and secret as follows:
     ```bash
       api_token=<your_telegram_api_token>
       gemini_api_key=<your_gemini_api_key>
    ```

### Step 6: Run the Bot
1. From the project directory, execute the following command:
    ```bash
      Copy code
      ./run.sh
    ```
    (Or use bash run.sh if needed. If you're on Mac or Linux, you may need to run chmod +x run.sh first.)
    A successful run will generate a terminal message: "TeleBot: Started polling."

### Step 7: Connect to Your Bot on Telegram
1. In Telegram, search for your bot using the username you created.
2. Open the bot and type the command:
    ```bash
      /start
    ```

**You are now ready to track your expenses with TrackMyDollar BOTGo!**

## Testing

We use pytest to perform testing on all unit tests together. The command needs to be run from the home directory of the project. The command is:
```
python -m pytest test/
```

## Code Coverage

Code coverage is part of the build. Every time new code is pushed to the repository, the build is run, and along with it, code coverage is computed. This can be viewed by selecting the build, and then choosing the codecov pop-up on hover.

Locally, we use the coverage package in python for code coverage. The commands to check code coverage in python are as follows:

```
coverage run -m pytest test/
coverage report
```

Please note: A coverage below 80% will cause the build to fail.

## :information_desk_person: Feature Demo
### Display Menu

Checkout what all actions you can perform in BotGo 

1. Enter the `/menu` command.
2. A list of commands with their description will be displayed.

### Budget

I want to increase/decrease my monthly budget.

1. Enter the `/budget` command
2. Following this user can add/update his/her budget, view current budget, delete the budget, or review per transaction maximum spend limit

### Add Expense

I just spent money and want to mark it as a transaction! 

1. Enter the `/add_expense` command
2. Click on the category to add
3. Type in the amount spent
4. Click on the date of the transaction
5. Select if you want to upload a receipt
6. Finally, your transaction will be recoded


### Add Income

I just earned some money and want to mark it as a transaction! 

1. Enter the `/add_income` command
2. Click on the category to add
3. Type in the amount earned
4. Click on the date of the transaction
5. Select if you want to upload a receipt
6. Finally, your transaction will be recoded

### Delete

Oh no! I entered a transaction but want to delete it! 

1. Enter the `/delete` command
2. This will delete all the transactions made so far.

### Edit

Oh no! I entered a transaction but entered the wrong category!

1. Enter the `/edit` command
2. Specify the date, category, and value of the transaction
3. Specify what part of the transaction to edit (either date, category, or value)
4. Enter in a new value

### Adding transactions from CSV 

I want to add transactions from a CSV my bank gave me, and visalize my spendings


1. Drag the .csv file into the telegram chat according to the format provided, and press send
2. For each transaction, classify the category
   1. The application will remember these mappings

### Download History

I want a CSV file of all my transactions.

1. Make sure you have a transaction history.
2. Enter the `/extract` command.
3. A CSV file will be sent with your history.

### See total Expenditure in different currencies

I want to convert my total daily or monthly expenditure in a different currency.

1. Enter the `/displayCurrency` command
2. Next, Choose your currency from the options
3. Choose from the category of day or month
4. You will get the converted price in that currency

### Send Email (Enhanced) 

I want to send myself an email for the monthly expenditure

1. Make sure you have a transaction history.
2. Enter the `/sendEmail` command.
3. Type the intended email address
4. You will get an email with the history file as attachment.
5. Along with the attachment you will get spend analysis using AI in natural language with improved format and graphs.

### Chat with AI

You can get a second opinion on your spendings by chatting with integrated AI.

1. Enter the `/chat` command.
2. You will be welcomed by the AI and since your history is already available to it you can ask questions regarding your financial questions
3. enter `exit` to stop the chat.

### Download PDF 

You can get a summary of your transactions in PDF format.

1. Enter the `/pdf` command.
2. Select the category that you want in the PDF history.
3. your PDF history will be created and ready to download.

### Download CSV (New)

You can get a summary of your transactions in CSV format.

1. Enter the `/csv` command.
2. Select the category that you want in the CSV history.
3. your CSV history will be created and ready to download with graphs and images.

### Scan Receipt (New)

You can add transactions by scanning images of your receipts using AI.

1. Enter the `/scan_receipt` command.
2. Upload an image of your receipt.
3. Gemini AI will scan this image and upload the transaction to your history.

### Add recurring expense

I have to add an expense will be repeated in the future

1. Enter the  `/add_recurring` command.
2. Select the category
3. Enter the amount 
4. Enter for how many months the expense will be there.
5. Your recurring expense will be added.

### Spending Estimation

Get an estimate of your spending for next day or month

1. Enter the  `/estimate` command.
2. Select from following
   1. Next Day
   2. Next Month
3. An Estimate will be provided

### Display your transactions

Get a tabular and graphical representation of your transactions

1. Enter the `/display` command.
2. Select from following category
   1. Day
   2. Month
3. Tabulated data will be provided
4. Following options can be chosen for graphical representation.
   1. Bar with budget
   2. Pie
   3. Bar without budget
5. Graph will be displayed according to choice.

### Receipts

Display all receipts for the day

1. Enter the `/receipt` command.
2. Enter the date `(YYYY-MM-DD or YYYYMMDD)` in this format to get receipt for that particular day.

### Category

Add/Delete/Show custom categories

1. Enter the `/category` command.
2. Select an option between expense and income in which you want to see the category
3. You can perform the following operations.
   1. Show Categories which will display the existing category
   2. Add a new category
   3. Delete a category

## Discord Chat
![image](https://github.com/user-attachments/assets/cfeb6ce7-bccd-4342-b5bf-7f7db5afb5ff)

## Notes:
You can download and install the Telegram desktop application for your system from the following site: https://desktop.telegram.org/


<hr>
<p>Title:'Track My Dollar'</p>
<p>Version: '4.5'</p>
<p>Authors(Iteration 6):
<table>
  <tr>
    <td align="center"><a href="https://github.com/AnuragGorkar"><img src="https://avatars.githubusercontent.com/u/56599642?s=400&u=351897f9422f135c4df24317d3fc8a28796f58bc&v=4" width="75px;" alt=""/><br /><sub><b>Anurag Gorkar</b></sub></a></td>
    <td align="center"><a href="https://github.com/aryansharma2k2"><img src="https://avatars.githubusercontent.com/u/118040810?v=4" width="75px;" alt=""/><br /><sub><b>Aryan Iguva</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/harshvora7"><img src="https://avatars.githubusercontent.com/u/45733155?v=4" width="75px;" alt=""/><br /><sub><b>Harsh Vora</b></sub></a><br /></td>
  </tr>
</table>
<p>Description: 'An easy to use Telegram Bot to track everyday expenses'</p>

<p>Authors(Iteration 5):'Jayesh, Harsh, Sagar, Soham'</p>
<p>Authors(Iteration 4):'Anuj, Bhavesh, Jash, Vaibhavi'</p>
<p>Authors(Iteration 3):'Vraj, Alex, Leo, Prithvish, Seeya'</p>
<p>Authors(Iteration 2):'Athithya, Subramanian, Ashok, Zunaid, Rithik'</p>
<p>Authors(Iteration 1):'Dev, Prakruthi, Radhika, Rohan, Sunidhi'</p>
