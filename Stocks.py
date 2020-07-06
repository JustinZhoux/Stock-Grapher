import pandas as pd
import chart_studio.plotly as py
import plotly.graph_objs as go
import datetime
from alpha_vantage.timeseries import TimeSeries
ts = TimeSeries(key='Y8GCMYVJEBS6N4DU', 
                output_format='pandas')
stock_code = input("Enter the stock ticker")
def read_stock(stock_code, interval = '1min'):
    df, _ = ts.get_intraday(symbol= stock_code,
                                    interval=interval,
                                    outputsize='full')
    
    # trim the df 
    df.rename(index= pd.to_datetime,
              columns = lambda x : x.split(' ')[-1],
              inplace = True) 
    
    return df
# 5-minutes interval
df_5min = read_stock(stock_code)
# 1-minute interval
df_1min = read_stock(stock_code, interval= '1min')
# acess current date
cur_dt = datetime.datetime.now()
# convert into string
dt_str = cur_dt.strftime('%Y-%m-%d')
# respective current date df
df_5 = df_5min[dt_str:]
df_1 = df_1min[dt_str:]
trace = go.Candlestick(x=df_5.index,
                       open=df_5.open,
                       high=df_5.high,
                       low=df_5.low,
                       close=df_5.close,
                       name = 'Candlestick')
trace_close = go.Scatter(x=list(df_1.index),
                         y=list(df_1.close),
                         name='Close',
                         line=dict(color='#87CEFA'))
trace_high = go.Scatter(x=list(df_1.index),
                        y=list(df_1.high),
                        visible = False,
                        name='High',
                        line=dict(color='#33CFA5'))
trace_low = go.Scatter(x=list(df_1.index),
                       y=list(df_1.low),
                       visible = False,
                       name='Low',
                       line=dict(color='#F06A6A'))
data = [trace, trace_high, trace_low, trace_close]
updatemenus = list([
    dict(type="buttons",
         active=99,
         x = 0.05,
         y = 0.99,
         bgcolor = '#000000',
         bordercolor = '#FFFFFF',
         font = dict( color='#FFFFFF', size=11 ),
         direction = 'left',
         xanchor = 'left',
         yanchor = 'top',
         buttons=list([
            dict(label = 'Close',
                 method = 'update',
                 args = [{'visible': [False, False, False, True]},
                         {'title': 'Minute Trading Data for '+ stock_code}]),
            dict(label = 'Candlestick',
                 method = 'update',
                 args = [{'visible': [True, False, False, False]},
                         {'title': stock_code + ' Candlestick'}]),
            dict(label = 'High',
                 method = 'update',
                 args = [{'visible': [False, True, False, False]},
                         {'title': stock_code + ' High'}]),
            dict(label = 'Low',
                 method = 'update',
                 args = [{'visible': [False, False, True, False]},
                         {'title': stock_code + ' Low'}]),
            dict(label = 'All',
                 method = 'update',
                 args = [{'visible': [False, True, True, True]},
                         {'title': stock_code}]),
            dict(label = 'Reset',
                 method = 'update',
                 args = [{'visible': [True, False, False, True]},
                         {'title': 'Minute Trading Data for ' + stock_code}])
        ]),
    )
])
layout = go.Layout(
                   title='Minute Trading Data for' + stock_code,
                   autosize = True,
                   plot_bgcolor = '#000000',
                   showlegend=False,
                   updatemenus=updatemenus
                   )
fig = dict(data=data,
           layout=layout)
py.plot(fig, filename= stock_code + 'minute_candlestick')