import streamlit as st
st.title("Streamlit Dashboard")
st.markdown("Cleaned dataset")

import pandas as pd

df = pd.read_csv("assignment11/cleaned_procurement_data.csv")  
st.subheader("Dataset Preview")
st.dataframe(df)

st.subheader("Dataset Summary")
st.write(df.describe())

st.subheader("Dataset Summary")
st.markdown("""
- Fill missing values on Defective_Units with 0
- Converted dates to datetime format
- Fill missing values od Delivery_Date with Na
""")

import plotly.express as px

st.subheader("Orders over Time")
bar_chart = px.bar(df, x='Order_Date', y='Quantity') 
st.plotly_chart(bar_chart)

st.subheader("POs by Date")
line_chart = px.line(df, x='Delivery_Date', y='Defective_Units') 
st.plotly_chart(line_chart)

