from fastapi import Query, Form
from pydantic import BaseModel, RootModel, validator, EmailStr
import datetime



class EmailSchema(BaseModel):
    email: list[EmailStr]

class BetBase(BaseModel):
    team1: str
    team2: str
    odds_team1: float
    odds_team2: float
    start: datetime.datetime

class UserCreate(BaseModel):
    username: str | None = None
    password: str | None = None 
    passwordconfirm: str | None = None
    email: str | None = None

    @classmethod
    def from_form(
        cls,
        email: str = Form(""),
        username: str = Form(""),
        password: str = Form(""),
        passwordconfirm: str = Form("")):        
        return cls(email=email, username=username, password=password, passwordconfirm=passwordconfirm)
    
    def validate(self):
        if not len(self.username) > 2:
            return {"validated": False, "feedback": "username too short"}  
        elif not len(self.password) > 3:
            return {"validated": False, "feedback": "password too short"} 
        elif not self.password == self.passwordconfirm:
             return {"validated": False, "feedback": "passwords don't match"}
        else:
             return {"validated": True, "feedback": "User created"}



class UserLogin(BaseModel):
     username : str
     password : str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str | None = None


class OddsMatch(BaseModel):
    name: str
    price: float


class OddsCreate(BaseModel):
    id: str
    sport_title: str
    commence_time: datetime.datetime
    home_team: str
    away_team: str
    home_odds: float | None = None 
    away_odds: float | None = None 
    draw_odds: float | None = None 


# Models for external api, automatically made with https://jsontopydantic.com/

class Outcome(BaseModel):
    name: str
    price: float


class Market(BaseModel):
    key: str
    last_update: str
    outcomes: list[Outcome]


class Bookmaker(BaseModel):
    key: str
    title: str
    last_update: str
    markets: list[Market]


class Match(BaseModel):
    id: str
    # sport_key: str
    sport_title: str
    commence_time: str
    home_team: str
    away_team: str
    home_odds: float | None = None
    away_odds: float | None = None
    draw_odds: float | None = None
    bookmakers: list[Bookmaker]


class MatchList(RootModel):
    root: list[Match]