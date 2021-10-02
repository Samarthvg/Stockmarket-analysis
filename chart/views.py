from logging import PlaceHolder
from dash.html.Div import Div
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Create your views here.

app = dash.Dash(__name__)

app.layout = html.Center([ 

    html.H1("Stock Market Analysis", style={'text-align':'center'}),

    html.Div([
        html.H4("Ticker"),
        dcc.Dropdown(
        id='tick',
        options=[
            {'label': 'TESLA', 'value': 'TSLA'},
            {'label': 'Coca Cola', 'value': 'KO'},
            {'label': 'Tata Motors', 'value': 'TATAMOTORS.BO'},
            {'label': 'NIFTY 50', 'value': '^NSEI'},
            {'label':'Amazon','value':'AMZN'}
        ],
        placeholder='Select Ticker',
        value = '^NSEI',
        style={
            'width': '150px',
            'text-align':'left'
        }

    ),
    html.H4("Time period"),
         dcc.Dropdown(
        id='duration',
        options=[
            {'label': '2 months', 'value': '2mo'},
            {'label': '6 months', 'value': '6mo'},
            {'label': '1 year', 'value': '1y'},
            {'label': '3 years', 'value': '5y'},
            {'label': 'Max', 'value': 'max'}
        ],
        placeholder='Duration',
        value = '2mo',
        style={
            'width': '150px',
            'text-align':'left'
        }

    ),
    html.H4("Moving average 1"),
         dcc.Dropdown(
        id='MA1',
        options=[
            {'label': '10', 'value': '10'},
            {'label': '21', 'value': '21'},
            {'label': '50', 'value': '50'},
            {'label': '200', 'value': '200'}
            
        ],
        placeholder='Select window gap',
        value = '10',
        style={
            'width': '150px',
            'text-align':'left'
        }

    ),
    html.H4 ("Moving average 2"),
         dcc.Dropdown(
        id='MA2',
        options=[
            {'label': '10', 'value': '10'},
            {'label': '21', 'value': '21'},
            {'label': '50', 'value': '50'},
            {'label': '200', 'value': '200'}
            
        ],
        placeholder='Select window gap',
        value = '21',
        style={
            'width': '150px',
            'text-align':'left'
        }),
    ],style={'color':'black','vertical-align':'text-bottom','border-radius':'25px','border':'2px solid teal','padding':'10px'}

    ),
    
    html.Center(dcc.Graph(id="graph"),style={'padding':'20px'}),

    ])
   

@app.callback(
    Output("graph", "figure"), 
    [Input("duration", "value")],
    [Input("tick", "value")],
    [Input("MA1","value")],
    [Input("MA2","value")])

def graph(duration,tick,MA1,MA2):
    import pandas as pd
    import yfinance as yf
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    import plotly.express as px
    import plotly.io as pio
    pio.templates

    print(tick, duration,MA1,MA2)

    df = yf.download(tickers=tick, period=duration).reset_index()

    df['Year'] = pd.DatetimeIndex(df['Date']).year

    
    moving_average1="MA"+MA1
    moving_average2= "MA"+MA2

    df['MA1'] = df['Close'].rolling(window=int(MA1), min_periods=0).mean()
    df['MA2'] = df['Close'].rolling(window=int(MA2), min_periods=0).mean()

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.06, 
                    subplot_titles=('OHLC', 'Volume'), 
                    row_width = [0.2,0.7])
    
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], 
                             high=df['High'], 
                             low=df['Low'], 
                             close=df['Close'],
                             name= 'OHLC',
                             increasing_line_color = 'teal', decreasing_line_color = 'maroon',
                             ),
                             row = 1, col = 1
              )

    fig.add_trace(go.Scatter(x=df.index,y= df['MA1'], marker_color = 'pink', name=moving_average1), row=1 ,col=1)
    fig.add_trace(go.Scatter(x=df.index,y= df['MA2'], marker_color = 'purple', name=moving_average2), row=1 ,col=1)

    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color = 'orange', showlegend = False), row=2, col=1)

    fig.update_layout(
       
        font_family='Courier New',
        xaxis_tickfont_size = 12,
        yaxis = dict(
            title = 'Price',
            title_font_size =14,
            tickfont_size=12,
            ),
        autosize=False,
        width = 1000,
        template = 'plotly_dark',
        height = 600,
        margin= dict(l=50,r=50,b=100,t=50,pad=5)
    )

    fig.update(layout_xaxis_rangeslider_visible=False)

    return fig

app.run_server(debug=True)