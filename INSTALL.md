## 🚀 Installation Guide for TrackMyDollar BOTGo

Follow these instructions to set up the TrackMyDollar BOTGo on your local system in a few minutes.

### Step 1: Clone Repository
1. Open a terminal.
2. Clone this repository to your local system:
   ```bash
   git clone https://github.com/CSC510SEFALL2024/MyDollarBot-BOTGo/tree/addedfeatures101
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
