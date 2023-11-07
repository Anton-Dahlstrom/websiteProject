from sqlalchemy import Column, Integer, String, text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class User(Base):
    __tablename__ = "users"    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_time = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text('NOW()'))
    

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, nullable=False)
    created_time = Column(TIMESTAMP(timezone=True), nullable=False,
                    server_default=text('NOW()'))
    hometeam = Column(String, nullable=False)
    awayteam = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)

class Odds(Base):
    __tablename__ = "odds"
    __allow_unmapped__ = True
    id = Column(String, primary_key=True, nullable=False)
    sport_title = Column(String, nullable=False)
    commence_time = Column(DateTime, nullable=False)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    home_odds = Column(Float, nullable=True)
    away_odds = Column(Float, nullable=True)
    draw_odds = Column(Float, nullable=True)


class Bet(Base):
    __tablename__ = "bets"
    id = Column(Integer, primary_key=True, nullable=False)
    created_time = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text('NOW()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    stake = Column(Integer, nullable=False)
    outcome = Column(String, nullable=False)
    odds = Column(Float, nullable=False)
    owner = relationship("User")
    event = relationship("Event")

class Update(Base):
        __tablename__ = "updates"
        updated = Column(DateTime, primary_key=True, nullable=False)
        next_update = Column(DateTime, nullable=False)
        api_source = Column(String)