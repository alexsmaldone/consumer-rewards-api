from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

user_points = 0
payer_points = {}
transactions = []


@app.get("/")
def get_payer_points():
    return payer_points

@app.post("/")
def add_transaction():
  pass

@app.post("/spend")
def spend_payer_points():
  pass
