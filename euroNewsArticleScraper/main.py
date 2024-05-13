# FastAPI RestAPI for database object manipulation
# .
# |- main.py > RestAPI application
# | 
# |- routers > API routes/methods declaration
# |   |-manufacturer_router.py 
# |   |-panel_router.py
# |   |
# |   |-models > data models
# |      |-manufacturer.py
# |      |-panel.py

# https://www.mongodb.com/languages/python/pymongo-tutorial
# python3 -m venv env-pymongo-fastapi-crud
# source env-pymongo-fastapi-crud/bin/activate
# python -m pip install 'fastapi[all]' 'pymongo[srv]' python-dotenv
# python -m uvicorn main:app --reload

from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient

#from routers import *
#import routers

from routers.article_router import router as article_router

config = dotenv_values(".env")
MongoClient
app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["CONN_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(article_router, tags=["articles"], prefix=f"/articles")

@app.get("/")
async def root():
    return {"message": "Welcome to the PyMongo tuto!"}