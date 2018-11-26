import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import os
import plotly.offline as pyo


app = dash.Dash()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
EXPENSE_FILE = '{}/../data/city-expenses-2005-2017.csv'.format(APP_ROOT)
REVENUE_FILE = '{}/../data/city-revenues-2005-2017.csv'.format(APP_ROOT)

e_df = pd.read_csv(EXPENSE_FILE, delimiter=';')
r_df = pd.read_csv(REVENUE_FILE, delimiter=';')

expense_df = e_df[e_df['level'] == 1]
revenue_df = r_df[r_df['level'] == 1]

fig = {
    "data": [
        {
            "values": expense_df['2017'],
            "labels": expense_df['level1'].str.replace(' Total', ''),
            "textposition":"inside",
            "domain": {"x": [0, .48]},
            "name": "Expense",
            "hoverinfo":"label+percent+name",
            "hole": .4,
            "type": "pie"
        },
        {
            "values": revenue_df['2017'],
            "labels": revenue_df['level1'].str.replace(' Total', ''),
            "text":["CO2"],
            "textposition":"inside",
            "domain": {"x": [.52, 1]},
            "name": "Revenue",
            "hoverinfo":"label+percent+name",
            "hole": .4,
            "type": "pie"
        }
    ],
    "layout": {
        "title": "Expense VS Revenue 2017",
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
pyo.plot(fig, filename='pie.html')
