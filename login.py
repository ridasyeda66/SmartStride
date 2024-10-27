# login.py
import streamlit as st
import hashlib
from google.cloud import firestore
from config import setup_gcp
import datetime

# Configure the path to the service account key
setup_gcp()

# Firestore client initialization
db = firestore.Client()


def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def user_exists(email):
    """Check if a user with the given email already exists in Firestore."""
    users_ref = db.collection("users")
    query = users_ref.where("email", "==", email).get()
    return len(query) > 0

def create_user(email, password):
    """Create a new user in Firestore with hashed password."""
    hashed_password = hash_password(password)
    user_data = {
        "email": email,
        "password": hashed_password
    }
    db.collection("users").add(user_data)

def verify_user(email, password):
    """Verify if the user's email and password match with Firestore records."""
    users_ref = db.collection("users")
    query = users_ref.where("email", "==", email).get()
    
    if query:
        user = query[0]
        stored_password = user.to_dict()["password"]
        return stored_password == hash_password(password), user.id
    return False, None

def session_reset():
    if "chat_history" in st.session_state:
        st.session_state["chat_history"] = []
    if "session_id" in st.session_state:
        del st.session_state["session_id"]

def login():
    st.title("Login / Signup")

    # Choose between login and signup
    choice = st.radio("Choose an option", ["Login", "Signup"])

    # Form for email and password
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        if st.button("Create Account"):
            if user_exists(email):
                st.error("User already exists. Please log in.")
            else:
                create_user(email, password)
                st.success("Account created successfully! Please log in.")

    elif choice == "Login":
        if st.button("Login"):
            authenticated, user_id = verify_user(email, password)
            if authenticated:
                session_reset()
                st.session_state["authenticated"] = True
                st.session_state["user_id"] = user_id
                st.success("Logged in successfully!")
                st.session_state["session_id"] = "session_" + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                st.rerun()  # Refresh the app to update the navigation
            else:
                st.error("Invalid email or password.")

    # Logout option if authenticated
    if st.session_state.get("authenticated"):
        if st.button("Logout"):
            st.session_state["authenticated"] = False
            st.session_state["user_id"] = None
            st.success("Logged out successfully.")
            session_reset()
            st.rerun()