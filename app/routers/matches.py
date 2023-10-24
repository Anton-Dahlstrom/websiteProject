from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from ..database import get_db
from starlette.templating import Jinja2Templates
from ..import models, schemas, oauth2
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/matches",
    tags=['matches']
)
template = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def get_matches(request: Request, db: Session = Depends(get_db)):
    matches = db.query(models.Odds).filter(models.Odds.commence_time > datetime.now()).order_by(models.Odds.commence_time.asc()).all()
    context = {"request": request,"login": False, "matches": matches}
    id = oauth2.verify_cookie(request)
    if id:
        context["login"] = True
    return template.TemplateResponse("matches.html", context )
