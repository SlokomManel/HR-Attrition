from pycaret.classification import *
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import joblib
import shap
import lime
from lime import lime_tabular


# IMPORT/LOAD
gbc = load_model('models/gbc_model') # GBC model
final_gbc = load_model('models/final_gbc') # final GBC model

prep_pipe = joblib.load("prep_pipe.pkl") # Pycaret preparation pipeline

train_data = pd.read_csv("data/preprocessed_data.csv") # Preprocessed data used in training
original = pd.read_csv("data/HR Employee Attrition.csv")


def get_prediction_df(input_df, model):
    """
    Get prediction using the gbc model
    """
    predictions_df = predict_model(estimator = model, data = input_df)
    return predictions_df

def process_using_pipeline(input_df, pipe):
    """
    Process the data using the Pycaret pipeline
    """
    return pipe.transform(input_df)

def st_explanation(plot, height=None):
    """
    Plot the explanation within the streamlit app
    """
    html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(html, height = height)

def st_shap(plot, height=None):
    """
    Plot the explanation within the streamlit app
    """
    html = f"<head>{shap.getjs()}</head><body>{plot}</body>"
    components.html(html, height = height)

def run():

    # Expand the layout
    st.set_page_config(layout = "wide")

    # Select whether or not to do single row or multiple row predictions
    add_selectbox = st.sidebar.selectbox("Single or Multi predict?", ("Single", "Multi"))
    
    # Title
    st.title("HR Attrition")
    st.subheader("Using this app you can identify whether an employee(s) will potentially leave in the next six months and also why.")

    # Initialise columns
    col1, col2, col3, col4 = st.beta_columns(4)

    # Create individual app elements to provide input for single row prediction
    if add_selectbox == "Single":

        with col1:
            Age = st.number_input("Age", min_value = 18, max_value = 100, step = 1)
            BusinessTravel = st.select_slider("BusinessTravel", options = ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'])
            DailyRate = st.number_input("DailyRate", min_value = 100, max_value = 1500, step = 1)
            Department = st.select_slider("Department", options = ['Sales', 'Research & Development', 'Human Resources'])
            DistanceFromHome = st.number_input("DistanceFromHome", min_value = 1, max_value = 30, step = 1)
            Education = st.select_slider("Education", options = [1, 2, 3, 4, 5])
            EducationField = st.select_slider("EducationField", options = ['Life Sciences', 'Other', 'Medical', 'Marketing', 'Technical Degree', 'Human Resources'])
            EnvironmentSatisfaction = st.select_slider("EnvironmentSatisfaction", options = [1, 2, 3, 4])
            
        with col2:
            Gender = st.select_slider("Gender", options = ["Female", "Male"])
            HourlyRate = st.number_input("HourlyRate", min_value = 1, max_value = 100, step = 1)
            JobInvolvement = st.select_slider("JobInvolvement", options = [1, 2, 3, 4])
            JobLevel = st.select_slider("JobLevel", options = [1, 2, 3, 4, 5])
            JobRole = st.select_slider("JobRole", options = ['Sales Executive', 'Research Scientist', 'Laboratory Technician', 'Manufacturing Director', 'Healthcare Representative', 'Manager', 'Sales Representative', 'Research Director', 'Human Resources'])
            JobSatisfaction = st.select_slider("JobSatisfaction", options = [1, 2, 3, 4])
            MaritalStatus = st.select_slider("MaritalStatus", options = ['Single', 'Married', 'Divorced'])
            MonthlyIncome = st.number_input("MonthlyIncome", min_value = 1000, max_value = 20000, step = 1)
            
        with col3:
            MonthlyRate = st.number_input("MonthlyRate", min_value = 2000, max_value = 27000, step = 1)
            NumCompaniesWorked = st.slider("NumCompaniesWorked", min_value = 0, max_value = 9, step = 1)
            #Over18 = st.select_slider("Over18", options = ["N", "Y"])
            OverTime = st.select_slider("OverTime", options = ["N", "Y"])
            PercentSalaryHike = st.number_input("PercentSalaryHike", min_value = 10, max_value = 25, step = 1)
            PerformanceRating = st.number_input("PerformanceRating", min_value = 3, max_value = 4, step = 1)
            RelationshipSatisfaction = st.select_slider("RelationshipSatisfaction", options = [1, 2, 3, 4])
            # StandardHours =
            StockOptionLevel = st.select_slider("StockOptionLevel", options = [0, 1, 2, 3])
            TotalWorkingYears = st.slider("TotalWorkingYears", min_value = 0, max_value = 40, step = 1)
            
        with col4:
            TrainingTimesLastYear = st.slider("TrainingTimesLastYear", min_value = 0, max_value = 6, step = 1)
            WorkLifeBalance = st.slider("WorkLifeBalance", min_value = 0, max_value = 4, step = 1)
            YearsAtCompany = st.slider("YearsAtCompany", min_value = 0, max_value = 40, step = 1)
            YearsInCurrentRole = st.slider("YearsInCurrentRole", min_value = 0, max_value = 18, step = 1)
            YearsSinceLastPromotion = st.slider("YearsSinceLastPromotion", min_value = 0, max_value = 15, step = 1)
            YearsWithCurrManager = st.slider("YearsWithCurrManager", min_value = 0, max_value = 18, step = 1)

        output = ""

        input_dict = {"Age" : Age, 
                    "BusinessTravel" :  BusinessTravel ,
                    "DailyRate" :  DailyRate ,
                    "Department" :  Department ,
                    "DistanceFromHome" :  DistanceFromHome ,
                    "Education" :  Education ,
                    "EducationField" :  EducationField ,
                    "EnvironmentSatisfaction" :  EnvironmentSatisfaction ,
                    "Gender" :  Gender ,
                    "HourlyRate" :  HourlyRate ,
                    "JobInvolvement" :  JobInvolvement ,
                    "JobLevel" :  JobLevel ,
                    "JobRole" :  JobRole ,
                    "JobSatisfaction" :  JobSatisfaction ,
                    "MaritalStatus" :  MaritalStatus ,
                    "MonthlyIncome" :  MonthlyIncome ,
                    "MonthlyRate" :  MonthlyRate ,
                    "NumCompaniesWorked" :  NumCompaniesWorked ,
                    #"Over18" :  Over18 ,
                    "OverTime" :  OverTime ,
                    "PercentSalaryHike" :  PercentSalaryHike ,
                    "PerformanceRating" :  PerformanceRating ,
                    "RelationshipSatisfaction" :  RelationshipSatisfaction ,
                    "StockOptionLevel" :  StockOptionLevel ,
                    "TotalWorkingYears" :  TotalWorkingYears ,
                    "TrainingTimesLastYear" :  TrainingTimesLastYear ,
                    "WorkLifeBalance" :  WorkLifeBalance ,
                    "YearsAtCompany" :  YearsAtCompany ,
                    "YearsInCurrentRole" :  YearsInCurrentRole ,
                    "YearsSinceLastPromotion" :  YearsSinceLastPromotion ,
                    "YearsWithCurrManager" :  YearsWithCurrManager}

        # Create row of data based upon the element inputs
        input_df = pd.DataFrame([input_dict])
 
        # Make single prediction for data input using the model
        if st.button("Predict"):

            # Get the prediction and score (takes the original dataframe and adds it on)
            prediction_df = get_prediction_df(input_df, final_gbc)

            # Grab the prediction label
            prediction_label = prediction_df['Label'][0]

            # Output of the prediction i.e. Yes/No
            st.success('{} this person will leave.'.format(prediction_label))

            # Preprocess the inputted data
            new_processed = process_using_pipeline(prediction_df, prep_pipe)

            # Create shap tree explainer
            test = shap.TreeExplainer(final_gbc['trained_model'], data = train_data, model_output = "probability")

            # Get shap values for new data
            sv = test.shap_values(new_processed.iloc[0])

            
            summary_df = pd.DataFrame([train_data.columns, sv]).T
            summary_df.columns = ['feature', 'shap_value']

            mapping = {}

            for feature in summary_df.feature.values:
                mapping[feature] = feature
                for prefix, alternative in zip(['BusinessTravel', 'Department', 'EducationField', 'Gender', 'JobLevel', 'JobRole', 'MaritalStatus', 'OverTime'],
                                            ['BusinessTravel', 'Department', 'EducationField', 'Gender', 'JobLevel', 'JobRole', 'MaritalStatus', 'OverTime']):
                    if feature.startswith(prefix):
                        mapping[feature] = alternative
                        break

            summary_df['feature'] = summary_df.feature.map(mapping)

            shap_df = summary_df.groupby('feature').sum().reset_index()

            # Plot the inputted data's shap plot
            st_explanation(shap.force_plot(base_value = test.expected_value,
                                            shap_values = shap_df.shap_value.values,
                                            features = input_df,
                                            feature_names = list(original.drop(["EmployeeNumber", "StandardHours", "EmployeeCount", "Over18", "Attrition"], axis = 1).columns),
                                            text_rotation = 180))


    # Batch prediction (multiple people to predict)
    if add_selectbox == "Multi":

        # Upload rows to predict
        file_upload = st.file_uploader("Upload csv file for predictions", type = ["csv"])

        # Make prediction and output data
        if file_upload is not None:
            data = pd.read_csv(file_upload)
            predictions = predict_model(estimator = gbc, data = data)
            st.write(predictions)

if __name__ == '__main__':
    run()