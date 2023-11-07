from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from . import emails
from ..import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/user",
    tags=['user']
)
template = Jinja2Templates(directory="templates")


@router.get("/register", response_class=HTMLResponse)
def get_register(request:Request):
    context = {"request": request}
    return template.TemplateResponse("register.html",context)

@router.post("/register", response_class=HTMLResponse)
def post_register(request: Request, user: schemas.UserCreate = Depends(schemas.UserCreate.from_form), 
                   db: Session = Depends(get_db)):    
    context = {"request": request, "feedback": "User creation failed.", "user": "nobody", "login": False}
    if db.query(models.User).filter(models.User.username == user.username).first():
        context["feedback"] = "Username already exists."
    else:
        print(user.email)
        validation = user.validate()
        context["feedback"] = validation["feedback"]
        if validation["validated"]:
            hashed_password = utils.hash(user.password)
            user.password = hashed_password
            new_user = models.User(**user.model_dump(exclude={"passwordconfirm"}))
            db.add(new_user)
            db.commit()
            db.refresh(new_user)        
            context["user"] = user.username
            context["login"] = True
            return template.TemplateResponse("index.html", context )
    return template.TemplateResponse("register.html", context )

@router.get("/reset_password", response_class=HTMLResponse)
def reset_password(request: Request):
    context = {"request": request, "login": False}
    response = template.TemplateResponse("resetpassword.html", context)
    return response

@router.post("/reset_password", response_class=HTMLResponse)
async def reset_password(request: Request, email: str = Form(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    context = {"request": request, "feedback": "Could not find email.", "login": False}
    if user:
        access_token = oauth2.create_access_token(data={"user_id": user.id})
        url = request.url_for("get_new_password")
        url_with_header = f"{url}?access_token={access_token}"
        context["feedback"] = "Check your inbox for a reset link."
        await emails.send_reset_mail([email], url_with_header)
    response = template.TemplateResponse("resetpassword.html", context)
    return response