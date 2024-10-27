# welcome.py
import streamlit as st

def welcome():
    st.title("Welcome to SmartStride!")
    st.write("This is your personalized dashboard. Use the navigation sidebar to explore different sections.")
    st.image("assistant.png", use_column_width=True)
    st.write("""
        - Navigate to the Elith Chatbot page for assistance.
        - Use the Finance Page for planning your expenses.
        - More features coming soon!
    """)
