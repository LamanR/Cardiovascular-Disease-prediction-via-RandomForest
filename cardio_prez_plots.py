#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 17:21:15 2023

@author: lamanr
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv('/Users/lamanr/RDS102/cardio_train.csv', delimiter=(';'))

# Set the figure size and style
plt.figure(figsize=(12, 10))
sns.set(style="whitegrid", font_scale=1.2)

# Calculate 'years' from 'age' column

# Create the count plot
sns.countplot(x='age', hue='cardio', data=df)

# Customize the plot
plt.title('Cardiovascular Disease Counts by Age', fontsize=16)
plt.xlabel('Age (Years)', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.legend(title='Cardio', loc='upper right', labels=['No Cardio', 'Cardio'])
plt.xticks(rotation=90)
plt.tight_layout()

# Show the plot
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Select numerical columns (excluding binary variables)
numerical_columns = ['ap_hi', 'ap_lo']

# Set the figure size and style
plt.figure(figsize=(16, 10))
sns.set(style="whitegrid", font_scale=1.2)

# Plot histograms for numerical features
for i, column in enumerate(numerical_columns, 1):
    plt.subplot(2, 3, i)
    sns.histplot(df[column], bins=30, kde=False, color='skyblue', edgecolor='black')
    plt.title(f'Distribution of {column}', fontsize=14)
    plt.xlabel(column, fontsize=12)
    plt.ylabel('Count', fontsize=12)

plt.tight_layout()
plt.show()



from IPython.display import display

# Assuming you have already defined the DataFrame 'df'
numerical_columns = ['height', 'weight', 'ap_hi', 'ap_lo']

# Display the descriptive statistics as a table
desc_stats = df[numerical_columns].describe()

# Set the figure size
plt.figure(figsize=(12, 6))

# Plot the bar plot
sns.barplot(x=desc_stats.index, y='mean', data=desc_stats, color='skyblue', edgecolor='black')
plt.errorbar(x=desc_stats.index, y='mean', yerr='std', data=desc_stats, fmt='none', capsize=5, color='black')

# Customize the plot
plt.title('Descriptive Statistics for Numerical Features', fontsize=16)
plt.xlabel('Feature', fontsize=14)
plt.ylabel('Mean', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.tight_layout()
plt.show()

# Boxplot for numerical features to identify outliers
df.drop(df[(df['height'] > df['height'].quantile(0.975)) | (df['height'] < df['height'].quantile(0.025))].index,inplace=True)
df.drop(df[(df['weight'] > df['weight'].quantile(0.975)) | (df['weight'] < df['weight'].quantile(0.025))].index,inplace=True)
df.drop(df[(df['ap_hi'] > df['ap_hi'].quantile(0.975)) | (df['ap_hi'] < df['ap_hi'].quantile(0.025))].index,inplace=True)
df.drop(df[(df['ap_lo'] > df['ap_lo'].quantile(0.975)) | (df['ap_lo'] < df['ap_lo'].quantile(0.025))].index,inplace=True)


from tabulate import tabulate

# Assuming you have already defined the DataFrame 'df'

# Calculate 'years' from 'age' column

# Calculate the descriptive statistics
# Print the descriptive statistics as a table
print(tabulate(desc_stats, headers='keys', tablefmt='pretty'))





import seaborn as sns
import matplotlib.pyplot as plt

# Assuming you have already defined the DataFrame 'df'

# Categorical columns to visualize
categorical_columns = ['gender', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'cardio']

# Set the figure size
plt.figure(figsize=(18, 10))

# Create count plots for each categorical variable
for i, column in enumerate(categorical_columns, 1):
    plt.subplot(3, 3, i)
    sns.countplot(x=column, data=df)
    plt.title(f'Distribution of {column}', fontsize=14)
    plt.xlabel(column, fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# Set the figure size

plt.figure(figsize=(18, 10))

# Create box plots for each numerical variable
for i, column in enumerate(numerical_columns, 1):
    plt.subplot(2, 3, i)
    sns.boxplot(x=column, data=df, palette='Set2')
    plt.title(f'Box Plot of {column}', fontsize=14)
    plt.xlabel(column, fontsize=12)
    plt.ylabel(None)

plt.tight_layout()
plt.show()



df = df[df['age'] != 30]



# Plot boxplots for numerical features grouped by 'cardio'
plt.figure(figsize=(16, 12))
for i, column in enumerate(numerical_columns, 1):
    plt.subplot(2, 3, i)
    sns.boxplot(x='cardio', y=column, data=df)
    plt.title(f"{column.capitalize()} by Cardio", fontsize=14)
    plt.xlabel('Cardio', fontsize=12)
    plt.ylabel(column.capitalize(), fontsize=12)

plt.tight_layout()
plt.show()

plt.figure(figsize=(20, 12))
for i, column in enumerate(categorical_columns, 1):
    plt.subplot(2, 3, i)
    sns.countplot(x=column, hue='cardio', data=df)
    plt.title(f"{column.capitalize()} by Cardio", fontsize=14)
    plt.xlabel(column.capitalize(), fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.legend(title='Cardio', loc='upper right')

plt.tight_layout()
plt.show()



df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)

# Calculate correlation matrix
corr_matrix = df.corr()

# Generate correlation heatmap
plt.figure(figsize=(16, 8))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", square=True)
plt.show()


# Store the 'cardio' column separately
cardio_column = df['cardio']

# Drop the 'cardio' column from the DataFrame
df.drop(columns=['cardio'], inplace=True)

# Add the 'cardio' column as the last column in the DataFrame
df['cardio'] = cardio_column