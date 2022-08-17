from fastapi import FastAPI

from db.utils import init_db, create_all_tables

from .routers import locations, profiles

init_db(user='user', password='password', host='localhost', database='bunnyfood_dev')
create_all_tables()

app = FastAPI()

app.include_router(locations.router)
app.include_router(profiles.router)
