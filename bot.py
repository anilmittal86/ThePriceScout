
import logging
import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from sqlalchemy.orm import Session
from models import SessionLocal, Game, User, init_db
from steam_client import fetch_game_price

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Steam Price Tracker!\n"
        "Commands:\n"
        "/add <app_id> - Track a game\n"
        "/list - List tracked games\n"
        "/remove <app_id> - Stop tracking a game"
    )

def get_db_session():
    return SessionLocal()

async def add_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /add <app_id>")
        return

    try:
        app_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Invalid App ID. It must be a number.")
        return

    telegram_id = update.effective_user.id
    session = get_db_session()

    try:
        # Get or Create User
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            user = User(telegram_id=telegram_id)
            session.add(user)
            session.commit() # Commit to get user ID
            session.refresh(user)

        # Check if game exists in DB
        game = session.query(Game).filter_by(app_id=app_id).first()
        
        if not game:
            await update.message.reply_text(f"Fetching data for App ID {app_id}...")
            game_data = await fetch_game_price(app_id)
            
            if not game_data:
                await update.message.reply_text("Could not find game on Steam. Check the App ID.")
                return

            game = Game(
                app_id=app_id,
                name=game_data['name'],
                current_price=game_data['price']
            )
            session.add(game)
            session.commit()
            session.refresh(game)
        
        # Check if already in watchlist
        if game in user.games:
             await update.message.reply_text(f"You are already tracking {game.name}.")
        else:
            user.games.append(game)
            session.commit()
            await update.message.reply_text(f"Added {game.name} (Current Price: ₹{game.current_price}) to your watchlist.")

    except Exception as e:
        logger.error(f"Error in add_game: {e}")
        await update.message.reply_text("An error occurred while adding the game.")
        session.rollback()
    finally:
        session.close()

async def list_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    session = get_db_session()

    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        
        if not user or not user.games:
            await update.message.reply_text("Your watchlist is empty.")
            return

        message = "Your Watchlist:\n"
        for game in user.games:
            message += f"• {game.name} (ID: {game.app_id}) - ₹{game.current_price}\n"
        
        await update.message.reply_text(message)

    except Exception as e:
        logger.error(f"Error in list_games: {e}")
        await update.message.reply_text("An error occurred while listing games.")
    finally:
        session.close()

async def remove_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /remove <app_id>")
        return

    try:
        app_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Invalid App ID.")
        return

    telegram_id = update.effective_user.id
    session = get_db_session()

    try:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        
        if not user:
             await update.message.reply_text("You check your watchlist is empty.")
             return

        game = session.query(Game).filter_by(app_id=app_id).first()
        
        if game and game in user.games:
            user.games.remove(game)
            session.commit()
            await update.message.reply_text(f"Removed {game.name} from your watchlist.")
        else:
            await update.message.reply_text("Game not found in your watchlist.")

    except Exception as e:
        logger.error(f"Error in remove_game: {e}")
        await update.message.reply_text("An error occurred while removing the game.")
        session.rollback()
    finally:
        session.close()

if __name__ == '__main__':
    # Initialize DB if not exists (though stage 1 did it)
    init_db()
    
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or token == "your_telegram_bot_token_here":
        print("Error: TELEGRAM_BOT_TOKEN not found in .env file.")
        exit(1)

    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('add', add_game))
    application.add_handler(CommandHandler('list', list_games))
    application.add_handler(CommandHandler('remove', remove_game))

    print("Bot is running...")
    application.run_polling()
