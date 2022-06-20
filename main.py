from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from datetime import datetime
from route_functions import validate_transaction, process_transaction, validate_spend, process_spend

app = FastAPI()

class PayerTransaction(BaseModel):
  payer: str
  points: int
  timestamp: datetime = datetime.now()

class SpendPoints(BaseModel):
  points: int

class User():
  def __init__(self, total_points=0):
    self.total_points = total_points


user = User()
payer_points = {}
transactions = []


@app.get("/points")
def get_payer_points():

    return payer_points

@app.get("/transactions", status_code=200)
def get_transactions():

    return transactions

@app.post("/points", status_code=200)
def add_transaction(transaction: PayerTransaction):

  validate_transaction(transaction, payer_points)
  return process_transaction(transactions, transaction, payer_points)

@app.post("/spend", status_code=200)
def spend_payer_points(spend: SpendPoints):

  validate_spend(spend.points, user.total_points)
  user.total_points -= spend.points
  return process_spend(spend.points, transactions, payer_points)
