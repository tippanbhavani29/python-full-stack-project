# frontend/app.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"  # Backend FastAPI URL

st.set_page_config(page_title="Crypto Portfolio Tracker", layout="wide")

st.title("💰 Crypto Portfolio Tracker")

# ---------------- Session State ---------------- #
if "user" not in st.session_state:
    st.session_state["user"] = None

# ---------------- User Registration/Login ---------------- #
st.sidebar.header("👤 User Authentication")

if st.session_state["user"] is None:
    auth_choice = st.sidebar.radio("Choose Action", ["Register", "Login"])

    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if auth_choice == "Register":
        if st.sidebar.button("Register"):
            response = requests.post(f"{API_URL}/users/register", json={"email": email, "password": password})
            if response.status_code == 200:
                st.success("✅ Registered successfully! Please login.")
            else:
                st.error(response.json().get("detail", "Registration failed"))

    elif auth_choice == "Login":
        if st.sidebar.button("Login"):
            response = requests.post(f"{API_URL}/users/login", json={"email": email})
            if response.status_code == 200:
                st.session_state["user"] = response.json()["user"]
                st.sidebar.success(f"Logged in as {email}")
            else:
                st.sidebar.error("❌ Invalid login")
else:
    st.sidebar.success(f"Logged in as {st.session_state['user']['email']}")
    if st.sidebar.button("Logout"):
        st.session_state["user"] = None
        st.rerun()

# ---------------- Portfolio Section ---------------- #
if st.session_state["user"]:
    st.subheader("📊 Your Portfolio")
    user_id = st.session_state["user"]["id"]

    # Add Asset
    with st.expander("➕ Add Asset"):
        coin_id = st.text_input("Coin ID (e.g., bitcoin, ethereum)")
        coin_name = st.text_input("Coin Name")
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        buy_price = st.number_input("Buy Price (USD)", min_value=0.0, step=0.01)
        if st.button("Add Asset"):
            response = requests.post(f"{API_URL}/portfolio/add", json={
                "user_id": user_id,
                "coin_id": coin_id,
                "coin_name": coin_name,
                "amount": amount,
                "buy_price": buy_price
            })
            if response.status_code == 200:
                st.success("✅ Asset added successfully")
            else:
                st.error("❌ Failed to add asset")

    # Portfolio Summary
    response = requests.get(f"{API_URL}/portfolio/{user_id}/summary")
    if response.status_code == 200:
        summary = response.json()["summary"]
        st.metric("💵 Total Investment", f"${summary['total_investment']:.2f}")
        st.metric("📈 Current Value", f"${summary['total_current_value']:.2f}")
        st.metric("📊 Gain/Loss", f"${summary['total_gain_loss']:.2f} ({summary['total_gain_loss_pct']}%)")

        df = pd.DataFrame(summary["portfolio"])

        if not df.empty:
            st.dataframe(df[["coin_name", "amount", "buy_price", "current_price", "investment", "current_value", "gain_loss", "gain_loss_pct"]])

            # Pie chart - distribution
            fig1 = px.pie(df, values="current_value", names="coin_name", title="Portfolio Distribution")
            st.plotly_chart(fig1, use_container_width=True)

            # Bar chart - gain/loss
            fig2 = px.bar(df, x="coin_name", y="gain_loss", color="gain_loss", title="Gain/Loss per Coin")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No assets found in your portfolio.")
    else:
        st.error("⚠️ Could not fetch portfolio summary.")
