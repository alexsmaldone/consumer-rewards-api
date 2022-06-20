from route_functions import validate_transaction, process_transaction, validate_spend, process_spend
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
