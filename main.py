from sqlite3 import Timestamp
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class Transaction(BaseModel):
  payer: str
  points: int
  timestamp: datetime

user_points = 0
payer_points = {}
transactions = []


@app.get("/")
def get_payer_points():
    return payer_points

@app.post("/transactions")
def add_transaction():
  pass

@app.post("/spending")
def spend_payer_points():
  pass
