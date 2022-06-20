import json
from route_functions import validate_transaction, process_transaction, validate_spend, process_spend
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


#  {"payer": "C", "points": 50, "timestamp": "2022-06-20T11:07:05.017197"}

def test_get_payer_points():
  response = client.get("/points")
  assert response.status_code == 200
  assert response.json() == {}

def test_nagative_balance_transaction():
  response = client.post("/points",
  json={"payer": "A", "points": -50, "timestamp": "2022-06-20T11:07:05.017197"},
  )
  assert response.status_code == 422
  assert response.json() == {"detail": 'ERROR: Unable to add transaction; payer balance cannnot go negative. A has 0 points in account.'}
