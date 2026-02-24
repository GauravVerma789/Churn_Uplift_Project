import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Uplift Dashboard", layout="wide")

st.title("Customer Uplift Modeling Dashboard")

# Load dataset
df = pd.read_csv("./data/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv")

# Create treatment flag
df["treatment"] = df["segment"].apply(lambda x: 0 if x=="No E-Mail" else 1)

# Fake uplift scores (use your real predictions later)
np.random.seed(42)
df["uplift_score"] = np.random.normal(0,0.02,len(df))

# ----------------------
# Dataset Overview
# ----------------------

st.subheader("Dataset Overview")
col1,col2,col3 = st.columns(3)

col1.metric("Total Customers", len(df))
col2.metric("Conversion Rate", round(df["conversion"].mean(),4))
col3.metric("Treatment Rate", round(df["treatment"].mean(),4))

# ----------------------
# Uplift Distribution
# ----------------------

st.subheader("Uplift Score Distribution")
st.bar_chart(df["uplift_score"])

# ----------------------
# Decile Analysis
# ----------------------

st.subheader("Decile Performance")

df["decile"] = pd.qcut(df["uplift_score"], 10, labels=False)

decile_perf = df.groupby("decile")["conversion"].mean().sort_index(ascending=False)

st.line_chart(decile_perf)

# ----------------------
# Targeting Simulator
# ----------------------

st.subheader("Targeting Simulator")

percent = st.slider("Select Top % Customers to Target", 10,100,20)

top_n = int(len(df)*(percent/100))
targeted = df.sort_values("uplift_score",ascending=False).head(top_n)

st.write("Targeted Users:", len(targeted))
st.metric("Expected Conversion Rate", round(targeted["conversion"].mean(),4))

# ----------------------
# ROI Estimator
# ----------------------

st.subheader("ROI Estimator")

cost = st.number_input("Cost per Email ($)",0.0,5.0,0.5)
revenue = st.number_input("Revenue per Conversion ($)",1.0,500.0,50.0)

expected_profit = (targeted["conversion"].sum()*revenue) - (len(targeted)*cost)

st.metric("Estimated Profit", round(expected_profit,2)) 