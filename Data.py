# Importing the libraries
import numpy as np
import pandas as pd

class Data():
    # Initizliaing input and output values of dataset
    def __init__(self, csv_file: str):                                   
        self.dataset = pd.read_csv(csv_file)
        self.X = self.dataset.iloc[:, :-1].values
        self.Y = self.dataset.iloc[:, -1].values

        # Descriptive statistics
        self.max_data = self.dataset.max()
        self.min_data = self.dataset.min()
        self.mean_data = self.dataset.mean()
        self.median_data = self.dataset.median()
    
    def mean(self, column):
        return self.mean_data.iloc[column]

    def range(self, column):
        return self.max_data.iloc[column] - self.min_data.iloc[column]

    def mode(self, column):
        pass

    def median(self, column):
        return self.median_data.iloc[column]
