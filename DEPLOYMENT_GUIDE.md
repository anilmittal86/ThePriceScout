
# Deployment Guide: PythonAnywhere

Since you want the bot to run continuously from your Git repository, **PythonAnywhere** is the best choice. It allows you to "clone" your code from GitHub and run it in the cloud.

## Prerequisites
- Your GitHub Repo: `https://github.com/anilmittal86/ThePriceScout`
- Your Telegram Bot Token

## Step 1: Account Setup
1.  Go to [pythonanywhere.com](https://www.pythonanywhere.com/) and sign up for a **Beginner (Free)** account.

## Step 2: Get the Code
1.  On your Dashboard, go to **Consoles**.
2.  Click **Bash** to open a terminal.
3.  Type the following commands:
    ```bash
    git clone https://github.com/anilmittal86/ThePriceScout.git
    cd ThePriceScout
    ```

## Step 3: Install Dependencies
1.  Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
2.  Install the libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Step 4: Configure the Token
Since `.env` is hidden from Git/GitHub for security, you must recreate it.
1.  In the console, type:
    ```bash
    nano .env
    ```
2.  Paste your token line:
    ```text
    TELEGRAM_BOT_TOKEN=123456789:YourActualTokenFromBotFather
    ```
    *(Right-click to Paste in the browser console)*
3.  Press `Ctrl+X`, then `Y`, then `Enter` to save.

## Step 5: Run It!
1.  Start the bot:
    ```bash
    python main.py
    ```

## Important Notes for Free Tier
- **Console Closing**: On the free tier, consoles might close after a long period of inactivity. You may need to log in occasionally to check if it's running.
- **Always On**: To have it restart automatically 24/7 ("Always On task"), you would need their $5/month plan.
- **Database**: Your database (`steam_tracker.db`) will be created in the cloud. It is **separate** from the one on your laptop. You will need to `/add` your games again.

## Alternative: Local Windows Startup
If you prefer to run it on your own laptop for free without worry:
1.  I have created a file `start_bot.bat` in your folder.
2.  Press `Win + R`, type `shell:startup`, and press Enter.
3.  Right-click `start_bot.bat` -> **Create Shortcut**.
4.  Drag the **Shortcut** into the Startup folder.
5.  Now the bot starts automatically whenever you turn on your PC!
