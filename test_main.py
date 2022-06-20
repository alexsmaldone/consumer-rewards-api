import json
from route_functions import validate_transaction, process_transaction, validate_spend, process_spend
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


#  {"payer": "C", "points": 50, "timestamp": "2022-06-20T11:07:05.017197"}

# =============================================================================================
# GET /POINTS
# =============================================================================================
def test_get_payer_points():
  response = client.get("/points")
  assert response.status_code == 200
  assert response.json() == {}

# =============================================================================================
# POST /POINTS
# =============================================================================================
def test_nagative_balance_transaction():
  response = client.post("/points",
  json={"payer": "A", "points": -50, "timestamp": "2022-06-20T11:07:05.017197"},
  )
  assert response.status_code == 422
  assert response.json() == {"detail": 'ERROR: Unable to add transaction; payer balance cannnot go negative. A has 0 points in account.'}

def test_zero_balance_transaction():
  response = client.post("/points",
  json={"payer": "A", "points": 0, "timestamp": "2022-06-20T11:07:05.017197"},
  )
  assert response.status_code == 422
  assert response.json() == {"detail": 'ERROR: Unable to add transaction; Points must be positive or negative integer.'}

def test_valid_transaction_sequence():
  client.post("/points",
  json={"payer": "A", "points": 100, "timestamp": "2022-06-20T11:07:05.017197"},
  )
  client.post("/points",
  json={"payer": "B", "points": 100, "timestamp": "2022-06-20T11:07:05.017197"},
  )
  client.post("/points",
  json={"payer": "A", "points": -50, "timestamp": "2022-06-20T11:07:05.017197"},
  )
  response = client.post("/points",
  json={"payer": "B", "points": -50, "timestamp": "2022-06-20T11:07:05.017197"},
  )
  assert response.status_code == 200
  assert response.json() == {"Message": "Transaction Successful", "Current Balance": {"A": 50, "B": 50}}

# =============================================================================================
# POST /SPEND
# =============================================================================================
def test_invalid_negative_spend():
  response = client.post("/spend",
  json={"points": -50},
  )
  assert response.status_code == 200
  assert response.json() == {"Message": "Transaction Successful", "Current Balance": {"A": 50, "B": 50}}