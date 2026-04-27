import streamlit as st
import pickle
import numpy as np

# ------------------ LOAD MODEL ------------------
model = pickle.load(open("model.pkl", "rb"))

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Stock AI", page_icon="📈", layout="wide")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
body {
    background-color: #0E1117;
}
.main {
    background-color: #0E1117;
}

/* Cards */
.card {
    background-color: #1E1E2E;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #00C9FF, #92FE9D);
    color: black;
    font-weight: bold;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}

/* Inputs */
.stNumberInput input, .stTextInput input {
    background-color: #262730;
    color: white;
    border-radius: 8px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}
</style>
""", unsafe_allow_html=True)

# ------------------ SESSION ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ------------------ LOGIN ------------------
def login():
    st.markdown("<h1 style='text-align:center;'>🔐 Login</h1>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login Successful 🚀")
            st.rerun()
        else:
            st.error("Invalid Credentials ❌")

# ------------------ DASHBOARD ------------------
def dashboard():
    st.markdown("<h1>📊 Dashboard</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    col1.markdown('<div class="card"><h3>Accuracy</h3><h2>77%</h2></div>', unsafe_allow_html=True)
    col2.markdown('<div class="card"><h3>Model</h3><h2>XGBoost</h2></div>', unsafe_allow_html=True)
    col3.markdown('<div class="card"><h3>Status</h3><h2 style="color:lightgreen;">Active</h2></div>', unsafe_allow_html=True)

    st.divider()

    st.subheader("📈 About System")
    st.info("AI model predicts stock closing price using Open, High, Low & Volume data.")

# ------------------ PREDICT ------------------
def prediction_page():
    st.markdown("<h1>📈 Predict Stock</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        open_price = st.number_input("Open Price", min_value=0.0)
        low_price = st.number_input("Low Price", min_value=0.0)

    with col2:
        high_price = st.number_input("High Price", min_value=0.0)
        volume = st.number_input("Volume Traded", min_value=0.0)

    if st.button("🚀 Predict"):
        input_data = np.array([[open_price, high_price, low_price, volume]])
        prediction = model.predict(input_data)

        st.markdown(f"""
        <div class="card">
            <h2>💰 Predicted Price: {prediction[0]:.2f}</h2>
        </div>
        """, unsafe_allow_html=True)

        if prediction[0] > open_price:
            st.success("📈 Market Trend: UP")
        else:
            st.error("📉 Market Trend: DOWN")

# ------------------ ACCOUNT ------------------
def account():
    st.markdown("<h1>👤 Account</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>Username: admin</h3>
        <h3>Role: User</h3>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ------------------ MAIN ------------------
if not st.session_state.logged_in:
    login()
else:
    st.sidebar.title("🚀 Smart Navigation")

    page = st.sidebar.radio("Go to", ["Dashboard", "Predict", "Account"])

    if page == "Dashboard":
        dashboard()
    elif page == "Predict":
        prediction_page()
    elif page == "Account":
        account()
