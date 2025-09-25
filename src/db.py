from supabase import Client, create_client
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
import os
from urllib.parse import urlencode

# ---------------- Load environment variables ---------------- #
load_dotenv()
SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL or KEY is missing in .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- Users ---------------- #
def create_user(email: str, password_hash: Optional[str] = None) -> Dict[str, Any]:
    """Register a new user (email/password or OAuth)."""
    response = supabase.table("users").insert({
        "email": email,
        "password_hash": password_hash
    }).execute()
    return response.data[0] if response.data else None


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Fetch a user by email."""
    response = supabase.table("users").select("*").eq("email", email).execute()
    return response.data[0] if response.data else None


def create_oauth_user(user_id: str, email: str) -> Dict[str, Any]:
    """Create an OAuth user record if it doesn't exist."""
    existing = supabase.table("users").select("*").eq("id", user_id).execute()
    if existing.data:
        return existing.data[0]
    response = supabase.table("users").insert({
        "id": user_id,
        "email": email,
        "password_hash": None  # OAuth users have no password
    }).execute()
    return response.data[0] if response.data else None


def get_google_login_url(redirect_to: str) -> str:
    """Generate Google login URL via Supabase."""
    params = {
        "provider": "google",
        "redirect_to": redirect_to
    }
    return f"{SUPABASE_URL}/auth/v1/authorize?{urlencode(params)}"

# ---------------- Portfolio ---------------- #
def add_asset(user_id: str, coin_id: str, coin_name: str, amount: float, buy_price: float) -> Dict[str, Any]:
    response = supabase.table("portfolio").insert({
        "user_id": user_id,
        "coin_id": coin_id,
        "coin_name": coin_name,
        "amount": amount,
        "buy_price": buy_price
    }).execute()
    return response.data[0] if response.data else None


def get_portfolio(user_id: str) -> List[Dict[str, Any]]:
    response = supabase.table("portfolio").select("*").eq("user_id", user_id).execute()
    return response.data


def update_asset(user_id: str, coin_id: str, amount: float, buy_price: float) -> Dict[str, Any]:
    response = supabase.table("portfolio").update({
        "amount": amount,
        "buy_price": buy_price
    }).eq("user_id", user_id).eq("coin_id", coin_id).execute()
    return response.data[0] if response.data else None


def delete_asset(user_id: str, coin_id: str) -> Dict[str, Any]:
    response = supabase.table("portfolio").delete().eq("user_id", user_id).eq("coin_id", coin_id).execute()
    return response.data[0] if response.data else None

# ---------------- Alerts ---------------- #
def add_alert(user_id: str, coin_id: str, target_price: float, alert_type: str) -> Dict[str, Any]:
    response = supabase.table("alerts").insert({
        "user_id": user_id,
        "coin_id": coin_id,
        "target_price": target_price,
        "alert_type": alert_type
    }).execute()
    return response.data[0] if response.data else None


def get_alerts(user_id: str) -> List[Dict[str, Any]]:
    response = supabase.table("alerts").select("*").eq("user_id", user_id).execute()
    return response.data


def delete_alert(alert_id: str) -> Dict[str, Any]:
    response = supabase.table("alerts").delete().eq("id", alert_id).execute()
    return response.data[0] if response.data else None


# ---------------- Example Usage ---------------- #
if __name__ == "__main__":
    # Traditional email/password user
    user = get_user_by_email("alice@example.com")
    if not user:
        user = create_user("alice@example.com", "hashed_password_123")
    user_id = user["id"]
    print("User ID:", user_id)

    # Google login URL example
    google_login = get_google_login_url("https://jkgwuubogxmjmsglajrj.supabase.co/auth/v1/callback")
    print("Go to this URL to login with Google:", google_login)
