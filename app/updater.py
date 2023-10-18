import time, requests, sched
from pydantic import BaseModel
from datetime import datetime, timedelta

from . import api


def update():
    t = datetime.now()
    with open("app/next_import.txt", "r") as file:
        last_update = file.read()
        next = datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S.%f')
    if t > next:
        api.update_matches()
        with open("app/next_import.txt", "w") as file:
            next_update = t + timedelta(hours=23)
            file.write(str(next_update))