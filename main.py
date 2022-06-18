from concurrent.futures import process
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class PayerTransaction(BaseModel):
  payer: str
  points: int
  timestamp: datetime = datetime.now()

class SpendPoints(BaseModel):
  points: int

class User():
  total_points = 0
  def __init__(self, total_points=0):
    self.total_points = total_points


user = User()
payer_points = {}
transactions = []


@app.get("/")
def get_payer_points():
    return payer_points

# DELETE THIS LATER
@app.get("/transactions", status_code=200)
def get_payer_points():
    return transactions



# need to create transaction and add to transactions list
# add to payer point balance if payer exists, otherwise create payer
@app.post("/payer_transactions", status_code=200)
def add_transaction(transaction: PayerTransaction):

  validate_transaction(transaction, payer_points)

  if transaction.payer not in payer_points:
    payer_points[transaction.payer] = 0
  payer_points[transaction.payer] += transaction.points
  user.total_points += transaction.points

  transactions.append(transaction)
  transactions.sort(key=lambda date: date.timestamp, reverse=True)
  return [payer_points, user.total_points]

def validate_transaction(transaction, payer_points):
  if (transaction.payer not in payer_points and transaction.points < 0) or (transaction.payer in payer_points and payer_points[transaction.payer] + transaction.points < 0):
    raise HTTPException(status_code=422,
    detail=f'ERROR: Unable to add transaction; payer balance cannnot go negative. {transaction.payer} has {payer_points[transaction.payer] if transaction.payer in payer_points else 0} points in account.')
  if transaction.points == 0:
    raise HTTPException(status_code=422,
    detail=f'ERROR: Unable to add transaction; Points must be positive or negative integer.')




# check if spend is greater than amount of total points for User, return error if >
# iterate backward over transactions
  # negative transaction point:
    # if enough in payer_points
      # logic here
    # not enough in payer points
      # logic here
  # positive transaction points
    # if enough in payer_points
      # logic here
    # not enough in payer points
      # logic here
  # add payer and negative points taken to payer list

# return list of dicts with payer and points subtracted from payer
@app.post("/spend", status_code=200)
def spend_payer_points(spend: SpendPoints):
  validate_spend(spend.points, user.total_points)
  user.total_points -= spend.points
  return process_spend(spend.points, transactions, payer_points)


def process_spend(spend, transactions, payer_points):
  spent = {}
  transaction_remove_counter = 0
  counter = len(transactions) - 1



  while spend > 0:
    pass






  while transaction_remove_counter > 0:
    transactions.pop()
    transaction_remove_counter -= 1

  return spent

def validate_spend(spend, user_points):
  if spend > user_points:
    raise HTTPException(status_code=422,
    detail=f'ERROR: Only {user_points} points available to spend')
  if spend <= 0:
    raise HTTPException(status_code=422,
    detail=f'ERROR: Points spend must be greater than 0.')
  pass



  return {"points": user.total_points}
