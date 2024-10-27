import streamlit as st

def planner():
    # Title and Introduction
    st.title("College Financial Planner")
    st.write("Welcome to your all-in-one financial planning app tailored for college students.")

    # Budget Tracker
    st.header("📊 Budget Tracker")
    income = st.number_input("Enter your total income ($):", min_value=0.0, step=0.01)
    expenses = st.number_input("Enter your total expenses ($):", min_value=0.0, step=0.01)
    if st.button("Calculate Balance"):
        balance = income - expenses
        st.write(f"Your remaining balance is: ${balance:.2f}")

    # Savings Goal Setter
    st.header("💰 Savings Goal")
    goal_amount = st.number_input("Enter your savings goal amount ($):", min_value=0.0, step=0.01)
    saved_amount = st.number_input("Enter your current savings amount ($):", min_value=0.0, step=0.01)
    if st.button("Calculate Remaining Savings"):
        remaining_savings = goal_amount - saved_amount
        st.write(f"You have ${remaining_savings:.2f} left to reach your goal.")

    # Loan Repayment Calculator
    st.header("🏦 Loan Repayment Calculator")
    principal = st.number_input("Loan Principal ($):", min_value=0.0, step=0.01)
    interest_rate = st.number_input("Annual Interest Rate (%):", min_value=0.0, step=0.01)
    years = st.number_input("Repayment Period (Years):", min_value=1, step=1)
    if st.button("Calculate Monthly Payment"):
        if interest_rate > 0:
            monthly_rate = (interest_rate / 100) / 12
            payments = years * 12
            monthly_payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** -payments)
        else:
            monthly_payment = principal / (years * 12)
        st.write(f"Your estimated monthly payment is: ${monthly_payment:.2f}")

    # End of the application
    st.write("Thank you for using the College Financial Planner. Good luck with your financial journey!")
