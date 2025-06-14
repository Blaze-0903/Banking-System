import streamlit as st
import time
from backend import BankSystem

# Page settings
st.set_page_config(page_title="Blaze Bank", layout="centered")

# Initialize session state
if "bank" not in st.session_state:
    st.session_state.bank = BankSystem()
if "page" not in st.session_state:
    st.session_state.page = "Home"

bank = st.session_state.bank

# Navigation logic
def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# ---------------------- HOME ----------------------
if st.session_state.page == "Home":
    # Page Header
    st.markdown("""
        <div style='text-align:center; padding: 2rem 0;'>
            <h1 style='font-size:3rem; color:#6C63FF;'>🏦 Blaze Bank</h1>
            <p style='font-size:1.2rem; color:#555;'>Modern • Secure • Personalized Digital Banking</p>
        </div>
    """, unsafe_allow_html=True)

    # Feature Highlights
    st.markdown("""
    <style>
        .feature-card {
            background-color: #ffffff;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            padding: 2rem 1rem;
            text-align: center;
            height: 250px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 0.8rem;
        }

        .feature-title {
            font-size: 1.3rem;
            font-weight: bold;
            color: #222;
            margin-bottom: 0.3rem;
        }

        .feature-text {
            font-size: 0.95rem;
            color: #555;
        }
    </style>
""", unsafe_allow_html=True)

    # Section heading
    st.markdown("<h2 style='text-align: center;'>Why Choose Blaze Bank?</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #555;'>Smart. Secure. Swift.</p>", unsafe_allow_html=True)

    # Cards in columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Secure</div>
            <div class="feature-text">Your data is protected end-to-end.</div>
        </div>
    """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Fast</div>
            <div class="feature-text">Instant transactions and updates.</div>
        </div>
    """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤝</div>
            <div class="feature-title">Personalized</div>
            <div class="feature-text">Tailored to your needs.</div>
        </div>
    """, unsafe_allow_html=True)

    # Call to Action
    st.markdown("---")
    st.markdown("<div style='text-align:center; font-size:18px; padding-bottom:1rem;'>Get Started Today</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔑 Login", use_container_width=True):
            go_to("Login")
    with col2:
        if st.button("📝 Register", use_container_width=True):
            go_to("Register")

    # Footer
    st.markdown("""
        <hr style="margin-top: 3rem; border: none; border-top: 1px solid #ddd;">
        <div style="text-align: center; padding: 1rem 0 2rem 0; font-size: 0.9rem; color: #666;">
            © 2025 Blaze Bank. All rights reserved.
        </div>
    """, unsafe_allow_html=True)

# ---------------------- LOGIN ----------------------
elif st.session_state.page == "Login":
    st.markdown("<h2 style='color:#2196F3'>🔑 Login to Your Account</h2>", unsafe_allow_html=True)
    with st.form("login_form"):
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")
        submitted = st.form_submit_button("➡️ Login")

        if submitted:
            result = bank.login_user(username, password)
            if "Welcome" in result:
                st.success(result)
                st.toast(result)
                time.sleep(1.5)
                go_to("Dashboard")
            else:
                st.error(result)

    if st.button("🆕 Not registered yet? Create an account"):
        go_to("Register")

# ---------------------- REGISTER ----------------------
elif st.session_state.page == "Register":
    st.markdown("<h2 style='color:#4CAF50'>🔐 Create a New Account</h2>", unsafe_allow_html=True)
    with st.form("register_form"):
        username = st.text_input("👤 Username")
        name = st.text_input("📛 Full Name")
        age = st.number_input("🎂 Age", min_value=10, max_value=100)
        contact = st.text_input("📱 Contact Number")
        password = st.text_input("🔑 Password", type="password")
        confirm_password = st.text_input("🔑 Confirm Password", type="password")
        submitted = st.form_submit_button("✅ Register")

        if submitted:
            if password != confirm_password:
                st.error("❌ Passwords do not match.")
            elif not all([username, name, contact, password]):
                st.warning("⚠️ Please fill all fields.")
            else:
                result = bank.register_user(username, name, age, contact, password)
                if "successfully" in result:
                    st.success(result)
                    st.balloons()
                    time.sleep(1.5)
                    go_to("Login")
                else:
                    st.error(result)

    if st.button("🔁 Already registered? Go to Login"):
        go_to("Login")

# ---------------------- DASHBOARD ----------------------
elif st.session_state.page == "Dashboard":
    user = bank.get_current_user()
    if not user:
        st.warning("Please login first.")
        go_to("Login")

    st.markdown(f"<h2 style='color:#9C27B0'>📊 Welcome, {user.name}</h2>", unsafe_allow_html=True)
    st.metric(label="💰 Account Balance", value=f"₹ {user.balance:.2f}")

    # Transaction history
    st.subheader("📜 Transaction History")
    if user.transactions:
        for txn in reversed(user.transactions[-5:]):
            st.info(txn)
    else:
        st.markdown("_No transactions yet._")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("➕ Deposit")
        with st.form("deposit_form"):
            amount = st.number_input("Enter amount to deposit", min_value=0.01, step=0.01, key="dep")
            submit_deposit = st.form_submit_button("Deposit")
            if submit_deposit:
                result = bank.deposit(amount)
                st.success(result)
                st.toast(result)
                time.sleep(1.5)
                st.rerun()

    with col2:
        st.subheader("➖ Withdraw")
        with st.form("withdraw_form"):
            amount = st.number_input("Enter amount to withdraw", min_value=0.01, step=0.01, key="wit")
            submit_withdraw = st.form_submit_button("Withdraw")
            if submit_withdraw:
                result = bank.withdraw(amount)
                if "Insufficient" in result:
                    st.error(result)
                    st.toast(result, icon="⚠️")
                else:
                    st.success(result)
                    st.toast(result)
                    time.sleep(1.5)
                    st.rerun()

    if st.button("🚪 Logout"):
        bank.logout_user()
        go_to("Home")
