# Importing the libraries
import numpy as np
import pandas as pd

class Data():
    # Initizliaing input and output values of dataset
    def __init__(self, csv_file: str):                                   
        self.dataset = pd.read_csv(csv_file)
        self.X = self.dataset.iloc[:, :-1].values
        self.Y = self.dataset.iloc[:, -1].values

        # Basic Measure
        self.max_data = self.dataset.max()
        self.min_data = self.dataset.min()

        # Central Measure
        self.mean_data = self.dataset.mean()
        self.median_data = self.dataset.median()

        # Dispersion Measure
        self.std_data = self.dataset.std()
        self.var_data = self.dataset.var()

    # Basic Measure
    def min(self, column):
        return self.min_data.iloc[column]
    
    def max(self, column):
        return self.max_data.iloc[column]

    # Central Measure
    def mean(self, column):
        return self.mean_data.iloc[column]

    def mode(self, column):
        return self.dataset.iloc[:, column].mode()[0]

    def median(self, column):
        return self.median_data.iloc[column]
    
    # Dispersion Measure
    def range(self, column):
        return self.max_data.iloc[column] - self.min_data.iloc[column]
    
    def std(self, column):
        return self.std_data.iloc[column]

    def var(self, column):
        return self.var_data.iloc[column]
    
    # Quartile
    def quantile(self, column, qt):
        return np.quantile(self.dataset.iloc[:, column:column+1], qt)

test = Data('Salary_Data.csv')

print("Basic Measure")
print("Min: " + str(test.min(0)))
print("Max: " + str(test.max(0)))
print("Mode: " + str(test.mode(0)))

print("\nCentral Measure")
print("Mean: " + str(test.mean(0)))
print("Median: " + str(test.median(0)))

print("\nDispersion Measure")
print("Range: " + str(test.range(0)))
print("Standard Deviation: " + str(test.std(0)))
print("Variance: " + str(test.var(0)))

print("\nQuartile")
print("Q1: " + str(test.quantile(0, 0.25)))
print("Q2: " + str(test.quantile(0, 0.5)))
print("Q3: " + str(test.quantile(0, 0.75)))
