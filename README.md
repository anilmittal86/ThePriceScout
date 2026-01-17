
# The Price Scout 🎮📉

**The Price Scout** is a personal Telegram bot (found at **@ThepriceScoutBot**) that tracks Steam game prices in India (INR) and notifies you immediately when a price drop occurs.

It is designed to run locally on your laptop or on a low-cost cloud server, ensuring you never miss a sale on your favorite games.

## ✨ Features
- **🔍 Smart Scraper**: Fetches real-time prices from Steam's API (handles rate limits automatically).
- **🤖 Telegram Bot**:
    - `/add <app_id>`: Add a game to your watchlist (e.g., `813780` for Age of Empires II).
    - `/list`: View all games you are tracking and their current prices.
    - `/remove <app_id>`: Remove a game from tracking.
- **⏰ Automatic Scheduler**: Checks for price drops every day at **10:00 AM** (and on startup).
- **💾 Local Database**: Uses SQLite (`steam_tracker.db`) to store your watchlist efficiently.

## 🚀 Setup Guide

### prerequisites
- Python 3.8 or higher.
- A Telegram Bot Token (Get one from [@BotFather](https://t.me/BotFather)).

### Installation
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/anilmittal86/ThePriceScout.git
    cd ThePriceScout
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**
    - Create a file named `.env` in the project folder.
    - Add your Telegram Bot Token inside it:
      ```text
      TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrstUVwxyz
      ```

## 🎮 How to Use

### Run Locally (Manual)
To start the bot, simply run:
```bash
python main.py
```
*Keep the terminal window open.*

### Run Locally (Automatic / Background)
If you want the bot to run automatically when you turn on your PC:
1.  Locate `start_bot.bat` in the project folder.
2.  Press `Win + R`, type `shell:startup`, and press Enter.
3.  Create a **Shortcut** to `start_bot.bat` inside this startup folder.
4.  That's it! The bot will now start silently in the background every time you boot up.

## 📱 Telegram Commands
- **Start**: `/start`
- **Add Game**: `/add <steam_app_id>`
    - *Example*: `/add 813780` (Find ID in the URL: `store.steampowered.com/app/813780/...`)
- **List Games**: `/list`
- **Remove Game**: `/remove <steam_app_id>`

## 🛠️ Tech Stack
- **Language**: Python
- **Bot Framework**: `python-telegram-bot`
- **Scheduling**: `APScheduler`
- **Database**: `SQLAlchemy` (SQLite)
- **HTTP Client**: `httpx`

---
*Happy Gaming & Saving!* 💸
