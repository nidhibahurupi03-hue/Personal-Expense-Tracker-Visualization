import streamlit as st
import pandas as pd
import plotly.express as px

from database.db import connect, create_tables, add_expense

# ---------------- INIT DB ----------------
create_tables()

# ---------------- UI ----------------
st.set_page_config(page_title="FinBoss AI", layout="wide")

st.title("🏦 FinBoss AI - Personal Finance System")

# ---------------- ADD EXPENSE UI ----------------
st.sidebar.subheader("➕ Add Expense")

date = st.sidebar.date_input("Date")
category = st.sidebar.text_input("Category")
amount = st.sidebar.number_input("Amount", min_value=0.0)
payment = st.sidebar.selectbox("Payment Method", ["UPI", "Cash", "Card"])
description = st.sidebar.text_input("Description")

if st.sidebar.button("Add Expense"):
    if category and amount > 0:
        add_expense(date, category, amount, payment, description)
        st.success("✅ Expense Added Successfully!")
        st.rerun()
    else:
        st.warning("⚠ Fill all fields properly")

# ---------------- LOAD DATA ----------------
conn = connect()
df = pd.read_sql_query("SELECT * FROM expenses", conn)

# ---------------- EMPTY CHECK ----------------
if df.empty:
    st.warning("No data found. Please add expenses from sidebar.")
    st.stop()

# ---------------- CLEAN DATA ----------------
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.month_name()

# ---------------- FILTER ----------------
st.sidebar.subheader("🔍 Filters")

category_filter = st.sidebar.multiselect("Category", df["category"].unique())

payment_filter = st.sidebar.multiselect("Payment", df["payment"].unique())

filtered = df.copy()

if category_filter:
    filtered = filtered[filtered["category"].isin(category_filter)]

if payment_filter:
    filtered = filtered[filtered["payment"].isin(payment_filter)]

# ---------------- KPIs ----------------
st.subheader("📊 Dashboard Overview")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total", f"₹ {filtered['amount'].sum():,.2f}")
col2.metric("📊 Avg", f"₹ {filtered['amount'].mean():,.2f}")
col3.metric("📦 Transactions", len(filtered))

# ---------------- CATEGORY CHART ----------------
st.subheader("📊 Category Analysis")

cat = filtered.groupby("category")["amount"].sum().reset_index()

fig1 = px.bar(cat, x="category", y="amount", color="category")
st.plotly_chart(fig1, use_container_width=True)

# ---------------- MONTHLY ----------------
st.subheader("📈 Monthly Trend")

mon = filtered.groupby("month")["amount"].sum().reset_index()

fig2 = px.line(mon, x="month", y="amount", markers=True)
st.plotly_chart(fig2, use_container_width=True)

# ---------------- PAYMENT ----------------
st.subheader("💳 Payment Analysis")

pay = filtered.groupby("payment")["amount"].sum().reset_index()

fig3 = px.pie(pay, values="amount", names="payment")
st.plotly_chart(fig3, use_container_width=True)

# ---------------- TABLE ----------------
st.subheader("📄 Data Table")

st.dataframe(filtered)