import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
import numpy as np
import pickle
import tensorflow as tf
import streamlit as st

# Load the model
model = tf.keras.models.load_model("model.h5")

# Load the scaler and encoder files
with open("label_encoder_gender.pkl", "rb") as file:
    label_encoder_gender = pickle.load(file)

with open("onehot_encoder_geo.pkl", "rb") as file:
    onehot_encoder_geo = pickle.load(file)

with open("scaler.pkl", "rb") as file:
    scaler = pickle.load(file)

# Streamlit title
st.title("Customer Churn Prediction")

# User input
geography = st.selectbox('Geography', onehot_encoder_geo.categories_[0])
gender = st.selectbox('Gender', label_encoder_gender.classes_)
age = st.slider('Age', 18, 92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
estimated_salary = st.number_input('Estimated Salary')
tenure = st.slider('Tenure', 0, 10)
num_of_products = st.slider('Number of Products', 1, 4)
has_cr_card = st.selectbox('Has Credit Card', [0, 1])
is_active_member = st.selectbox('Is Active Member', [0, 1])

# Prepare the input data
input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Gender': [label_encoder_gender.transform([gender])[0]],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary],
    'Geography': [geography]
})

# OneHotEncode Geography
encoded = onehot_encoder_geo.transform(input_data[['Geography']]).toarray()
encoded_df = pd.DataFrame(encoded, columns=onehot_encoder_geo.get_feature_names_out(['Geography']))

# Combine one-hot encoded columns with input data
input_data = pd.concat([input_data.reset_index(drop=True), encoded_df], axis=1)
input_data = input_data.drop(columns=['Geography'])  # Drop original Geography column

# Scale the input data
input_scaled = scaler.transform(input_data)

# Make predictions
prediction = model.predict(input_scaled)
prediction_prob = prediction[0][0]

# Display results
st.write(f'Churn Probability: {prediction_prob:.2f}')
if prediction_prob > 0.5:
    st.write("Customer is likely to churn")
else:
    st.write("Customer is not likely to churn")