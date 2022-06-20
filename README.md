# Fetch Rewards Backend Software Engineering Takehome
A REST API designed to receive HTTP requests and return responses based on a user's transactions, reward points balance, and reward points spend. 

## Overview
* A `user` can have reward points balances in their account from various `payers` (presumably businesses where a user transacts)
  * e.g., `{"Nike": 500, "Cheesecake Factory": 1000}`
 
* `Transactions` are submitted to add or subtract points from a user's reward points balance
  * Payer balances in a user's account cannot go below 0
 
* A user can `spend` points from their account/payer balances
  * User's total points cannot go below 0
  * Points are spent in First-In-First-Out order based on transaction timestamp, irrespective of payer

## Dependencies 
* [Python](https://www.python.org/downloads/) - The latest version of Python to run the program, or at least version 3.7+
* [FastAPI](https://fastapi.tiangolo.com/) - A modern, fast, web framework for building APIs with Python 3.6+ based on standard Python type hints
* [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation and settings management using python type annotations
* [Pytest](https://docs.pytest.org/en/7.1.x/index.html) - Python testing framework

## Installation

1) Clone git repo to your local machine 
   ```
    git clone https://github.com/alexsmaldone/fetchrewards-takehome.git
   ```
2) Cd into the project's root directory 
   ```
    cd fetchrewards-takehome/
   ```
3) Install dependencies
   ```
    pip install -r requirements.txt
   ```
