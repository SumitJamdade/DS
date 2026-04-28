import streamlit as st
import pickle
import numpy as np
import pandas as pd

# ------------------ LOAD MODEL ------------------
model = pickle.load(open("model.pkl", "rb"))

# ------------------ LOAD DATA ------------------
df = pd.read_csv("processed_data.csv")
df.columns = df.columns.str.lower()

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Smart Trade", page_icon="📈", layout="wide")

# ------------------ CSS ------------------
st.markdown("""
<style>
.card {
    background-color: #1E1E2E;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

# ------------------ SESSION ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ------------------ LOGIN ------------------
def login():
    st.title("💼 Smart Trade Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")

# ------------------ DASHBOARD ------------------
def dashboard():

    st.title("📊 Smart Trade Dashboard")

    st.info("Welcome to Smart Trade — AI based stock prediction platform.")

    # -------- Portfolio --------
    st.subheader("💼 My Portfolio")

    portfolio = {
        "TCS": 10,
        "INFOSYS": 5,
        "RELIANCE": 3
    }

    total_value = 0

    for stock, qty in portfolio.items():
        stock_data = df[df['ticker'] == stock]

        if not stock_data.empty:
            price = stock_data.iloc[-1]['close_price']
            value = price * qty
            total_value += value

            st.write(f"{stock} → {qty} shares | ₹{price:.2f} | Value: ₹{value:.2f}")

    st.success(f"💰 Total Portfolio Value: ₹{total_value:.2f}")

    st.divider()

    # -------- Search --------
    st.subheader("🔍 Search Company")

    search = st.text_input("Enter company name")

    if search:
        result = df[df['ticker'].str.contains(search.upper())]
        st.dataframe(result[['ticker', 'open_price', 'close_price']].tail(10))

    st.divider()

    # -------- News --------
    st.subheader("📰 Market News")

    st.write("• IT stocks are showing steady growth 📈")
    st.write("• Banking sector is stable 🏦")
    st.write("• Global market trends affecting volatility 🌍")

# ------------------ PREDICTION ------------------
def prediction_page():

    st.title("📈 Predict Stock Closing Price")

    # Company dropdown
    company = st.selectbox("Select Company", df['ticker'].unique())

    data = df[df['ticker'] == company].iloc[-1]

    st.subheader("📊 Latest Data Used")
    st.write(data[['open_price', 'high_price', 'low_price', 'volume_traded']])

    if st.button("🚀 Predict"):

        input_data = np.array([[ 
            data['open_price'],
            data['high_price'],
            data['low_price'],
            data['volume_traded']
        ]])

        prediction = model.predict(input_data)

        st.success(f"💰 Predicted Closing Price: ₹{prediction[0]:.2f}")

        # Trend
        if prediction[0] > data['open_price']:
            st.success("📈 Market Trend: UP")
        else:
            st.error("📉 Market Trend: DOWN")

        # Explanation
        st.subheader("🧠 Why this prediction?")

        st.info("""
The model analyzes relationship between:

• Open Price  
• High Price  
• Low Price  
• Volume  

Higher demand & volume → price increases  
Lower demand → price drops  

Prediction is based on patterns learned from historical stock data.
""")

# ------------------ ACCOUNT ------------------
def account():

    st.title("👤 My Account")

    st.write("Username: admin")
    st.write("Plan: Basic Trader")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ------------------ MAIN ------------------
if not st.session_state.logged_in:
    login()
else:
    st.sidebar.title("🚀 Smart Trade")

    page = st.sidebar.radio("Navigation", ["Dashboard", "Predict", "Account"])

    if page == "Dashboard":
        dashboard()
    elif page == "Predict":
        prediction_page()
    elif page == "Account":
        account()
