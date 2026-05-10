import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_expense(df):

    df['month'] = pd.to_datetime(df['date']).dt.month

    monthly = df.groupby('month')['amount'].sum().reset_index()

    if len(monthly) < 2:
        return 0

    X = monthly[['month']]
    y = monthly['amount']

    model = LinearRegression()
    model.fit(X, y)

    next_month = np.array([[monthly['month'].max() + 1]])
    return model.predict(next_month)[0]