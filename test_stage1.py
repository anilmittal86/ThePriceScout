
import asyncio
from steam_client import fetch_game_price
from models import init_db, SessionLocal, Game
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_stage1():
    print("--- STEP 1: Initialize Database ---")
    init_db()
    print("Database initialized successfully.\n")

    print("--- STEP 2: Fetch Game Data ---")
    app_id = 813780  # Age of Empires II: DE
    print(f"Fetching data for App ID: {app_id}...")
    
    game_data = await fetch_game_price(app_id)
    
    if not game_data:
        print("Failed to fetch game data.")
        return

    print(f"Fetched Data: {game_data}\n")

    print("--- STEP 3: Save to Database ---")
    session = SessionLocal()
    
    try:
        # Check if game exists
        existing_game = session.query(Game).filter_by(app_id=app_id).first()
        
        if existing_game:
            print("Game already exists, updating...")
            existing_game.name = game_data['name']
            existing_game.current_price = game_data['price']
            # existing_game.last_updated is updated automatically if we set it up that way, 
            # but let's force update it or leave it to default if it's new.
            from datetime import datetime
            existing_game.last_updated = datetime.utcnow()
        else:
            print("Creating new game entry...")
            new_game = Game(
                app_id=app_id,
                name=game_data['name'],
                current_price=game_data['price']
            )
            session.add(new_game)
        
        session.commit()
        print("Game saved to database successfully.\n")

        print("--- STEP 4: Verify Data ---")
        saved_game = session.query(Game).filter_by(app_id=app_id).first()
        print(f"Retrieved from DB: {saved_game}")
        
    except Exception as e:
        print(f"Error saving to DB: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    asyncio.run(test_stage1())
