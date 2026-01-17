
import logging
from telegram.ext import Application
from models import SessionLocal, Game
from steam_client import fetch_game_price

logger = logging.getLogger(__name__)

async def check_prices(context):
    """
    Background task to check for price drops.
    This function is called by the job queue.
    """
    logger.info("Starting price check job...")
    print("DEBUG: Starting price check job...")
    
    session = SessionLocal()
    try:
        games = session.query(Game).all()
        
        for game in games:
            logger.info(f"Checking price for {game.name} ({game.app_id})...")
            
            # Fetch fresh data
            new_data = await fetch_game_price(game.app_id)
            
            if not new_data:
                logger.warning(f"Could not fetch data for {game.name}")
                continue
            
            new_price = new_data['price']
            
            # Check for price drop
            # Note: We compare < current_price.
            # You might want to handle the case where current_price is None or 0 differently.
            if game.current_price is not None and new_price < game.current_price:
                drop_amount = game.current_price - new_price
                percent = (drop_amount / game.current_price) * 100
                
                logger.info(f"Price Drop detected for {game.name}! {game.current_price} -> {new_price}")
                
                # Notify users
                message = (
                    f"🚨 *Price Drop Alert!* 🚨\n\n"
                    f"**{game.name}**\n"
                    f"Old Price: ₹{game.current_price}\n"
                    f"New Price: ₹{new_price}\n"
                    f"Drop: ₹{drop_amount:.2f} ({percent:.0f}%)"
                )
                
                for user in game.watchers:
                    try:
                        # context.bot is available in job queue callback
                        await context.bot.send_message(chat_id=user.telegram_id, text=message, parse_mode='Markdown')
                        logger.info(f"Notification sent to {user.telegram_id}")
                    except Exception as e:
                        logger.error(f"Failed to send message to {user.telegram_id}: {e}")
            
            # Update price in DB regardless of drop (to keep it current)
            game.current_price = new_price
            from datetime import datetime
            game.last_updated = datetime.utcnow()
            session.commit()
            
    except Exception as e:
        logger.error(f"Error in check_prices: {e}")
        session.rollback()
    finally:
        session.close()
    
    logger.info("Price check job finished.")
