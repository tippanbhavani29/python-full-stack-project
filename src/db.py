# crypto_tracker.py
from supabase import create_client, Client
from urllib.parse import urlencode, parse_qs, urlparse
from dotenv import load_dotenv
import os
from typing import List, Dict, Optional

# ---------------- Load environment variables ---------------- #
load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL or KEY is missing in .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- Users ---------------- #
def create_user(email: str, password_hash: Optional[str] = None) -> Dict:
    """Create a user (email/password or OAuth)."""
    response = supabase.table("users").insert({
        "email": email,
        "password_hash": password_hash
    }).execute()
    return response.data[0] if response.data else None


def get_user_by_email(email: str) -> Optional[Dict]:
    """Fetch user by email."""
    response = supabase.table("users").select("*").eq("email", email).execute()
    return response.data[0] if response.data else None


def create_oauth_user(user_id: str, email: str) -> Dict:
    """Create OAuth user if not exists."""
    existing = supabase.table("users").select("*").eq("id", user_id).execute()
    if existing.data:
        return existing.data[0]
    response = supabase.table("users").insert({
        "id": user_id,
        "email": email,
        "password_hash": None
    }).execute()
    return response.data[0] if response.data else None


def get_google_login_url() -> str:
    """Generate Google login URL via Supabase."""
    redirect_url = "https://jkgwuubogxmjmsglajrj.supabase.co/auth/v1/callback"
    params = {
        "provider": "google",
        "redirect_to": redirect_url
    }
    return f"{SUPABASE_URL}/auth/v1/authorize?{urlencode(params)}"

# ---------------- Portfolio ---------------- #
def add_asset(user_id: str, coin_id: str, coin_name: str, amount: float, buy_price: float) -> Dict:
    response = supabase.table("portfolio").insert({
        "user_id": user_id,
        "coin_id": coin_id,
        "coin_name": coin_name,
        "amount": amount,
        "buy_price": buy_price
    }).execute()
    return response.data[0] if response.data else None


def get_portfolio(user_id: str) -> List[Dict]:
    response = supabase.table("portfolio").select("*").eq("user_id", user_id).execute()
    return response.data


# ---------------- Alerts ---------------- #
def add_alert(user_id: str, coin_id: str, target_price: float, alert_type: str) -> Dict:
    response = supabase.table("alerts").insert({
        "user_id": user_id,
        "coin_id": coin_id,
        "target_price": target_price,
        "alert_type": alert_type
    }).execute()
    return response.data[0] if response.data else None


def get_alerts(user_id: str) -> List[Dict]:
    response = supabase.table("alerts").select("*").eq("user_id", user_id).execute()
    return response.data

# ---------------- Example flow ---------------- #
if __name__ == "__main__":
    # Step 1: Generate Google login URL
    login_url = get_google_login_url()
    print("Go to this URL to login with Google:")
    print(login_url)

    # Step 2: After Google login, Supabase redirects to your callback URL
    # Copy the full redirected URL from the browser and paste here
    callback_url = input("Paste the full callback URL after login: ")

    # Step 3: Parse the URL query parameters (for demo, we simulate user info)
    # In a real app, use Supabase client or session to get the user info
    oauth_user_id = "simulated_google_user_id_123"  # Replace with actual session user.id
    oauth_email = "alice@gmail.com"                 # Replace with actual session user.email

    # Step 4: Create OAuth user in database
    user = create_oauth_user(oauth_user_id, oauth_email)
    print("OAuth user created/fetched:", user)

    # Step 5: Add a portfolio asset
    asset = add_asset(user["id"], "bitcoin", "Bitcoin", 0.5, 30000)
    print("Added portfolio asset:", asset)

    # Step 6: Add a price alert
    alert = add_alert(user["id"], "bitcoin", 35000, "above")
    print("Added price alert:", alert)

    # Step 7: Display portfolio and alerts
    print("User portfolio:", get_portfolio(user["id"]))
    print("User alerts:", get_alerts(user["id"]))
