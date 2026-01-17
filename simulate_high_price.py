
from models import SessionLocal, Game

def set_high_price():
    session = SessionLocal()
    app_id = 813780 # Age of Empires II: DE
    
    game = session.query(Game).filter_by(app_id=app_id).first()
    if game:
        print(f"Current Price: {game.current_price}")
        game.current_price = 5000.0
        session.commit()
        print(f"New Artificial Price: {game.current_price}")
    else:
        print("Game not found!")
    
    session.close()

if __name__ == "__main__":
    set_high_price()
