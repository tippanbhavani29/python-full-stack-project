# src/logic.py

import requests
from typing import List, Dict, Optional
from src.db import (
    create_user,
    get_user_by_email,
    create_oauth_user,
    add_asset,
    get_portfolio,
    update_asset,
    delete_asset,
    add_alert,
    get_alerts,
    delete_alert
)
# from supabase import DatabaseManager

# ---------------- Users Manager ---------------- #
class UsersManager:
    def __init__(self):
        pass

    def register_user(self, email: str, password_hash: str) -> Dict:
        user = get_user_by_email(email)
        if user:
            return {"error": "User already exists", "user": user}
        return create_user(email, password_hash)

    def login_user(self, email: str) -> Optional[Dict]:
        return get_user_by_email(email)

    def login_oauth_user(self, user_id: str, email: str) -> Dict:
        return create_oauth_user(user_id, email)

# ---------------- Portfolio Manager ---------------- #
class PortfolioManager:
    def __init__(self):
         
        self.cg_base_url = "https://api.coingecko.com/api/v3"

    def add_asset(self, user_id: str, coin_id: str, coin_name: str, amount: float, buy_price: float) -> Dict:
        return add_asset(user_id, coin_id, coin_name, amount, buy_price)

    def update_asset(self, user_id: str, coin_id: str, amount: float, buy_price: float) -> Dict:
        return update_asset(user_id, coin_id, amount, buy_price)

    def delete_asset(self, user_id: str, coin_id: str) -> Dict:
        return delete_asset(user_id, coin_id)

    def get_portfolio(self, user_id: str) -> List[Dict]:
        return get_portfolio(user_id)

    def get_current_price(self, coin_id: str, vs_currency: str = "usd") -> Optional[float]:
        url = f"{self.cg_base_url}/simple/price"
        params = {"ids": coin_id, "vs_currencies": vs_currency}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get(coin_id, {}).get(vs_currency)
        except Exception as e:
            print(f"Error fetching price for {coin_id}: {e}")
            return None

    def portfolio_summary(self, user_id: str) -> Dict:
        portfolio = self.get_portfolio(user_id)
        total_investment = 0.0
        total_current_value = 0.0
        portfolio_details = []

        for item in portfolio:
            coin_id = item["coin_id"]
            amount = item["amount"]
            buy_price = item["buy_price"]
            current_price = self.get_current_price(coin_id) or buy_price

            investment = amount * buy_price
            current_value = amount * current_price
            gain_loss = current_value - investment
            gain_loss_pct = (gain_loss / investment * 100) if investment > 0 else 0

            total_investment += investment
            total_current_value += current_value

            portfolio_details.append({
                "coin_id": coin_id,
                "coin_name": item["coin_name"],
                "amount": amount,
                "buy_price": buy_price,
                "current_price": current_price,
                "investment": investment,
                "current_value": current_value,
                "gain_loss": gain_loss,
                "gain_loss_pct": round(gain_loss_pct, 2)
            })

        total_gain_loss = total_current_value - total_investment
        total_gain_loss_pct = (total_gain_loss / total_investment * 100) if total_investment > 0 else 0

        return {
            "total_assets": len(portfolio),
            "total_investment": total_investment,
            "total_current_value": total_current_value,
            "total_gain_loss": total_gain_loss,
            "total_gain_loss_pct": round(total_gain_loss_pct, 2),
            "portfolio": portfolio_details
        }

# ---------------- Alerts Manager ---------------- #
class AlertsManager:
    def __init__(self):
         pass

    def add_alert(self, user_id: str, coin_id: str, target_price: float, alert_type: str) -> Dict:
        if alert_type not in ("above", "below"):
            return {"error": "Invalid alert type"}
        return add_alert(user_id, coin_id, target_price, alert_type)

    def delete_alert(self, alert_id: str) -> Dict:
        return delete_alert(alert_id)

    def get_alerts(self, user_id: str) -> List[Dict]:
        return get_alerts(user_id)

    def alert_summary(self, user_id: str) -> Dict:
        alerts = self.get_alerts(user_id)
        above_alerts = [a for a in alerts if a["alert_type"] == "above"]
        below_alerts = [a for a in alerts if a["alert_type"] == "below"]
        return {
            "total_alerts": len(alerts),
            "above_alerts": len(above_alerts),
            "below_alerts": len(below_alerts),
            "alerts": alerts
        }
