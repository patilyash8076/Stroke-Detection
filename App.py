import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt

# Load the model
with open('rf_model.pkl', 'rb') as file:
    model = pickle.load(file)

# App header and description
st.title('Stroke Prediction Web App')
st.write('Enter patient details to predict the likelihood of a stroke.')

# Function to make predictions
def predict_stroke_probability(data):
    pred = model.predict_proba(data)[0][1]
    prediction = pred*100
    if prediction > 45:
        return f'Patient is high Prone to Stroke with likelihood of: {round(prediction,2)}'
    else:
        return  f'Patient is not Prone to Stroke with likelihood of: {round(prediction,2)}'


# Input fields for user to enter patient details
gender = st.selectbox('Gender', ['Male','Female'])
age = st.number_input('Age', min_value=1, max_value=120, value=30)
hypertension = st.selectbox('Hypertension', ['Yes', 'No'])
heart_disease = st.selectbox('Heart Disease', ['Yes', 'No'])
ever_married = st.selectbox('Married', ['Yes', 'No'])
Residence_type = st.selectbox('Residence Type',["Urban","Rural"])
job_type = st.selectbox('Job Type', ["Govt_job",'Never_worked','Private','Self_employed','children'])
avg_glucose_level = st.number_input('Average Glucose Level', min_value=40, max_value=300, value=80)
bmi = st.number_input('BMI', min_value=10, max_value=60, value=25)
smoking_status = st.selectbox('Smoking Status',["never smoked", "Unknown", "formerly smoked", "smokes"])

# Mapping of user input
gender_mapping = {'Male': 1, 'Female': 0}
gender_encoded = gender_mapping[gender]

hypertension_mapping = {'Yes': 1, 'No': 0}
hypertension_encoded = hypertension_mapping[hypertension]

heart_disease_mapping = {'Yes': 1, 'No': 0}
heart_disease_encoded = heart_disease_mapping[heart_disease]

married_mapping = {"Yes": 1,"No": 0}
married_encoded = married_mapping[ever_married]

residence_mapping = {"Urban": 1, "Rural": 0}
residence_encoded = residence_mapping[Residence_type]

job_dict= {'Govt_job':0,
           'Never_worked':0,
           'Private':0,
           'Self_employed':0,
           'children':0}

if job_type in job_dict:
    job_dict[job_type] = 1
# print(job_dict)

smoke_dict = {"never smoked": 0,
             "Unknown" : 1,
             "formerly smoked" : 2,
             "smokes" : 3}
# print(smoke_dict)

# Prepared data
data = {'gender': [gender_encoded], 'age': [age], 'hypertension': [hypertension_encoded],
        'heart_disease': [heart_disease_encoded], 'ever_married':[married_encoded],
        'Residence_type':[residence_encoded],'Govt_job':[job_dict['Govt_job']],'Never_worked':[job_dict['Never_worked']],
        'Private':[job_dict['Private']],'Self_employed':[job_dict['Self_employed']],'children':[job_dict['children']],
        'avg_glucose_level': [avg_glucose_level], 'bmi': [bmi],'smoking_status':[smoke_dict[smoking_status]]}
input_df = pd.DataFrame(data)
# print(input_df.values)

# Predicticting
if st.button('Predict Stroke Probability', key='predict_button'):
    prediction = predict_stroke_probability(input_df)
    styled_prediction = f'<p style="font-size: 24px; color: lack; font-weight: bold;">{prediction}%</p>'
    st.write(styled_prediction, unsafe_allow_html=True)
