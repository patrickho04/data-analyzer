from PreprocessData import PreprocessData
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

# uses ordinary least squares to find coefficient and constant
# y = b0 + b1x
def linear_regression_model(ds: PreprocessData, col: int):
    # Linear regression model
    regressor = LinearRegression()
    regressor.fit(ds.x_train[col], ds.y_train)
    y_pred = regressor.predict(ds.x_test[col])

    # Plotting line against training input
    plt.scatter(ds.x_train[col], ds.y_train, color='green')
    plt.scatter(ds.x_test, ds.y_test, color='red')
    plt.plot(ds.x_train[col], regressor.predict(ds.x_train[col]), color='blue')
    plt.title('Salary vs. Experience (Test Set)')
    plt.xlabel('Years of Experience')
    plt.ylabel('Salary')
    plt.show()


test = PreprocessData('50_Startups.csv')
test.split_train_test()
linear_regression_model(test, 0)