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


@app.post("/payer_transactions", status_code=200)
def add_transaction(transaction: PayerTransaction):

  validate_transaction(transaction, payer_points)
  return process_transaction(transactions, transaction, payer_points)

def process_transaction(transactions, transaction, payer_points):
  user.total_points += transaction.points

  if transaction.points > 0:
    if transaction.payer not in payer_points:
      payer_points[transaction.payer] = 0
    payer_points[transaction.payer] += transaction.points
    transactions.append(transaction)
    transactions.sort(key=lambda date: date.timestamp, reverse=True)

    return payer_points

  else:
    remove_counter = 0
    transIdx = len(transactions) - 1
    last_trans = transactions[transIdx]
    while transaction.points < 0:
      if abs(last_trans.points) > abs(transaction.points):
        transactions[transIdx].points += transaction.points
        payer_points[transaction.payer] += transaction.points
        transaction.points = 0
      else:
        payer_points[transaction.payer] -= last_trans.points
        transaction.points += last_trans.points
        remove_counter += 1
        transIdx -= 1

    while remove_counter > 0:
      transactions.pop()
      remove_counter -= 1

    return payer_points

def validate_transaction(transaction, payer_points):
  if (transaction.payer not in payer_points and transaction.points < 0) or (transaction.payer in payer_points and payer_points[transaction.payer] + transaction.points < 0):
    raise HTTPException(status_code=422,
    detail=f'ERROR: Unable to add transaction; payer balance cannnot go negative. {transaction.payer} has {payer_points[transaction.payer] if transaction.payer in payer_points else 0} points in account.')
  if transaction.points == 0:
    raise HTTPException(status_code=422,
    detail=f'ERROR: Unable to add transaction; Points must be positive or negative integer.')


@app.post("/spend", status_code=200)
def spend_payer_points(spend: SpendPoints):
  validate_spend(spend.points, user.total_points)
  user.total_points -= spend.points
  return process_spend(spend.points, transactions, payer_points)


def process_spend(spend, transactions, payer_points):
  spent = {}
  transaction_remove_counter = 0
  transIdx = len(transactions) - 1

  while spend > 0:
    transaction = transactions[transIdx]
    trans_pts = transaction.points

    if trans_pts > spend:
      if payer_points[transaction.payer] >= spend:
        payer_points[transaction.payer] -= spend
        if transaction.payer not in spent:
          spent[transaction.payer] = 0
        spent[transaction.payer] -= spend
        transaction.points -= spend
        spend = 0
      else:
        spend -= payer_points[transaction.payer]
        if transaction.payer not in spent:
          spent[transaction.payer] = 0
        spent[transaction.payer] -= payer_points[transaction.payer]
        payer_points[transaction.payer] = 0
        transaction_remove_counter += 1
        transIdx -= 1

    elif trans_pts <= spend:

      if payer_points[transaction.payer] >= trans_pts:
        payer_points[transaction.payer] -= trans_pts
        if transaction.payer not in spent:
          spent[transaction.payer] = 0
        spent[transaction.payer] -= trans_pts
        spend -= trans_pts
        transaction_remove_counter += 1
        transIdx -= 1
      else:
        spend -= payer_points[transaction.payer]
        if transaction.payer not in spent:
          spent[transaction.payer] = 0
        spent[transaction.payer] -= payer_points[transaction.payer]
        payer_points[transaction.payer] = 0
        transaction_remove_counter += 1
        transIdx -= 1

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
