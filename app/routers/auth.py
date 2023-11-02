from fastapi import APIRouter, Depends, status, HTTPException, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models, utils, oauth2
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
    print(redirect_url)
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

@router.get("/reset_password", response_class=HTMLResponse)
def reset_password(request: Request):
    context = {"request": request, "login": False}
    response = template.TemplateResponse("resetpassword.html", context)
    return response

@router.post("/reset_password", response_class=HTMLResponse)
def reset_password(request: Request, email: str = Form(), db: Session = Depends(get_db)):
    email = db.query(models.User).filter(models.User.email == email).first()
    context = {"request": request, "feedback": "Could not find email.", "login": False}
    if email:
        context["feedback"] = "Check your inbox for a reset link."
    # send actual email
    response = template.TemplateResponse("resetpassword.html", context)
    return response