from sqlite3 import Timestamp
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class PayerTransaction(BaseModel):
  payer: str
  points: int
  timestamp: datetime

class UserSpend(BaseModel):
  points: int

total_points = 0
payer_points = {}
transactions = []


@app.get("/point_balance")
def get_payer_points():
    return payer_points

@app.post("/payer_transactions")
def add_transaction(transaction: PayerTransaction):
  pass

@app.post("/spending")
def spend_payer_points(spend: UserSpend):
  pass
