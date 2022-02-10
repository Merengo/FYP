import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output,State
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from datetime import datetime
import joblib



app = dash.Dash()
server = app.server


app.layout = html.Div([
   
    html.H1("Stock Price Prediction Dashboard", style={"textAlign": "center"}),
     dcc.DatePickerRange(id='my_date_picker',
                                 min_date_allowed=datetime(2015,1,1),
                                 max_date_allowed=datetime(2025,12,31),
                                 start_date_placeholder_text = 'Start date',
                                 end_date_placeholder_text = 'End date',
                                 start_date = datetime(2016,1,1),
                                 end_date = datetime.today(),
                                 display_format = 'Y-MM-DD'
                                
                                 ),
    dcc.Tabs(id="tabs", children=[
       
        dcc.Tab(label='NSE-TATAGLOBAL', id ='tab1',value='TATAGLOBAL',children=[
			html.Div([
				html.H2(" Historical Prices",style={"textAlign": "center"}),
				dcc.Graph(
					id="graph 1"
					

				),
				html.H2("Predicted Prices",style={"textAlign": "center"}),
				dcc.Graph(
					id="graph 2"
					

				)				
			])        		


        ]),
        dcc.Tab(label='NASDAQ: AAPL', id='tab2',value='AAPL',children=[
            html.Div([
				html.H2(" Historical Prices",style={"textAlign": "center"}),
				dcc.Graph(
					id="graph1"
					

				),
				html.H2("Predicted Prices",style={"textAlign": "center"}),
				dcc.Graph(
					id="graph2"
					

				)				
			])        		

        ])


    ])
])







@app.callback(Output('graph 1','figure'),
             [Input('tab1','value'),
              Input('my_date_picker','start_date'),
              Input('my_date_picker','end_date'),
              ])
def update_graph_1(value,start_date,end_date):
    df1 = pd.Series(pd.date_range(start_date,end_date))
    df1 = pd.DataFrame(df1, columns=['Date'])
    df = pd.read_csv("NSE-TATAGLOBAL11.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    filtered_df = pd.merge(df,df1,how='inner',on='Date')
    figure = go.Figure(data=[go.Candlestick(x=filtered_df['Date'],
                open=filtered_df['Open'], 
                high=filtered_df['High'],
                low=filtered_df['Low'], 
                close=filtered_df['Close'],
                    
                )
                      ],layout={'plot_bgcolor':'white','paper_bgcolor':'white'})
    figure.update_layout(title=value,xaxis_rangeslider_visible=False,hovermode='x',yaxis_title='Price in USD',xaxis_title='Period')
    return figure

@app.callback(Output('graph1','figure'),
             [Input('tab2','value'),
              Input('my_date_picker','start_date'),
              Input('my_date_picker','end_date'),
              ])
def update_graph_2(value,start_date,end_date):
    df1 = pd.Series(pd.date_range(start_date,end_date))
    df1 = pd.DataFrame(df1, columns=['Date'])
    df = pd.read_csv("AAPL.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    filtered_df = pd.merge(df,df1,how='inner',on='Date')
    figure = go.Figure(data=[go.Candlestick(x=filtered_df['Date'],
                open=filtered_df['Open'], 
                high=filtered_df['High'],
                low=filtered_df['Low'], 
                close=filtered_df['Close'],
                    
                )
                      ],layout={'plot_bgcolor':'white','paper_bgcolor':'white'})
    figure.update_layout(title=value,xaxis_rangeslider_visible=False,hovermode='x',yaxis_title='Price in USD',xaxis_title='Period')
    return figure
  


@app.callback(Output('graph 2','figure'),
             [Input('tab1','value'),
              Input('my_date_picker','start_date'),
              Input('my_date_picker','end_date'),
              ])
def View_predictions(value,start_date,end_date):
    df2 = pd.Series(pd.date_range(start_date,end_date))
    df2 = pd.DataFrame(df2, columns=['Date'])
    df2["weekday"] = df2["Date"].dt.weekday
    df2["dayofyear"] = df2["Date"].dt.dayofyear
    df2["year"] = df2["Date"].dt.year
    df2["month"] = df2["Date"].dt.month
    df2["dayofmonth"] = df2["Date"].dt.day
    y_pred = model1.predict(df2[['year', 'month', 'dayofmonth', 'weekday',
    'dayofyear']])
    Predicted = pd.DataFrame(y_pred,columns = ['Close','Open','High','Low'])
    Final = pd.concat([df2,Predicted],axis = 1)
    figure = go.Figure(data=[go.Scatter(x=Final['Date'],
                                        y=Final['Close'],
                                        mode='lines', opacity=0.7,
                                                                          
                
                   )
                      ],layout={'plot_bgcolor':'white','paper_bgcolor':'white'})
    figure.update_layout(title=value,xaxis_rangeslider_visible=False,hovermode='x',yaxis_title='Price in USD',xaxis_title='Period')
    return figure 


@app.callback(Output('graph2','figure'),
             [Input('tab2','value'),
              Input('my_date_picker','start_date'),
              Input('my_date_picker','end_date'),
              ])

def View_predictions(value,start_date,end_date):
    df2 = pd.Series(pd.date_range(start_date,end_date))
    df2 = pd.DataFrame(df2, columns=['Date'])
    df2["weekday"] = df2["Date"].dt.weekday
    df2["dayofyear"] = df2["Date"].dt.dayofyear
    df2["year"] = df2["Date"].dt.year
    df2["month"] = df2["Date"].dt.month
    df2["dayofmonth"] = df2["Date"].dt.day
    y_pred = model2.predict(df2[['year', 'month', 'dayofmonth', 'weekday',
    'dayofyear']])
    Predicted = pd.DataFrame(y_pred,columns = ['Close','Open','High','Low'])
    Final = pd.concat([df2,Predicted],axis = 1)
    figure = go.Figure(data=[go.Scatter(x=Final['Date'],
                                        y=Final['Close'],
                                        mode='lines', opacity=0.7,
                                                                          
                
                   )
                      ],layout={'plot_bgcolor':'white','paper_bgcolor':'white'})
    figure.update_layout(title=value,xaxis_rangeslider_visible=False,hovermode='x',yaxis_title='Price in USD',xaxis_title='Period')
    return figure       
    

if __name__ == '__main__':
    with open('model1.joblib','rb') as model1_file:
        model1 = joblib.load(model1_file)
    with open('model2.joblib','rb') as model2_file:
        model2 = joblib.load(model2_file)
    app.run_server()