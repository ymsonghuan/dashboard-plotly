import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
from dash.dependencies import Input, Output

app = dash.Dash()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
EXPENSE_FILE = '{}/../data/city-expenses-2005-2017.csv'.format(APP_ROOT)
REVENUE_FILE = '{}/../data/city-revenues-2005-2017.csv'.format(APP_ROOT)
years = [str(x) for x in range(2008, 2018)]
years_reverse = [str(x) for x in reversed(range(2008, 2018))]

e_df = pd.read_csv(EXPENSE_FILE, delimiter=';')
r_df = pd.read_csv(REVENUE_FILE, delimiter=';')

expense_total_df = e_df[e_df['level'] == 0][years]
revenue_total_df = r_df[r_df['level'] == 0][years]
print(expense_total_df.iloc[0])
print(revenue_total_df.iloc[0])

fig = {
    "data": [
        {
            "x": years[0:(9 + 1)],
            "y": expense_total_df.iloc[0][0:(9 + 1)],
            "name": "Expense",
            "hoverinfo":"x+y+name",
            "type": "bar"
        },
        {
            "x": years,
            "y": revenue_total_df.iloc[0],
            "textposition":"inside",
            "name": "Revenue",
            "hoverinfo":"x+y+name",
            "type": "bar"
        }
    ],
    "layout": {
        "title": "Expense VS Revenue 2008-2017",
        "barmode": "group",
        "bargap": 0.15,
        "bargroupgap": 0.1,
        "yaxis": {
            "title": "USD (Billions)"
        }
    }
}
pyo.plot(fig, filename='line.html')
