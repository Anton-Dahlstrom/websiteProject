from typing import List

from fastapi import BackgroundTasks, FastAPI, APIRouter
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from ..schemas import EmailSchema
from starlette.responses import JSONResponse
from ..config import settings
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter(tags=['Email'])


conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


html = """
<h1>testing<h1>
<p>Thanks for using Fastapi-mail</p> 
"""

async def send_reset_mail(email: EmailSchema, url: str):
    body = html + f'<a><a href="{url}">Click here to reset your password</a><a>'
    message = MessageSchema(
        subject="Reset Password",
        recipients=email,
        body=body,
        subtype=MessageType.html)
    fm = FastMail(conf)
    await fm.send_message(message)
    return "worked"

@router.post("/reset_password", response_class=RedirectResponse)
async def reset(email: EmailSchema):
    message = MessageSchema(
        subject="Reset Password",
        recipients=email,
        body=html,
        subtype=MessageType.html)
    
    fm = FastMail(conf)
    await fm.send_message(message)
    return "worked" 

@router.post("/confirm_email", response_class=RedirectResponse)
async def confirm(email: EmailSchema):
    message = MessageSchema(
        subject="Confirm Email",
        recipients=email,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return "worked" 