# api/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Ensure src folder is in Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.logic import UsersManager, PortfolioManager, AlertsManager

# ---------------- App Setup ---------------- #
app = FastAPI(title="Crypto Tracker API", version="1.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ---------------- Managers ---------------- #
user_manager = UsersManager()
portfolio_manager = PortfolioManager()
alerts_manager = AlertsManager()

# ---------------- Schemas ---------------- #
class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str

class AssetCreate(BaseModel):
    user_id: str
    coin_id: str
    coin_name: str
    amount: float
    buy_price: float

class AssetUpdate(BaseModel):
    user_id: str
    coin_id: str
    amount: float
    buy_price: float

class AlertCreate(BaseModel):
    user_id: str
    coin_id: str
    target_price: float
    alert_type: str

# ---------------- User Endpoints ---------------- #
@app.post("/users/register")
def register_user(user: UserCreate):
    result = user_manager.register_user(user.email, user.password)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"status": "success", "user": result}

@app.post("/users/login")
def login_user(user: UserLogin):
    result = user_manager.login_user(user.email)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "user": result}

# ---------------- Portfolio Endpoints ---------------- #
@app.post("/portfolio/add")
def add_asset_endpoint(asset: AssetCreate):
    result = portfolio_manager.add_asset(
        asset.user_id, asset.coin_id, asset.coin_name, asset.amount, asset.buy_price
    )
    return {"status": "success", "asset": result}

@app.put("/portfolio/update")
def update_asset_endpoint(asset: AssetUpdate):
    result = portfolio_manager.update_asset(
        asset.user_id, asset.coin_id, asset.amount, asset.buy_price
    )
    return {"status": "success", "asset": result}

@app.delete("/portfolio/delete/{user_id}/{coin_id}")
def delete_asset_endpoint(user_id: str, coin_id: str):
    result = portfolio_manager.delete_asset(user_id, coin_id)
    return {"status": "success", "result": result}

@app.get("/portfolio/{user_id}/summary")
def portfolio_summary_endpoint(user_id: str):
    result = portfolio_manager.portfolio_summary(user_id)
    return {"status": "success", "summary": result}

# ---------------- Alerts Endpoints ---------------- #
@app.post("/alerts/add")
def add_alert_endpoint(alert: AlertCreate):
    result = alerts_manager.add_alert(alert.user_id, alert.coin_id, alert.target_price, alert.alert_type)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {"status": "success", "alert": result}

@app.delete("/alerts/delete/{alert_id}")
def delete_alert_endpoint(alert_id: str):
    result = alerts_manager.delete_alert(alert_id)
    return {"status": "success", "result": result}

@app.get("/alerts/{user_id}/summary")
def alert_summary_endpoint(user_id: str):
    result = alerts_manager.alert_summary(user_id)
    return {"status": "success", "summary": result}

# ---------------- Run ---------------- #
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
