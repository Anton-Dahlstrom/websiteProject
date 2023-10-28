from fastapi import FastAPI, HTTPException, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routers import matches, users, auth
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from . import oauth2, api
import sched, time
from threading import Thread

app = FastAPI()

s = sched.scheduler(time.time, time.sleep)

def print_event(sc=None): 
    api.update_matches()
    sc.enter(84600, 1, print_event, (sc,))
    sc.run()


@app.on_event("startup")
async def startup_event():
    # thread = Thread(target=updater.printer(), kwargs=dict(sc=s))
    # thread.start()
    thread = Thread(target=print_event, kwargs=dict(sc=s))
    thread.start()


# Directs jinja to our HTML templates
template = Jinja2Templates(directory="templates")

# Mounts our static folder so Jinja can find our CSS.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Determines which domains, http methods, headers etc. are allowed to connect.
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Adds our routers.
app.include_router(matches.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def index(request: Request):
    context = {"request": request, "login": False}
    id = oauth2.verify_cookie(request)
    if id:
        context["login"] = True
    response = template.TemplateResponse("index.html", context)
    return response

@app.get("/about")
def about(request: Request):
    context = {"request": request, "userlink": "user", "login": False}
    id = oauth2.verify_cookie(request)
    if id:
        context["login"] = True
    return template.TemplateResponse("about.html", context)