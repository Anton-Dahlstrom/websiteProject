from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from ..database import get_db
from starlette.templating import Jinja2Templates
from ..import models, schemas, utils, oauth2

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




# @router.post("/login", response_class=HTMLResponse)
# def get_login(request:Request):
#     context = {"request": request}
#     return template.TemplateResponse("register.html",context)