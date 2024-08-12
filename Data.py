# Importing the libraries
from typing import List
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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
    def min(self, column) -> float:
        return self.min_data.iloc[column]
    
    def max(self, column) -> float:
        return self.max_data.iloc[column]

    # Central Measure
    def mean(self, column) -> float:
        return self.mean_data.iloc[column]

    def mode(self, column) -> float:
        return self.dataset.iloc[:, column].mode()[0]

    def median(self, column) -> float:
        return self.median_data.iloc[column]
    
    # Dispersion Measure
    def range(self, column) -> float:
        return self.max_data.iloc[column] - self.min_data.iloc[column]
    
    def std(self, column) -> float:
        return self.std_data.iloc[column]

    def var(self, column) -> float:
        return self.var_data.iloc[column]
    
    # Quartile
    def quantile(self, column, qt) -> float:
        return np.quantile(self.dataset.iloc[:, column], qt)
    
    # Single Variable vs. Result
    def scatter_plot(self, columns: List[int], title: str = '', xlabel: str = '', ylabel: str = '', colors: List[str] = ['red']*99) -> None:
        if len(columns) > len(colors):
            raise IndexError("Column and color length must be equal.")   
        
        for i in range(len(columns)):
            if columns[i] >= len(self.X[0]):                                            # check if column listed in columns is an indpendent variable column        
                raise IndexError("Column does not have independent variables.")
            elif columns[i] < 0:                                                        # check if column exists
                raise IndexError("Column does not exist.")
            plt.scatter(self.dataset.iloc[:, columns[i]], self.Y, color=colors[i])

        plt.title(title)    
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()
    
    def line_chart(self, columns: List[int], title: str = '', xlabel: str = '', ylabel: str = '', colors: List[str] = ['red']*99) -> None:
        if len(columns) > len(colors):
            raise IndexError("Column and color length must be equal.")

        for i in range(len(columns)):
            if columns[i] >= len(self.X[0]):
                raise IndexError("Column does not have independent variables.")
            elif columns[i] < 0:
                raise IndexError("Column does not exist.")
            plt.plot(self.dataset.iloc[:, columns[i]], self.Y, color=colors[i])

        plt.title(title)    
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    def bar(self) -> None:
        pass

    def hist(self) -> None:
        pass

    def box_plot(self, column, title: str = '', xlabel: str = '', ylabel: str = '') -> None:
        if column < 0 or column >= len(self.dataset):
            raise IndexError("Column does not exist.")
        
        plt.boxplot(self.dataset.iloc[:, column])
        plt.title(title)    
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

test = Data('50_Startups.csv')

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

test.scatter_plot(columns=[0, 1, 2], colors=['red', 'blue', 'green'])
test.line_chart(columns=[0, 1, 2], colors=['red', 'blue', 'green'])
test.box_plot(column=0)
