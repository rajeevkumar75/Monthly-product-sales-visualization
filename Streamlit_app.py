import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Page Config
st.set_page_config(page_title="🛍️ Retail Sales Dashboard", layout="wide")


# Title & Header
st.title("📊 Monthly Product Sales Visualization")
st.markdown("Analyze monthly sales data with full EDA, key metrics, and visual insights from your retail dataset.")


# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv("retail_sales_dataset.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.strftime('%b')    
    df['Month_Num'] = df['Date'].dt.month              
    return df

df = load_data()

# Filter Data
months = sorted(df['Month'].unique(), key=lambda x: pd.to_datetime(x, format='%b').month)
selected_months = st.sidebar.multiselect("📅 Filter by Month", months, default=months)
filtered_df = df[df['Month'].isin(selected_months)]


# KPI Metrics
st.subheader("📌 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Revenue", f"₹{filtered_df['Total Amount'].sum():,.0f}")
col2.metric("📦 Total Units Sold", f"{filtered_df['Quantity'].sum():,}")
col3.metric("🏆 Top Category", filtered_df.groupby('Product Category')['Total Amount'].sum().idxmax())

# EDA Section
st.markdown("---")
st.subheader("📋 Exploratory Data Analysis")

with st.expander("🔍 Dataset Preview"):
    st.dataframe(df.head())

with st.expander("🧠 Basic Information"):
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Data Types:**")
        st.dataframe(df.dtypes)
    with col2:
        st.write("**Missing Values:**")
        st.dataframe(df.isnull().sum())

with st.expander("📈 Statistical Summary"):
    st.dataframe(df.describe())

with st.expander("📊 Distribution Analysis"):
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Product Category Count**")
        cat_counts = df['Product Category'].value_counts()
        fig_cat, ax_cat = plt.subplots()
        sns.barplot(x=cat_counts.index, y=cat_counts.values, ax=ax_cat, palette="Set2")
        ax_cat.set_title("Transactions per Product Category")
        plt.xticks(rotation=30)
        st.pyplot(fig_cat)

    with col2:
        st.write("**Gender Distribution**")
        fig_gender, ax_gender = plt.subplots()
        sns.countplot(x='Gender', data=df, ax=ax_gender, palette='pastel')
        ax_gender.set_title("Customer Gender Distribution")
        st.pyplot(fig_gender)

with st.expander("👤 Age Distribution"):
    fig_age, ax_age = plt.subplots()
    sns.histplot(df['Age'], bins=15, kde=True, color='skyblue', ax=ax_age)
    ax_age.set_title("Customer Age Distribution")
    ax_age.set_xlabel("Age")
    st.pyplot(fig_age)

with st.expander("💸 Revenue by Category"):
    cat_rev = df.groupby('Product Category')['Total Amount'].sum().sort_values()
    fig_rev, ax_rev = plt.subplots()
    cat_rev.plot(kind='barh', ax=ax_rev, color='orange')
    ax_rev.set_title("Total Revenue by Product Category")
    st.pyplot(fig_rev)

# Visualization Section
st.markdown("---")
st.subheader("📊 Visual Analysis")

# Bar Chart: Units Sold by Category
st.markdown("### 🔹 Units Sold by Product Category")
prod_sales = filtered_df.groupby('Product Category')['Quantity'].sum().sort_values(ascending=False)
fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.barplot(x=prod_sales.index, y=prod_sales.values, ax=ax1, palette='coolwarm')
ax1.set_title("Total Units Sold by Product Category")
ax1.set_ylabel("Units Sold")
st.pyplot(fig1)

# Line Chart: Monthly Revenue Trend
st.markdown("### 🔹 Monthly Revenue Trend")
monthly_rev = filtered_df.groupby('Month_Num')['Total Amount'].sum().reset_index()
monthly_rev['Month'] = monthly_rev['Month_Num'].apply(lambda x: pd.to_datetime(str(x), format='%m').strftime('%b'))
monthly_rev = monthly_rev.sort_values('Month_Num')
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=monthly_rev, x='Month', y='Total Amount', marker='o', ax=ax2, color='green')
ax2.set_title("Monthly Revenue Trend")
ax2.set_ylabel("Revenue")
ax2.grid(True)
st.pyplot(fig2)

# Pie Chart: Revenue Contribution
st.markdown("### 🔹 Revenue Contribution by Category")
cat_share = filtered_df.groupby('Product Category')['Total Amount'].sum()
fig3, ax3 = plt.subplots(figsize=(4, 4))
cat_share.plot.pie(autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'), ax=ax3)
ax3.set_ylabel("")
ax3.set_title("Revenue Share by Product Category")
st.pyplot(fig3)


# Footer
st.markdown("---")
st.markdown("Made with ❤️ by **Rajeev Kumar** for Guvi project")
