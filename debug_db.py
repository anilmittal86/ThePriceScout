
from models import SessionLocal, Game, User

session = SessionLocal()

print("--- DEBUG INFO ---")
# Check Game
game = session.query(Game).filter_by(app_id=813780).first()
if game:
    print(f"Game: {game.name} (ID: {game.app_id})")
    print(f"Current Price in DB: {game.current_price}")
    print(f"Watchers: {[u.telegram_id for u in game.watchers]}")
else:
    print("Game 813780 not found in DB.")

# Check Users
users = session.query(User).all()
print(f"All Users: {[u.telegram_id for u in users]}")

session.close()
