
from models import init_db, SessionLocal, Game

session = SessionLocal()
games = session.query(Game).all()
print(f"Total Games found: {len(games)}")
for game in games:
    print(f"ID: {game.id}, AppID: {game.app_id}, Name: {game.name}, Price: {game.current_price}")
session.close()
