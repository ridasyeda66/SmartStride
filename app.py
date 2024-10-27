# app.py
import streamlit as st
import login
import chatbot
import planner
import welcome

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Navigation options
PAGES = {
    "Login": login.login,
    "Welcome Page": welcome.welcome,
    "Elith Chatbot": chatbot.chatbot,
    "Finance Page": planner.planner,
}

def main():
    st.sidebar.title("Navigation")
    
    if st.session_state["authenticated"]:
        # Display navigation options once logged in
        choice = st.sidebar.radio("Go to", list(PAGES.keys())[1:])  # Exclude login page
        PAGES[choice]()
        
        # Logout button
        if st.sidebar.button("Logout"):
            st.session_state["authenticated"] = False
            st.rerun()  # Refresh the app to update the navigation
    else:
        # Show the login page if not authenticated
        PAGES["Login"]()

if __name__ == "__main__":
    main()
