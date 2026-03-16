import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="wide"
)

# Get the absolute path to the housing1 directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
housing1_path = os.path.join(BASE_DIR, 'House_Price_Prediction-main', 'housing1')
DATA_PATH = os.path.join(housing1_path, "Data", "house_price.csv")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df

def train_model(df):
    X = df.drop("Price", axis=1)
    y = df["Price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model, X_train, X_test, y_train, y_test

# Load data
df = load_data()
model, X_train, X_test, y_train, y_test = train_model(df)

# Title
st.title("🏠 House Price Prediction")
st.markdown("Predict house prices based on property features using Machine Learning")

# Sidebar
st.sidebar.header("Property Features")

area = st.sidebar.number_input("Area (sq ft)", min_value=500, max_value=5000, value=1500, step=100)
bedrooms = st.sidebar.selectbox("Bedrooms", [1, 2, 3, 4, 5], index=2)
bathrooms = st.sidebar.selectbox("Bathrooms", [1, 2, 3, 4], index=1)
stories = st.sidebar.selectbox("Stories", [1, 2, 3], index=0)
parking = st.sidebar.selectbox("Parking Spaces", [0, 1, 2, 3], index=1)
age = st.sidebar.number_input("Age of House (years)", min_value=0, max_value=50, value=10, step=1)
location = st.sidebar.selectbox("Location", ["Urban", "Suburban", "Rural"], index=0)
location_map = {"Urban": 1, "Suburban": 2, "Rural": 3}
location_val = location_map[location]

# Prediction
if st.sidebar.button("Predict Price", type="primary"):
    input_data = np.array([[area, bedrooms, bathrooms, stories, parking, age, location_val]])
    prediction = model.predict(input_data)[0]
    
    st.success(f"### Predicted House Price: ₹ {int(prediction):,}")
    
    # Show similar properties
    st.subheader("Similar Properties in Dataset")
    similar = df[
        (df['Area'] >= area - 200) & (df['Area'] <= area + 200) &
        (df['Bedrooms'] == bedrooms)
    ].head(5)
    st.dataframe(similar.style.format({"Price": "₹ {:,.0f}"}))

# Main content - Tabs
tab1, tab2, tab3 = st.tabs(["📊 Data Overview", "📈 Visualizations", "🤖 Model Info"])

with tab1:
    st.subheader("Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Properties", len(df))
    col2.metric("Average Price", f"₹ {df['Price'].mean():,.0f}")
    col3.metric("Min Price", f"₹ {df['Price'].min():,.0f}")
    col4.metric("Max Price", f"₹ {df['Price'].max():,.0f}")
    
    st.subheader("Raw Data")
    st.dataframe(df.style.format({"Price": "₹ {:,.0f}"}))

with tab2:
    st.subheader("Price Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['Price'], kde=True, ax=ax)
    ax.set_xlabel("Price (₹)")
    ax.set_ylabel("Count")
    st.pyplot(fig)
    
    st.subheader("Price vs Area")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='Area', y='Price', hue='Bedrooms', ax=ax2)
    ax2.set_xlabel("Area (sq ft)")
    ax2.set_ylabel("Price (₹)")
    st.pyplot(fig2)
    
    st.subheader("Correlation Heatmap")
    fig3, ax3 = plt.subplots(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax3)
    st.pyplot(fig3)

with tab3:
    st.subheader("Model Information")
    st.write("**Algorithm:** Linear Regression")
    st.write("**Features Used:**")
    st.write("- Area (sq ft)")
    st.write("- Number of Bedrooms")
    st.write("- Number of Bathrooms")
    st.write("- Number of Stories")
    st.write("- Parking Spaces")
    st.write("- Age of House")
    st.write("- Location (Urban/Suburban/Rural)")
    
    # Model performance
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    st.subheader("Model Performance")
    col1, col2 = st.columns(2)
    col1.metric("Training R² Score", f"{train_score:.3f}")
    col2.metric("Testing R² Score", f"{test_score:.3f}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and Scikit-Learn")
