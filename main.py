from fastapi import FastAPI
import datetime

app = FastAPI()

user_points = 0
payer_points = {}
transactions = []

@app.get("/")
async def root():
    return "Hello World :)"
