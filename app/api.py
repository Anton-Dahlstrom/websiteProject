
import json
from . import schemas, models, database
from .database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, Depends
from datetime import timedelta, datetime
from .config import settings
import requests 

api_key = settings.api_key
sport = "soccer_sweden_allsvenskan"
region = "eu"
markets = "h2h"
url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={api_key}&regions={region}&markets={markets}"

bookmaker = "pinnacle"

def addUpdateTimeToDB(db):
    update = models.Update()
    currentTime = datetime.now()
    next_update = currentTime + timedelta(hours=23)
    update.updated = currentTime
    update.next_update = next_update
    update.api_source = bookmaker
    db.add(update)
    db.commit()
    db.refresh(update) 

def timeForNextUpdate(db):
    last_update = db.query(models.Update).order_by(models.Update.updated.desc()).limit(1).first()
    if last_update:
        return last_update.next_update
    else:
        return None

def update_matches():
    with SessionLocal() as db:
            next_update = timeForNextUpdate(db)
            if next_update == None or datetime.now() > next_update:
                r = requests.get(url)
                data = r.json()
                events = schemas.Model(data)
                addUpdateTimeToDB(db)
                for event in events.root:
                    for bookmaker in event.bookmakers:
                        if bookmaker.key == bookmaker:
                            for market in bookmaker.markets:
                                for outcome in market.outcomes:
                                    if event.home_team == outcome.name:
                                        event.home_odds = outcome.price
                                    elif event.away_team == outcome.name:
                                        event.away_odds = outcome.price
                                    elif outcome.name == "Draw":
                                        event.draw_odds = outcome.price
                    
                    schema = schemas.OddsCreate(**event.model_dump())
                    new_event = models.Odds(**schema.model_dump())
                    event_exists = db.query(models.Odds).filter(models.Odds.id == new_event.id).first()
                    if not event_exists:
                        new_event.commence_time += timedelta(hours=2)
                        db.add(new_event)
                        db.commit()
                    else:
                        event_exists.home_odds = new_event.home_odds
                        event_exists.away_odds = new_event.away_odds
                        event_exists.draw_odds = new_event.draw_odds
                        db.commit()    


        # print(next)
    # if t > next:
    #     update_matches()
    #     with open("app/next_import.txt", "w") as file:
    #         next_update = t + timedelta(hours=23)
    #         file.write(str(next_update))


# -- For future optimization --     
          
#     temp = [bookmaker for event.bookmakers in events for bookmaker in event.bookmakers]
#     temp = [bookmaker for event in events.root for bookmaker in event.bookmakers if bookmaker.key=="sport888"]
#     temp = [market.outcomes for event in events.root for bookmaker in event.bookmakers if bookmaker.key=="sport888" for market in bookmaker.markets]
#     temp = [outcome for event in events.root for bookmaker in event.bookmakers if bookmaker.key=="sport888" for market in bookmaker.markets for outcome in market.outcomes]
#     temp = [market.outcomes for market in bookmaker.markets for bookmaker in event.bookmakers if bookmaker.key=="sport888" for event in events.root]
#     print(temp)