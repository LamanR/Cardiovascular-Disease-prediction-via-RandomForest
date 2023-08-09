#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 09:07:01 2023

@author: lamanr
"""

"""
Cardiovascular Disease dataset:
   predicting presence or absence of cardiovascular disease 

"""

# Importing necessary libraries
import pandas as pd
from mysql_connection import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data into a DataFrame
df=pd.read_csv('/Users/lamanr/Downloads/cardio_train.csv', delimiter=(';'))

"""
1. Dataset transfer onto and fetching from Mysql

"""

# Credentials of server
host='127.0.0.1'
user='root'
password='L.mysql42'
db='classicmodels'

# Queries to execute
queries = { 'table': 
           """CREATE TABLE IF NOT EXISTS cardio 
           (id INT, age INT, gender INT, height INT, weight FLOAT, ap_hi INT, ap_lo INT, 
            cholesterol INT, gluc INT, smoke INT, alco INT, active INT, cardio INT)""", 
            'insert': 
            "INSERT INTO cardio VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            'upload': "SELECT * FROM cardio;"
}
    
# Connecting to Mysql database
reConnect(user, password, host, db)

# Creating table
dbExecute(queries['table'])

# Inserting rows to created table
for row in df.itertuples(index=False):
    
    dbInsert(queries['insert'],row)

print("Data transfer completed successfully.")

# Fetching 
result, columns = dbSelect(queries['upload'])

# Convert the result to a df
df = pd.DataFrame(result, columns=columns)


"""
2. EDA and manipulation

"""

# Describe data
print(df.head())
print(df.info())
print(df.describe(include = 'all'))

# Distribution of numerical features
numerical_features = ['age_years', 'bmi', 'height', 'weight', 'ap_hi', 'ap_lo']
df[numerical_features].hist(figsize=(10, 8))
plt.tight_layout()
plt.show()

# Categorical features
categorical_features = ['gender', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'cardio']
for feature in categorical_features:
    plt.figure(figsize=(12, 8))
    sns.countplot(data=df, x=feature)
    plt.show()
    
# From value counts of cardio column we can say that we have balanced data

# Our target is cardio,so let's look at its relation to other features

# Age
sns.countplot(x='age_years', hue='cardio', data=df)

plt.title('Cardiovascular Disease Counts by Age', fontsize=16)
plt.xlabel('Age (Years)', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.legend(title='Cardio', loc='upper right', labels=['No Cardio', 'Cardio'])
plt.xticks(rotation=90)
plt.tight_layout()

plt.show()

# Categorigal
sns.catplot(x="variable", hue="value", col="cardio",
            data=pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active']),
            kind="count")
plt.show()

# Gender
plt.figure(figsize=(6, 4))
sns.countplot(x="gender", hue="cardio", data=df)
plt.show()

# Dealing with outliers:
    
# Boxplot for numerical features to identify outliers
for feature in numerical_features:
    plt.figure(figsize=(10, 8))
    sns.boxplot(data=df[feature])
    plt.show()
   
# Aim values that are at the extreme ends of the data distribution, 
# since our data is overall clean dataset

df.drop(df[(df['height'] > df['height'].quantile(0.975)) | (df['height'] < df['height'].quantile(0.025))].index,inplace=True)
df.drop(df[(df['weight'] > df['weight'].quantile(0.975)) | (df['weight'] < df['weight'].quantile(0.025))].index,inplace=True)
df.drop(df[(df['ap_hi'] > df['ap_hi'].quantile(0.975)) | (df['ap_hi'] < df['ap_hi'].quantile(0.025))].index,inplace=True)
df.drop(df[(df['ap_lo'] > df['ap_lo'].quantile(0.975)) | (df['ap_lo'] < df['ap_lo'].quantile(0.025))].index,inplace=True)

# Calculate correlation matrix
corr_matrix = df.corr()

# Generate correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", square=True)
plt.show()

# Define age groups based on predefined age bins
age_bins = [29, 40, 60, np.inf]
age_labels = ['Young', 'Middle-aged', 'Senior']
df['age_group'] = pd.cut(df['age_years'], bins=age_bins, labels=age_labels)

# Calculate the difference between systolic and diastolic blood pressure
df['bp_difference'] = df['ap_hi'] - df['ap_lo']
# Create a new feature representing the square of BMI
df['bmi_squared'] = df['bmi'] ** 2

# Create an interaction term between age_years and cholesterol
df['age_cholesterol_interaction'] = df['age_years'] * df['cholesterol']

# Create an interaction term between weight and height
df['weight_height_interaction'] = df['weight'] * df['height']

# Define weight status categories based on BMI thresholds
weight_status_bins = [0, 18.5, 24.9, 29.9, np.inf]
weight_status_labels = ['Underweight', 'Normal', 'Overweight', 'Obese']
df['weight_status'] = pd.cut(df['bmi'], bins=weight_status_bins, labels=weight_status_labels)


# Define blood pressure categories based on predefined thresholds
blood_pressure_bins = [0, 89, 119, 139, np.inf]
blood_pressure_labels = ['Low', 'Normal', 'Elevated', 'High']
df['bp_category'] = pd.cut(df['ap_hi'], bins=blood_pressure_bins, labels=blood_pressure_labels)

# Create an interaction term between alcohol and smoking
df['alco_smoke_interaction'] = df['alco'] + df['smoke']

# Create an interaction term between physical activity and other features
df['activity_interaction'] = df['active'] * (df['cholesterol'] + df['gluc'] + df['smoke'] + df['alco'])


# Convert categorical variables to dummy variables
df_with_dummies = pd.get_dummies(df, columns=['age_group', 'weight_status', 'bp_category'])

# Calculate the correlation between the dummy variables and 'cardio'
correlation_with_cardio = df_with_dummies.corr()['cardio'].drop('cardio')

# Display correlation values with 'cardio'
print(correlation_with_cardio)


# Write DataFrame to CSV file
df.to_csv('cardio_output.csv', index=False)
