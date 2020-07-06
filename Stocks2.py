import pandas as pd
import sys
import chart_studio.plotly as py
import plotly.graph_objs as go
import datetime
from alpha_vantage.timeseries import TimeSeries
ts = TimeSeries(key='Y8GCMYVJEBS6N4DU', 
                output_format='pandas')
def read_stock(stock_code, interval = '1min'):
    df, _ = ts.get_intraday(symbol= stock_code,
                                    interval=interval,
                                    outputsize='full')
    
    # trim the df 
    df.rename(index= pd.to_datetime,
              columns = lambda x : x.split(' ')[-1],
              inplace = True) 
    
    return df
def draw(stock_code):
  df_5min = read_stock(stock_code)
  df_1min = read_stock(stock_code, interval= '1min')
  cur_dt = datetime.datetime.now()
  dt_str = cur_dt.strftime('%Y-%m-%d')
  df_5 = df_5min[dt_str:]
  df_1 = df_1min[dt_str:]
  stock = go.Candlestick(x=df_5.index,
                         open=df_5.open,
                         high=df_5.high,
                         low=df_5.low,
                         close=df_5.close,
                         name = 'Candlestick')
  stock_close = go.Scatter(x=list(df_1.index),
                           y=list(df_1.close),
                           name='Close',
                           line=dict(color='#D3D3D3'))
  stock_high = go.Scatter(x=list(df_1.index),
                          y=list(df_1.high),
                          visible = False,
                          name='High',
                          line=dict(color='#7CFC00'))
  stock_low = go.Scatter(x=list(df_1.index),
                         y=list(df_1.low),
                         visible = False,
                         name='Low',
                         line=dict(color='#FF0000'))
  data = [stock, stock_high, stock_low, stock_close]
  updatemenus = list([
      dict(type="buttons",
           x = 0.05,
           y = 0.95,
           bgcolor = '#000000',
           bordercolor = '#FFFFFF',
           font = dict( color='#FFFFFF', size= 10),
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
              dict(label = 'Reset',
                   method = 'update',
                   args = [{'visible': [True, False, False, True]},
                           {'title': 'Minute Interval Data for ' + stock_code}])
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



