import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pytz

# CSV published link for sheets
             
sheet_nutri = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSbTXMRRDRlwUjBWHEH3vonSAMdeAO_Msd7vzilOEn1Xcgq4mczGbThacy28t2XHVK8yMOf29-bvGWl/pub?gid=1213091586&single=true&output=csv"
df_nutri = pd.read_csv(sheet_nutri)

# NUTRITION SHEET

# Data Cleaning and Type Conversion
df_nutri.dropna(how='all', inplace=True)

# Convert date and numerical columns
df_nutri['Date'] = pd.to_datetime(df_nutri['Date'], errors='coerce')
df_nutri['Kcal'] = pd.to_numeric(df_nutri['Kcal'], errors='coerce')
df_nutri['Protein'] = pd.to_numeric(df_nutri['Protein'], errors='coerce')
df_nutri['Carbs'] = pd.to_numeric(df_nutri['Carbs'], errors='coerce')
df_nutri['Fat'] = pd.to_numeric(df_nutri['Fat'], errors='coerce')
df_nutri['Maintenance'] = pd.to_numeric(df_nutri['Maintenance'], errors='coerce')
df_nutri['Rec Prot'] = pd.to_numeric(df_nutri['Rec Prot'], errors='coerce')
df_nutri['Deficit'] = pd.to_numeric(df_nutri['Deficit'], errors='coerce')
# df_nutri['Weight (Kg)'] = pd.to_numeric(df_nutri['Weight (Kg)'], errors='coerce') # Ya es float64

# Dealing with missing values

mask = df_nutri['Weight (Kg)'].isna()
df_nutri.loc[mask, 'Weight (Kg)'] = (
    df_nutri['Weight (Kg)']
    .rolling(7, min_periods=1, center=True)
    .median() # We imputed the median for missing values
)

# Add 7 days moving average/median
df_nutri['Calories_7dMed'] = df_nutri['Kcal'].rolling(window=7).median() # Moving Median
df_nutri['Deficit_7dMed'] = df_nutri['Deficit'].rolling(window=7).median() # Moving Median
df_nutri['Protein_7dMed'] = df_nutri['Protein'].rolling(window=7).median() # Moving Median
df_nutri['Carbs_7dMed'] = df_nutri['Carbs'].rolling(window=7).median() # Moving Median
df_nutri['Fat_7dMed'] = df_nutri['Fat'].rolling(window=7).median() # Moving Median
df_nutri['Cals_Protein'] = 4 * df_nutri['Protein']
df_nutri['Cals_Carbs'] = 4 * df_nutri['Carbs']
df_nutri['Cals_Fat'] = 9 * df_nutri['Fat']
df_nutri['Total_Cals'] = df_nutri['Cals_Protein'] + df_nutri['Cals_Carbs'] + df_nutri['Cals_Fat']
df_nutri['Pct_Cals_Protein'] = 100 * df_nutri['Cals_Protein']/df_nutri['Total_Cals']
df_nutri['Pct_Cals_Carbs'] = 100 * df_nutri['Cals_Carbs']/df_nutri['Total_Cals']
df_nutri['Pct_Cals_Fat'] = 100 * df_nutri['Cals_Fat']/df_nutri['Total_Cals']
df_nutri['Pct_7dMA_Protein'] = df_nutri['Pct_Cals_Protein'].rolling(window=7).mean()
df_nutri['Pct_7dMA_Carbs'] = df_nutri['Pct_Cals_Carbs'].rolling(window=7).mean()
df_nutri['Pct_7dMA_Fat'] = df_nutri['Pct_Cals_Fat'].rolling(window=7).mean()
df_nutri['Weight_7dMed'] = df_nutri['Weight (Kg)'].rolling(window=7).median() # Moving Median

# Sidebar options
st.sidebar.image("logo.png", width=150)
st.sidebar.markdown("## Navigation")
view = st.sidebar.radio("Choose Plot:", ["Weight", "Calorie Intake", "Calorie Deficit/Surplus", 
                                         "Protein", "Carbohydrates", "Fat", "Percentages"])

# Title
st.title("Alexandra Álvarez: Daily Calorie and Macronutrient Tracker")
st.caption("Built with Python 💻 | Powered by Discipline 💪")

# Show plot
if view == "Weight":
    fig = px.line(df_nutri, x='Date', y=['Weight (Kg)', 'Weight_7dMed'], 
                  title='Daily Weight in Kg',
                  labels={'value': 'Weight (Kg)'})                 
    fig.for_each_trace(
     lambda t: t.update(name='7 day moving median') if t.name == 'Weight_7dMed' else None)
    st.plotly_chart(fig, use_container_width=True)

elif view == "Calorie Intake":
    fig = px.line(df_nutri, x='Date', y=['Kcal', 'Maintenance', 'Calories_7dMed'], 
                  title='Daily Calories',
                  labels={'value': 'Calories'})                 
    fig.for_each_trace(
     lambda t: t.update(name='7 day moving median') if t.name == 'Calories_7dMed' else None)                
    st.plotly_chart(fig, use_container_width=True)

elif view == "Calorie Deficit/Surplus":
     fig = px.line(df_nutri, x='Date', y=['Deficit', 'Deficit_7dMed'],
                  title='Daily Calorie Deficit/Surplus',
                  labels={'value': 'Calories'})                 
     fig.for_each_trace(
     lambda t: t.update(name='7 day moving median') if t.name == 'Deficit_7dMed' else None) 
     # Add horizontal line at y = 0
     fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Zero Line", annotation_position="top left")
     st.plotly_chart(fig, use_container_width=True)

elif view == "Protein":
    fig = px.line(df_nutri, x='Date', y=['Protein', 'Rec Prot', 'Protein_7dMed'],
                  title='Daily Protein',
                  labels={'value': 'Grams'})
    fig.for_each_trace(
         lambda t: t.update(name='7 day moving median') if t.name == 'Protein_7dMed' else None) 
    st.plotly_chart(fig, use_container_width=True)

elif view == "Carbohydrates":
    fig = px.line(df_nutri, x='Date', y=['Carbs', 'Carbs_7dMed'],
                  title='Daily Carbohydrates',
                  labels={'value': 'Grams'})
    fig.for_each_trace(
         lambda t: t.update(name='7 day moving median') if t.name == 'Carbs_7dMed' else None) 
    st.plotly_chart(fig, use_container_width=True)

elif view == "Fat":
    fig = px.line(df_nutri, x='Date', y=['Fat', 'Fat_7dMed'],
                  title='Daily Fat',
                  labels={'value': 'Grams', 'Date': 'Date'})
    fig.for_each_trace(
         lambda t: t.update(name='7 day moving median') if t.name == 'Fat_7dMed' else None) 
    st.plotly_chart(fig, use_container_width=True)

elif view == "Percentages":
    fig = px.line(df_nutri, x='Date', y=['Pct_Cals_Protein', 'Pct_7dMA_Protein', 'Pct_Cals_Carbs', 'Pct_7dMA_Carbs', 'Pct_Cals_Fat', 'Pct_7dMA_Fat'],
                  title='Percentages Of Calories For Each Macro',
                  labels={'value': 'Percent', 'Date': 'Date'})
    # Líneas de referencia para tus metas de macros
    fig.add_hline(y=35, line_dash="dot", line_color="blue", 
                   annotation_text="Protein Goal (35%)", annotation_position="top right")

    fig.add_hline(y=45, line_dash="dot", line_color="red", 
                   annotation_text="Carbs Goal (45%)", annotation_position="top left")

    fig.add_hline(y=20, line_dash="dot", line_color="green", 
                   annotation_text="Fat Goal (20%)", annotation_position="bottom left")
    st.plotly_chart(fig, use_container_width=True)

# Optional footer
st.markdown("---")
st.markdown("📬 **Let's connect!**  \n[YouTube @LiftIQ](https://youtu.be/mWHC0rZiGhc?t=2) · [GitHub](https://github.com/JennerFran) · [LinkedIn](https://linkedin.com/in/francodatascience) · [Data](https://docs.google.com/spreadsheets/d/1WasZpz2HazySQA6S0owWgesaFsxqN_8OfxJHiBk59QQ/edit?gid=2018616909#gid=2018616909)")
