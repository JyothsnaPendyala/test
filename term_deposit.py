import streamlit as st
import pickle

pickle_in = open("finalised_model.pkl", "rb")
classifier = pickle.load(pickle_in)

header = st.container()
header_two = st.container()

def prediction(age,job,marital,education,balance,contact,day,month,duration,campaign,previous,poutcome,housing_new,loan_new):
    predict = classifier.predict([[age, job, marital, education, balance, contact, day, month, duration, campaign, previous, poutcome, housing_new,	loan_new]])
    return predict

with header:
    st.title("BANK TERM DEPOSIT PREDICTION")

with header_two:
    st.header("Predicts whether a person takes deposit in bank")
    age = st.text_input("Age (Enter your age)")
    job = st.text_input("Job (management = 0, technician = 1, entrepreneur = 2, blue-collar = 3, unknown = 4, retired = 5, admin. = 6, services = 7, self-employed = 8, unemployed = 9, housemaid = 10, student = 11)")
    marital = st.text_input("Marital Status (single=0, married=1, divorced=2, unknown=3)")
    education = st.text_input("Education(primary=0, secondary=1, tertiary=2, unknown=3))")
    balance = st.text_input("Balance (Enter youy balance)")
    contact = st.text_input("Contact  (cellular=0, telephone=1, unknown=2)")
    day = st.text_input("Number of days passed (enter number)")
    month = st.text_input("Last contact month (jan=0, feb=1, mar=2, apr=3, may=4, jun=5, jul=6, aug=7, sep=8. oct=9, nov=10, dec=11)")
    duration = st.text_input("Last contact duration (in sec)")
    campaign = st.text_input("Number of contacts performed in present campaign (Enter a number)")
    previous = st.text_input("Number of contacts performed in previous campaign (Enter a number)")
    poutcome = st.text_input("Outcome of the previous campaign(failure=0, success=1, unknown=2, other=3)")
    housing_new = st.text_input("Have housing loan? (Yes = 1, No = 0)")
    loan_new = st.text_input("Have personal loan? (Yes = 1, No = 0)")
    result = ''
    if st.button("Predict"):
        result = prediction(age,job,marital,education,balance,contact,day,month,duration,campaign,previous,poutcome,housing_new,loan_new)
        if result == 1:
            st.text("Customer may take term deposit in the bank" + str(result))
        else:
            st.text("Customer may not take term deposit in the bank"+ str(result))
    #st.success("The Output is {} ".format(result))