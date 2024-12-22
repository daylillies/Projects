import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

# Title of the app
st.write("""
# Simple Iris Flower Prediction App

This app predicts the **Iris flower** type
""")

# Sidebar user input
st.sidebar.header('User Input Parameters')

def user_input_features():
    """Function to capture user input"""
    features = {
        'sepal_length': st.sidebar.slider('Sepal length', 4.3, 7.9, 5.4),
        'sepal_width': st.sidebar.slider('Sepal width', 2.0, 4.4, 3.4),
        'petal_length': st.sidebar.slider('Petal length', 1.0, 6.9, 1.3),
        'petal_width': st.sidebar.slider('Petal width', 0.1, 2.5, 0.2)
    }
    return pd.DataFrame(features, index=[0])

# Get user input features
df = user_input_features()

# Display user input
st.subheader('User Input parameters')
st.write(df)

# Load iris dataset and initialize model
iris = datasets.load_iris()
X, Y = iris.data, iris.target
clf = RandomForestClassifier().fit(X, Y)

# Prediction
prediction = clf.predict(df)
prediction_proba = clf.predict_proba(df)

# Output results
st.subheader('Class labels and their corresponding index number')
st.write(iris.target_names)

st.subheader('Prediction')
st.write(iris.target_names[prediction])

st.subheader('Prediction Probability')
st.write(prediction_proba)
