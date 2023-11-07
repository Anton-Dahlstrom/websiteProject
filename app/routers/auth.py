from fastapi import APIRouter, Depends, status, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, utils, oauth2
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from ..database import get_db

router = APIRouter(tags=['authentication'])
template = Jinja2Templates(directory="templates")

@router.get("/login", response_class=HTMLResponse)
def get_login(request:Request):
    context = {"request": request, "remember": ""}
    remember = request.cookies.get("Rememberme")
    if remember:
        context["remember"] = remember
    return template.TemplateResponse("login.html",context)

@router.post("/login", response_class=RedirectResponse)
def login(request: Request, rememberme: bool = Form(False), user_credentials: OAuth2PasswordRequestForm = Depends(), 
          db: Session = Depends(get_db)):    
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    redirect_url = request.url_for("index")
    if not user or not utils.verify(user_credentials.password, user.password):
        context = {"request": request, "feedback": "Incorrect username or password."}
        response = template.TemplateResponse("login.html", context)
        return response
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    response = RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="Authorization", value=access_token, httponly=True)
    response.headers["user"] = user.username
    if rememberme:
        response.set_cookie(key='Rememberme', value=user_credentials.username)
    else:
        if request.cookies.get("Rememberme"):
            response.delete_cookie("Rememberme")
    return response

@router.get("/logout", response_class=HTMLResponse)
def logout(request: Request):
    context = {"request": request, "login": False}
    response = template.TemplateResponse("index.html", context)
    response.delete_cookie("Authorization")
    return response


@router.get("/new_password", response_class=HTMLResponse)
def get_new_password(request:Request, access_token: str):
    context = {"request": request,"login": False}
    id = oauth2.verify_access_token(access_token)
    if id:
        context["login"] = True
        response = template.TemplateResponse("newpassword.html",context)
        response.set_cookie(key="Authorization", value=access_token, httponly=True)
    return response

@router.post("/new_password", response_class=HTMLResponse)
def post_new_password(request:Request, newpassword: str = Form(), passwordconfirm: str = Form(), db: Session = Depends(get_db)):
    context = {"request": request, "login": False, "feedback": "Your password has been changed!"}
    if newpassword == passwordconfirm:

        id = oauth2.verify_cookie(request)
        if id:
            context["login"] = True
            hashed_password = utils.hash(newpassword)
            user = db.query(models.User).filter(models.User.id == id)
            user.update({models.User.password: hashed_password})
            db.commit()
            user.password = utils.hash(newpassword)
        else: context["feedback"] = "Something went wrong, your token might have expired."
    else: context["feedback"] = "Passwords must match!"
    return template.TemplateResponse("newpassword.html",context)