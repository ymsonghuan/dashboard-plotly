import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import os
import plotly.offline as pyo

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
EXPENSE_FILE = '{}/../data/city-expenses-2005-2017.csv'.format(APP_ROOT)
REVENUE_FILE = '{}/../data/city-revenues-2005-2017.csv'.format(APP_ROOT)
years = [str(x) for x in reversed(range(2008, 2018))]

e_df = pd.read_csv(EXPENSE_FILE, delimiter=';')
r_df = pd.read_csv(REVENUE_FILE, delimiter=';')

app = dash.Dash()

expense_df = e_df[e_df['level'] == 1]
revenue_df = r_df[r_df['level'] == 1]


app.layout = html.Div(children=[
    html.Span("Durham County budget"),
    html.H1('durham city expenses!'),
    html.Div('Sams dashbord'),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='exp-vs-rev-year',
                options=[{'label': year, 'value': year} for year in years],
                value='2017',
                clearable=False
            )
        ],
            style={'width': '48%', 'display': 'inline-block'})
    ]),
    dcc.Graph(id='exp-vs-rev-pie-chart')
], style={'padding': 10})


@app.callback(Output('exp-vs-rev-pie-chart', 'figure'),
              [Input('exp-vs-rev-year', 'value')])
def update_pie_chart(fiscal_year):
    return {
        "data": [
            {
                "values": expense_df[fiscal_year],
                "labels": expense_df['level1'].str.replace(' Total', ''),
                "textposition":"inside",
                "domain": {"x": [0, 0.48]},
                "name": "Expense",
                "hoverinfo":"label+percent+name",
                "hole": .4,
                "type": "pie"
            },
            {
                "values": revenue_df[fiscal_year],
                "labels": revenue_df['level1'].str.replace(' Total', ''),
                "text":["CO2"],
                "textposition":"inside",
                "domain": {"x": [0.52, 1]},
                "name": "Revenue",
                "hoverinfo":"label+percent+name",
                "hole": .4,
                "type": "pie"
            }
        ],
        "layout": {
            "title": "Expense VS Revenue {}".format(fiscal_year),
            "annotations": [
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "Expense",
                    "x": 0.21,
                    "y": 0.5
                },
                {
                    "font": {
                        "size": 20
                    },
                    "showarrow": False,
                    "text": "Revenue",
                    "x": 0.79,
                    "y": 0.5
                }
            ]
        }
    }


if __name__ == '__main__':
    app.run_server()
