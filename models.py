
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
import os

Base = declarative_base()

# Association table for Watchlist (Many-to-Many between User and Game)
watchlist_association = Table(
    'watchlist', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('game_id', Integer, ForeignKey('games.id'))
)

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    app_id = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    current_price = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Game(name='{self.name}', app_id={self.app_id}, price={self.current_price})>"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    
    # Relationship to games via watchlist
    games = relationship("Game", secondary=watchlist_association, backref="watchers")

    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id})>"

# Database initialization
DATABASE_URL = "sqlite:///steam_tracker.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
