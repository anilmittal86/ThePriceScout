
import logging
# Force disable all logging
logging.disable(logging.CRITICAL)
from models import SessionLocal, Game

session = SessionLocal()
with open("db_status.txt", "w") as f:
    game = session.query(Game).filter_by(app_id=813780).first()
    if game:
        f.write(f"Price: {game.current_price}\n")
        f.write(f"Watchers: {len(game.watchers)}\n")
    else:
        f.write("Game not found\n")
session.close()
