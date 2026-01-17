
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
    
    # Run every 24 hours (86400 seconds)
    job_queue.run_repeating(check_prices, interval=86400, first=10)
    
    logger.info("Bot and Scheduler started. Checking prices every 60 seconds.")
    
    # Run
    application.run_polling()

if __name__ == "__main__":
    main()
