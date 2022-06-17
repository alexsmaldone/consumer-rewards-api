from sqlite3 import Timestamp
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class PayerTransaction(BaseModel):
  payer: str
  points: int
  timestamp: datetime



total_points = 0
payer_points = {}
transactions = []


@app.get("/")
def get_payer_points():
    return payer_points



# need to create transaction and add to transactions list
# add to payer point balance if payer exists, otherwise create payer
@app.post("/payer_transactions")
def add_transaction(transaction: PayerTransaction):
  transactions.append(transaction)

  if transaction.name not in payer_points:
    payer_points[transaction.payer] = 0
  payer_points[transaction.payer] += transaction.points

  return "Transaction posted"

@app.post("/spending")
def spend_payer_points(points: int):
  pass
