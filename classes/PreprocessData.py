from Data import Data
import numpy as np
from sklearn.impute import SimpleImputer

# Preprocessing tools for machine learning
class PreprocessData(Data):
    def __init__(self, csv_file):
        super().__init__(csv_file=csv_file)

    def replace_missing_data(self, lower:int, upper:int) -> None:
        imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
        imputer.fit(self.X[:, lower:upper])
        self.X = imputer.transform(self.X[:, lower:upper])
