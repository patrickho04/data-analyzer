# Importing the libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List

class Data():
    # Initizliaing input and output values of dataset
    def __init__(self, csv_file: str):                                   
        self.dataset = pd.read_csv(csv_file)
        self.X = self.dataset.iloc[:, :-1].values
        self.Y = self.dataset.iloc[:, -1].values

        # Basic Measure
        self.max_data = self.dataset.max()
        self.min_data = self.dataset.min()

    # Basic Measure
    def min(self, column) -> float:
        return self.min_data.iloc[column]
    
    def max(self, column) -> float:
        return self.max_data.iloc[column]

    # Central Measure
    def mean(self, column) -> float:
        return self.dataset.mean().iloc[column]

    def mode(self, column) -> float:
        return self.dataset.iloc[:, column].mode()[0]

    def median(self, column) -> float:
        return self.dataset.median().iloc[column]
    
    # Dispersion Measure
    def range(self, column) -> float:
        return self.max_data.iloc[column] - self.min_data.iloc[column]
    
    def std(self, column) -> float:
        return self.dataset.std().iloc[column]

    def var(self, column) -> float:
        return self.dataset.var().iloc[column]
    
    # Quartile
    def quantile(self, column, qt) -> float:
        return np.quantile(self.dataset.iloc[:, column], qt)
    
    def iqr(self, column) -> float:
        return self.quantile(column, 0.75) - self.quantile(column, 0.25)
    
    # Single Variable vs. Result
    def scatter_plot(self, columns: List[int], xlabel: str = '', colors: List[str] = ['red']*99) -> None:
        # Fill color list if it doesn't match amount of columns
        if len(columns) > len(colors):
            dif = len(columns) - len(colors)
            fill = ['red'] * dif
            colors = colors + fill
        
        for i in range(len(columns)):
            # Check if column listed in columns is an indpendent variable column    
            if columns[i] >= len(self.X[0]):    
                raise IndexError("Column does not have independent variables.")
            elif columns[i] < 0:
                raise IndexError("Column does not exist.")
            plt.scatter(self.dataset.iloc[:, columns[i]], self.Y, color=colors[i])

        plt.xlabel(xlabel)
        plt.ylabel(self.dataset.columns[-1])
        plt.show()
    
    def line_chart(self, columns: List[int], xlabel: str = '', colors: List[str] = ['red']*99) -> None:
        # Fill color list if it doesn't match amount of columns
        if len(columns) > len(colors):
            dif = len(columns) - len(colors)
            fill = ['red'] * dif
            colors = colors + fill

        for i in range(len(columns)):
            if columns[i] >= len(self.X[0]):
                raise IndexError("Column does not have independent variables.")
            elif columns[i] < 0:
                raise IndexError("Column does not exist.")
            plt.plot(self.dataset.iloc[:, columns[i]], self.Y, color=colors[i])

        plt.xlabel(xlabel)
        plt.ylabel(self.dataset.columns[-1])
        plt.show()

    def bar(self) -> None:
        pass

    def hist(self) -> None:
        pass

    def box_plot(self, column, xlabel: str = '') -> None:
        if column < 0 or column >= len(self.dataset):
            raise IndexError("Column does not exist.")
        
        plt.boxplot(self.dataset.iloc[:, column])
        plt.xlabel(xlabel)
        plt.ylabel(self.dataset.columns[-1])
        plt.show()
