from wsgiref import validate
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
@app.get("/transactions")
def get_payer_points():
    return transactions



# need to create transaction and add to transactions list
# add to payer point balance if payer exists, otherwise create payer
@app.post("/payer_transactions")
def add_transaction(transaction: PayerTransaction):
  transactions.append(transaction)
  transactions.sort(key=lambda date: date.timestamp, reverse=True)

  if transaction.payer not in payer_points:
    payer_points[transaction.payer] = 0
  payer_points[transaction.payer] += transaction.points
  user.total_points += transaction.points

  return [payer_points, user.total_points]


# check if spend is greater than amount of total points for User, return error if >
# iterate backward over transactions, subtract points from payer in payerpoints
  # add payer and negative points taken to payer list
  # if total amount is greater than amount in transaction, then delete that transaction
  #
# return list of dicts with payer and points subtracted from payer
@app.post("/spend")
def spend_payer_points(spend: SpendPoints):
  validate_spend(spend.points, user.total_points)

  user.total_points -= spend.points

  subtracted_points = {}
  transaction_remove_counter = 0
  for i in reversed(range(len(transactions))):

    transaction = transactions[i]
    if spend.points == 0:
      break
    if spend.points > transaction.points:
      spend.points -= transaction.points
      payer_points[transaction.payer] -= transaction.points
      if transaction.payer not in subtracted_points:
        subtracted_points[transaction.payer] = 0
      subtracted_points[transaction.payer] -= transaction.points
      transaction_remove_counter += 1

    elif spend.points < transaction.points:
      transaction.points -= spend.points
      payer_points[transaction.payer] -= spend.points
      if transaction.payer not in subtracted_points:
        subtracted_points[transaction.payer] = 0
      subtracted_points[transaction.payer] -= spend.points
      spend.points = 0

    else:
      payer_points[transaction.payer] -= spend.points
      if transaction.payer not in subtracted_points:
        subtracted_points[transaction.payer] = 0
      subtracted_points[transaction.payer] -= spend.points
      transaction_remove_counter += 1
      spend.points = 0

  while transaction_remove_counter > 0:
    transactions.pop()
    transaction_remove_counter -= 1

  return subtracted_points
def validate_spend(spend, user_points):
  if spend > user_points:
    raise HTTPException(status_code=422,
    detail=f'ERROR: Only {user_points} points available to spend')
  if spend <= 0:
    raise HTTPException(status_code=422,
    detail=f'ERROR: Points spend must be greater than 0.')
  pass



  return {"points": user.total_points}
