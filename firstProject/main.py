from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from routes.route import router as todo_router
from routes.auth import router as auth_router

app = FastAPI()

app.include_router(todo_router)
app.include_router(auth_router)


# app.get("/")
# def say_hello():
#     return "Hello, Namasthe"