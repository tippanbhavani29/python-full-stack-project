# 🚀 Crypto Portfolio Tracker

**Crypto Portfolio Tracker** is a beginner-friendly application to help you **manage and monitor your cryptocurrency investments** in real time. Track your holdings, calculate gains/losses, visualize historical trends, and get alerts—**all in one secure dashboard**. Perfect for crypto enthusiasts who want a smart and interactive portfolio tool.  

---

## Key Features

- **📊 Live Portfolio & Gain/Loss Calculation** – Track your holdings and see profits or losses in real time.  
- **➕➖ Add/Remove Coins** – Easily manage your crypto assets.  
- **📈 Historical Price Charts** – Visualize market trends and coin performance over time.  
- **🔔 Email/SMS Alerts** – Get notified when your coins hit target prices.  
- **🔒 User Authentication & Secure Storage** – Keep your portfolio and personal data safe.  

------

## Project Structure
Crypto-tracker/
|
|---src/         #core application logic
|   |---logic.py #Business logic and task
operations
|   |---db.py    #database operations
|
|---API/         #backend api
|   |---main.py  #FastAPI endpoints 
|
|---frontend/    #Frontend application
|   |---api.py   #Streamlit web interface
|
|---requirements.txt #python Dependeencie
|
|---README.md #project documentation
|
|---.env #Python Variables


## Quick Start
### Prerequiestes
- Python 3.8 or higher
- A supabase account
- Git(Push,cloning)


### 1.Clone or Download the project
# option 1: Clone with Gir 
git clone <repository-url>
# oprion 2: Download and extract the ZIP file

### 2.Install Dependencies
# Install all required python packages
ppip install -r requirements.txt
### 3. Set up Supabase Database

1.Create a Supabase Project:

2.Create the Tasks Table:

-   Go to SQL Editor in your Supabase dashboard
-   Run this sql command:

``` sql
create table users (
    id uuid primary key default gen_random_uuid(),
    email text unique not null,
    password_hash text not null,
    created_at timestamp default now()
);
create table portfolio (
    id uuid primary key default gen_random_uuid(),
    user_id uuid references users(id),
    coin_id text not null,        
    coin_name text,
    amount numeric not null,
    buy_price numeric,
    created_at timestamp default now()
);
create table alerts (
    id uuid primary key default gen_random_uuid(),
    user_id uuid references users(id),
    coin_id text not null,
    target_price numeric not null,
    alert_type text check (alert_type in ('above','below')),
    created_at timestamp default now()
);
 
```
3. ** Get Your Credentials:

### 4 .Configure Environment Variables


1. Create a `.env` file in the project root
2. ADD Your Supabase crediential to `.env`:
SUPABASE_URL=your_project_url_here
SUPABASE_KEY=your_anon_key_here

**Example:**
SUPABASE_URL=https://anandsdnwklen/supabase.co
SUPABASE_KEY=ey.jaskhdwebbabdhsadbajbajaksjio...


### 5. Run the Application
## Stramlit Frontend
Streamlit run frontend/app.py

The app will open in your browser at `http://localhost:8501`

## FastAPI Backend
cd api
python main.py
The API will be availabale at `http://localhost:8000`

### How to Use the Crypto Portfolio Tracker
## Sign Up / Log In

User opens the app (Streamlit frontend).
They either:
Sign Up with email & password (stored in Supabase Auth 🔒), or
Log In if they already have an account.
Once authenticated, the app knows their user_id.

## Add Coins to Portfolio
On the dashboard, there’s an “Add Coin” form.
User selects a coin (e.g., Bitcoin), enters:
Amount (e.g., 0.5 BTC)
Buy Price (e.g., $25,000)
This info is saved in the Portfolio table in Supabase, linked to their user_id.
## View Portfolio Dashboard
The dashboard displays:
Total Portfolio Value 💰 → based on live prices from CoinGecko API.
Gains/Losses 📊 → compares current price vs buy price.
Holdings Table → list of all coins user owns.
Historical Price Charts 📈 → line charts or candlestick charts per coin.

## Manage Portfolio

User can:
Remove a coin ➖ → Deletes entry from Supabase.
Update holdings ✏️ → e.g., if they bought more of a coin.

## Set Price Alerts
User sets a rule like:
“Notify me if Bitcoin drops below $20,000”
Stored in Alerts table in Supabase.
Background task (Python + scheduler or serverless function) checks prices.
If triggered → Email (SMTP) or SMS (Twilio API) 🔔 sent.

## Log Out
When done, user logs out.
Session ends securely → no one else can see their portfolio.

### Technologies Used
 - **Frontend**: Streamlit(python web framework)
 - **Backend**: FastAPI (Python REST API framework)
 - **Database**:Supabase(PostgreSQL-based backend-as-a-service)
 - **Language**:Python 3.8+

### Key components
1. **`src/db.py`** : Database operations 
    - Handles all CRUD  operations with supabase
2. **`src/logic.py`**:Business logic 
    - Tasks validation and processing
### ToubleShooting
## Common  Issues
1. **"Module not found " errors**
    - Make sure you've installed all dependeencies:`pip installl -r requirements.txt`
    - Check that you're running commands from correct directory
## Future Enhancements
Ideas for extending this project:


1. Advanced Authentication & Security
2. Smarter Portfolio Analytics
3. Multi-Asset Support
4. Automated Trading (Optional, Advanced)
5. Social Features
6. Visualization & Insights
7. Mobile App Integration
## Support
 
If you encounter any issues or have questions:
- email:`tippanbhavani@gmail.com`
- mobile no: `9347151681`