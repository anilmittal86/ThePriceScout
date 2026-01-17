
import asyncio
import json
import os
import logging
from telegram import Bot
from steam_client import fetch_game_price
from dotenv import load_dotenv

# Load env (for local testing), GitHub Actions uses Secrets
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_check():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        logger.error("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")
        return

    bot = Bot(token=token)
    
    # Load games
    try:
        with open("games.json", "r") as f:
            games = json.load(f)
    except FileNotFoundError:
        logger.error("games.json not found")
        return

    for game in games:
        app_id = game["app_id"]
        name = game["name"]
        
        logger.info(f"Checking {name} ({app_id})...")
        data = await fetch_game_price(app_id)
        
        if not data:
            logger.error(f"Failed to fetch {name}")
            continue

        current_price = data['price']
        
        # Simple Alert Logic:
        # If the price is anything less than the 'target_price' defined in json, alert me.
        # OR you can just alert on ANY drop if you store previous price. 
        # For simplicity in GitHub Actions (stateless), we'll alert if price > 0.
        
        message = (
            f"🎮 *{name}*\n"
            f"Current Price: ₹{current_price}\n"
        )
        
        # Optional: Start Logic (Only alert if price is good, or just daily report)
        # For now, we send a daily report of the price.
        
        await bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

if __name__ == "__main__":
    asyncio.run(run_check())
