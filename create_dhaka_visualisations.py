import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime, timedelta 
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import calendar

def time_resample(dataframe, time_period):
    '''
    Resamples the dataframe over the given period of time. 
    For example, if values averaged over a day required then arguments would be df and "D"
    
    >> time_period: 'D' = days, 'M' = month, 'Y' = year

    Returns dataframe object
    '''
    resampled_df = pd.DataFrame()
    resampled_df['AQImean'] = dataframe.AQI.resample(time_period).mean()
    resampled_df['AQImed'] = dataframe.AQI.resample(time_period).median()
    resampled_df['AQImin'] = dataframe.AQI.resample(time_period).min()
    resampled_df['AQImax'] = dataframe.AQI.resample(time_period).max()
    resampled_df['AQIstd'] = dataframe.AQI.resample(time_period).std()
    resampled_df['Month'] = dataframe.Month.resample(time_period).first()
    resampled_df['Year'] = dataframe.Year.resample(time_period).first()
    resampled_df['Day'] = dataframe.Day.resample(time_period).first()
    #  To ensure statistical significance want to omit values when a significant fraction of the
    #  expected number of measurements in the given time period are missing. 
    #  For example, days when only 5 hours in 24 have measurement data available.
    #  Lets exclude data where half the expected measurements missing:
    resampled_df['Measurements'] = dataframe.AQI.resample(time_period).count()
    resampled_df = resampled_df[resampled_df['Measurements']>resampled_df['Measurements'].max()/2]
    return resampled_df



current_year = datetime.today().year

datafile = Path.cwd().joinpath('data', 
                                  'silver', 
                                  'us_embassy', 
                                  'collated_dhaka_air_data.csv')

df = pd.read_csv(datafile, parse_dates=['Date (LT)'], index_col='Date (LT)')

df_dayavg = time_resample(df, 'D')
df_monthavg = time_resample(df, 'M')

df_dayavg.AQImean.plot(kind='hist', bins=range(0,400,20))
plt.title('Distribution of Daily Average AQI', fontsize=15)

df_monthavg.AQImean.plot(kind='hist', bins=range(0,400,20))
plt.title('Distribution of Monthly Average AQI', fontsize=15)


#%% Scatter & line plot with custom background

fig, ax = plt.subplots(figsize=(24,12))
trans = 0.5

xpoints = [datetime.strptime('2015-01-01', "%Y-%m-%d"), 
           datetime.today()+timedelta(days=15)]

plt.fill_between(x = xpoints, y1 = 0, y2 = 50 , 
                 color = 'green', alpha = trans, hatch = 'x')
plt.fill_between(x = xpoints, y1 = 50, y2 = 100 , 
                 color = 'yellow', alpha = trans, hatch = '+')
plt.fill_between(x = xpoints, y1 = 100, y2 = 150 , 
                 color = 'orange', alpha = trans, hatch = '.')
plt.fill_between(x = xpoints, y1 = 150, y2 = 200 , 
                 color = 'red', alpha = trans, hatch = '\\')
plt.fill_between(x = xpoints, y1 = 200, y2 = 300 , 
                 color = 'purple', alpha = trans, hatch = '..')
plt.fill_between(x = xpoints, y1 = 300, y2 = 500 , 
                 color = 'maroon', alpha = trans, hatch = '/')

ax=sns.scatterplot(x=df_dayavg.index, 
                   y='AQImean', 
                   data=df_dayavg, 
                   color='k', 
                   s=155, 
                   marker='d')

sns.lineplot(x=df_monthavg.index,  
             y='AQImean', 
             data = df_monthavg, 
             color = 'k', 
             lw = 8)

textsize = 35
years = [*range(2016, current_year+1)]
axis_positions = [0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
for xpos, year in zip(axis_positions, years):
    plt.figtext(xpos, 0.01, year, ha = 'center', fontsize = textsize)
    
quality_categories = ['Good', 
                      'Moderate', 
                      'Caution', 
                      'Unhealthy', 
                      'Very\nUnhealthy', 
                      'Extremely\nUnhealthy'
                      ]
y_positions = [25, 75, 125, 175, 250, 350]
textstartdate = datetime.strptime('2015-07-01', "%Y-%m-%d")
for y_pos, category in zip(y_positions, quality_categories):
    plt.text(textstartdate, y_pos, category, va = 'center', fontsize = 25)
    
from dateutil.relativedelta import relativedelta


three_month_interval_dates_list = [datetime.strptime('2016-03', "%Y-%m")+
                             n*relativedelta(months=+3) for n in range(0,24)]

plt.xticks(three_month_interval_dates_list, rotation = 45, fontsize = 25)

ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.yticks(fontsize = 25)
plt.ylim(0,400)
plt.xlim(datetime.strptime('2015-06-01', "%Y-%m-%d"), 
         datetime.today()+timedelta(days=15))
plt.ylabel('AQI', fontsize =50)
plt.xlabel('')

#%% Heatmap

#  Create custom colour bar to match the standard AQI categories colour scheme
norm = mcolors.Normalize(-1,1)
aqicolors = [
    [0, 'green'], 
    [55/350, 'yellow'], 
    [75/350, 'yellow'], 
    [105/350, 'orange'], 
    [125/350, 'orange'], 
    [155/350, 'red'], 
    [175/350, 'red'],
    [205/350, 'purple'], 
    [275/350, 'purple'],
    [1, 'maroon']
            ]
aqicmap = mcolors.LinearSegmentedColormap.from_list("", aqicolors)

plt.figure(figsize=(14,8))
months = calendar.month_abbr[1:]
seasonaltable = df.pivot_table(values='AQI',
                               index='Month',
                               columns='Hour')
sns.heatmap(seasonaltable, 
            cmap=aqicmap,linecolor='white',
            linewidths=1, 
            yticklabels = months, 
            vmin = 0, 
            vmax = 350, 
            annot = True, 
            fmt = '.0f')
plt.ylabel('')
plt.xlabel('Time of Day', fontsize=27)
plt.yticks(rotation=0, fontsize=15)
plt.xticks(fontsize=15)
plt.figtext(0.76, 0.03,'AQI', fontsize=30)
#plt.savefig('../report/Heatmap_AQIcols.png', bbox_inches='tight')
plt.show()


#%% Boxplots
df['Weekday'] = df.index.day_name()

time_period_list = ['Weekday',
                    'Hour',
                    'Year', 
                    'Month']    

for time_period in time_period_list:
    
    fig, axes = plt.subplots(1, 1, figsize=(10, 6))
    sns.boxplot(data=df, x=time_period, y='AQI')
    plt.ylim(0,350)

# In[28]:


fig, axes = plt.subplots(1, 1, figsize=(12, 8))
df.AQI.plot(color='0.9', ax=axes)
rolling = df.AQI.rolling('30D')
q10 = rolling.quantile(0.1).to_frame('q10')
q90 = rolling.quantile(0.9).to_frame('q90')
median = rolling.median().to_frame('median')
pd.concat([q10, median, q90], axis=1).plot(ax=axes)