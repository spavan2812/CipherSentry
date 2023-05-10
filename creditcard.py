import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import streamlit as st


data = pd.read_csv('dataset.csv')


st.title("Credit Card Fraud Detection")
st.write("Here's a quick look at the data:")
st.write(data.head())

st.write("Checking for Missing Data:")
st.write(data.isnull().sum())


st.write("Visualizing the Class Distribution:")
sns.countplot('Class', data=data)
plt.title('Class Distribution (0: No Fraud | 1: Fraud)')
st.pyplot()


st.write("Splitting the Data into Train and Test Sets:")
X = data.drop('Class', axis=1)
y = data['Class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


st.write("Building the Logistic Regression Model:")
lr = LogisticRegression()
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)
acc = accuracy_score(y_test, y_pred)
st.write(f"Model Accuracy: {acc}")


st.write("Enter the transaction details below to check if it's fraudulent or not:")
time = st.text_input("Time (in seconds)")
v1 = st.text_input("V1")
v2 = st.text_input("V2")
v3 = st.text_input("V3")
v4 = st.text_input("V4")
v5 = st.text_input("V5")
v6 = st.text_input("V6")
v7 = st.text_input("V7")
v8 = st.text_input("V8")
v9 = st.text_input("V9")
v10 = st.text_input("V10")
v11 = st.text_input("V11")
v12 = st.text_input("V12")
v13 = st.text_input("V13")
v14 = st.text_input("V14")
v15 = st.text_input("V15")
v16 = st.text_input("V16")
v17 = st.text_input("V17")
v18 = st.text_input("V18")
v19 = st.text_input("V19")
v20 = st.text_input("V20")
v21 = st.text_input("V21")
v22 = st.text_input("V22")
v23 = st.text_input("V23")
v24 = st.text_input("V24")
v25 = st.text_input("V25")
v26 = st.text_input("V26")
v27 = st.text_input("V27")
v28 = st.text_input("V28")
amount = st.text_input("Amount")

input_data = [time, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, amount]
input_data = np.array(input_data).reshape(1,-1)
if st.button("Predict"):
    prediction = lr.predict(input_data)
    if prediction == 0:
        st.write("The transaction is not fraudulent.")
    else:
        st.write("The transaction is fraudulent.")