
import logging
import os
import asyncio
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from bot import start, add_game, list_games, remove_game
from scheduler import check_prices
from models import init_db

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    # Initialize DB
    init_db()
    
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found in .env")
        return

    # Build Application
    application = ApplicationBuilder().token(token).build()
    
    # Register Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('add', add_game))
    application.add_handler(CommandHandler('list', list_games))
    application.add_handler(CommandHandler('remove', remove_game))
    
    # Setup Job Queue
    job_queue = application.job_queue
    
    # Run every day at 10:00 AM
    from datetime import time
    
    # Run daily at 10:00 AM
    # Note: If the computer is off at 10 AM, it will miss the job until the next day.
    job_queue.run_daily(check_prices, time=time(hour=10, minute=0))

    # Also run once 10 seconds after startup/restart to ensure we check at least once today
    job_queue.run_once(check_prices, 10)
    
    logger.info("Bot and Scheduler started. Checking prices every 60 seconds.")
    
    # Run
    application.run_polling()

if __name__ == "__main__":
    main()
