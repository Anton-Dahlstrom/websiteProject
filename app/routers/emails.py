from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from ..schemas import EmailSchema
from ..config import settings


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
<h1>Password reset<h1>
<p>Follow the link below to reset your password.</p> 
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
