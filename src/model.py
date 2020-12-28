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

#%%
df2018=pd.read_csv('../data/raw/Dhaka_PM2.5_2018_YTD.csv', parse_dates=['Date (LT)'], index_col='Date (LT)')
df2018.AQI.replace({-999:np.nan}, inplace=True)
avg2018 = df2018.resample('M').mean().interpolate().resample('D').mean().interpolate().AQI
std2018 = df2018.resample('M').std().interpolate().resample('D').mean().interpolate().AQI
missing = pd.concat([avg2018['07/2018':'11/2018'], std2018['07/2018':'11/2018']], axis=1)
missing.columns = ['AQI_mean', 'AQI_std']
missing['noise'] = missing['AQI_std'].apply(lambda x: float(np.random.normal(0, x, 1)))
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
df_raw.AQI.plot(ax=ax)
missing['AQI_sim'] = missing['AQI_mean'].add(missing['noise'])
missing.AQI_sim.plot(ax=ax, color='r')
#%%
fig, ax = plt.subplots(1, 1, figsize=(12, 8))


df_dayAQI = df_raw.resample('D').mean().AQI.dropna()
df = df_dayAQI.append(missing['08/17/2018':'11/2/2018'].AQI_sim)
df = df.resample('D').mean()
df.plot(ax=ax)
#%%

#pm.auto_arima(y, fit_args)
df_acf = df.diff(365).diff().dropna()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 14))
plot_acf(df_acf, zero=False, ax=ax1, lags=20)
plot_pacf(df_acf, zero=False, ax=ax2, lags=20)
ax2.set_ylim(-0.5,0.5)
# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 14))
# plot_acf(df_acf, zero=False, ax=ax1, lags=[365, 730, 1095])
# plot_pacf(df_acf, zero=False, ax=ax2, lags=[365, 730, 1095])
#%%

results = pm.auto_arima(df_acf, d=1, start_p=1, max_p=5, start_q=0, max_q=12,
                        seasonal=True, m=365, D=1, start_P=0, max_P=0, 
                        start_Q=0, max_Q=4, information_criterion='aic', 
                        trace=True, error_action='ignore', stepwise=True)


#%%
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 14))
df = df_dayAQI.diff(365).dropna()#.diff().dropna()
#df = df_deseasoned
plot_acf(df, zero=False, ax=ax1, lags=400)
plot_pacf(df, zero=False, ax=ax2, lags=400)

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
