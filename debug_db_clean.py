
import logging
logging.basicConfig(level=logging.WARNING) # Silence INFO logs
from models import SessionLocal, Game, User

session = SessionLocal()

print("\n\n--- DEBUG INFO ---")
game = session.query(Game).filter_by(app_id=813780).first()
if game:
    print(f"Game: {game.name}")
    print(f"Price: {game.current_price}")
    print(f"Watchers: {[u.telegram_id for u in game.watchers]}")
else:
    print("Game not found.")
print("------------------\n")

session.close()
