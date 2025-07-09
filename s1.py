import streamlit as st
from datetime import date 

st.write("Hello harsh")

breakfast = st.selectbox("Chouse your BreakFast ",["Tea","Milk","Coffie"])
st.write(f"You select {breakfast}")

sport = st.checkbox("Add Extra suger")

if sport:
    st.write(f"Suger Added in {breakfast} ")

gender = st.radio("Enter Gender : ",["Male","Female","Others"])

st.slider("Suger Level",0,5,1)


st.number_input("How many Cups",min_value=1,max_value=10,step=1)

name = st.text_input("Enter your Name")
if name :
    st.write(f"Welcome, {name} ! Your {breakfast} is on the way ")


dob = st.date_input("select Your Date Of birth",min_value=date(1990,1,1),max_value=date.today())
st.write(f"Your Date of borth is : {dob}")

if st.button("Count Day"):  
    todaydate = date.today()
    days_old = (dob-todaydate).days
    st.write(f"You are {int(days_old//365)} year old.")
    st.success("Data Submited Successfully..")



