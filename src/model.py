#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 14:07:37 2020

@author: tim
"""

import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
from pathlib import Path
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import pmdarima as pm
#%%
datafile = Path.cwd().parent.joinpath('data', 'processed',
                               'USembassy_dhakadata_clean.csv')

df_raw = pd.read_csv(datafile, index_col='Date (LT)', parse_dates=['Date (LT)'])

df_dayAQI = df_raw.resample('D').mean().AQI.dropna()

df_deseasoned = df_dayAQI - df_dayAQI.rolling('30D').mean().dropna()
df_stationary = df_deseasoned.diff().dropna()
#%%

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 14))
df = df_dayAQI.diff().dropna().diff().dropna()
#df = df_deseasoned
plot_acf(df, zero=False, ax=ax1, lags=1400)
plot_pacf(df, zero=False, ax=ax2, lags=1400)

#%%
tmp = []
for p in range(10):
    for q in range(10):
        try:
            model = SARIMAX(df_stationary, order=(p,1,q), seasonal_order=(1,1,1,365))
            results = model.fit()
            tmp.append([p , q, results.aic, results.bic])
        except:
            tmp.append([p,q, None, None])
#%%

model = SARIMAX(df_stationary, order=(2,1,9))
results = model.fit()


forecast = results.get_prediction(start=-360)
#forecast = results.get_forecast(steps=30)

mean_fc = forecast.predicted_mean

con_in = forecast.conf_int()
#%%

fig, ax = plt.subplots(1, 1, figsize=(14, 8))
plt.plot(df_stationary['2020':].index, df_stationary['2020':])
plt.plot(mean_fc.index, mean_fc, c='r')
plt.fill_between(con_in.index, con_in['lower AQI'], con_in['upper AQI'],
                 color='pink')

plt.show()
#%%
from numpy import cumsum
orig = cumsum(df_stationary)+df_dayAQI.rolling('30D').mean()
predorig = cumsum(mean_fc)+df_dayAQI.rolling('30D').mean()


fig, ax = plt.subplots(1, 1, figsize=(14, 8))
df_dayAQI.plot(ax=ax)
orig.plot(ax=ax)
predorig.plot(ax=ax)
df_dayAQI.rolling('30D').mean().plot()
plt.show()
