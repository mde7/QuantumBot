import datetime as dt
import pickle

import numpy as np
from utils.graph_utils import get_price_data
from sklearn.preprocessing import MinMaxScaler

with open("utils/model_pkl", "rb") as f:
    eth_model = pickle.load(f)


async def model_predict():
    a = await get_price_data("ETHGBP", "1d", 30)

    scaler = MinMaxScaler(feature_range=(0, 1))
    X_scaled = scaler.fit_transform(np.array(a[4]).reshape(-1, 1))
    X = X_scaled.reshape(1, -1)

    y = eth_model.predict(X)
    y_scaled = scaler.inverse_transform(y.reshape(1, -1))
    y_final = round(float(y_scaled), 2)

    date = dt.date.today() + dt.timedelta(days=1)
    date_final = date.strftime("%d/%m/%Y")
    return date_final, y_final
