import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
from dash.dependencies import Input, Output

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
EXPENSE_FILE = '{}/../data/city-expenses-2005-2017.csv'.format(APP_ROOT)
REVENUE_FILE = '{}/../data/city-revenues-2005-2017.csv'.format(APP_ROOT)
years = [str(x) for x in range(2007, 2017)]
years_reverse = [str(x) for x in reversed(range(2007, 2017))]

e_df = pd.read_csv(EXPENSE_FILE, delimiter=';')
r_df = pd.read_csv(REVENUE_FILE, delimiter=';')
expense_total_df = e_df[e_df['level'] == 0][years]
revenue_total_df = r_df[r_df['level'] == 0][years]
expense_df = e_df[e_df['level'] == 1]
revenue_df = r_df[r_df['level'] == 1]
expense_sorted_df = expense_df.sort_values(by=['2016'], ascending=False)
revenue_sorted_df = revenue_df.sort_values(by=['2016'], ascending=False)

external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

app = dash.Dash(external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.Nav([html.A("Durham County Budget Dashboard", className="navbar-brand text-white")],
             className="navbar navbar-expand-sm bg-primary navbar-dark"),

    html.Div([
        html.Div([
            html.Div([
                dcc.Graph(id='exp-vs-rev-bar-chart')
            ], style={'margin-top': 10}),
            html.Div([
                dcc.RangeSlider(
                    id='year-range-slider',
                    min=0,
                    max=len(years) - 1,
                    value=[0, len(years) - 1],
                    marks=dict(zip(range(len(years)), years)),
                    included=False
                )], style={'margin-bottom': 30, 'margin-top': 5})
        ], className="container-fluid bg-light rounded col-6 border"),

        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='exp-vs-rev-year',
                    options=[{'label': year, 'value': year}
                             for year in years_reverse],
                    value='2016',
                    clearable=False
                )
            ], style={'width': '48%', 'display': 'inline-block'}, className="col-3"),
            dcc.Graph(id='exp-vs-rev-pie-chart')
        ], className="container-fluid bg-light rounded col-6 border")
    ], style={'margin-bottom': 50, 'margin-top': 10, 'margin-left': 5, 'margin-right': 5}, className="row"),

    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='exp-department-multi-dropdown',
                    options=[{'label': i.replace(' Total', ''), 'value': i}
                             for i in expense_sorted_df['level1']],
                    value=['WATER MANAGEMENT Total',
                           'POLICE Total', 'PUBLIC WORKS Total'],
                    multi=True
                )], style={'display': 'inline-block'}, className="col-9"),
            html.Div([
                dcc.Graph(id='exp-line-chart')
            ], style={'margin-top': 10})
        ], className="col-6 container-fluid bg-light rounded col-6 border"),

        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='rev-department-multi-dropdown',
                    options=[{'label': i.replace(' Total', ''), 'value': i}
                             for i in revenue_sorted_df['level1']],
                    value=['UNDEFINED Total', 'WATER MANAGEMENT Total',
                           'PUBLIC WORKS Total', 'FINANCE Total'],
                    multi=True
                )], style={'display': 'inline-block'}, className="col-9"),
            html.Div([
                dcc.Graph(id='rev-line-chart')
            ], style={'margin-top': 10})
        ], className="col-6 container-fluid bg-light rounded col-6 border")
    ], style={'margin-bottom': 50, 'margin-left': 5, 'margin-right': 5}, className="row")
], className="container-fluid")


@app.callback(Output('exp-vs-rev-pie-chart', 'figure'),
              [Input('exp-vs-rev-year', 'value')])
def update_pie_chart(fiscal_year):
    return {
        "data": [
            {
                "values": expense_df[fiscal_year],
                "labels": expense_df['level1'].str.replace(' Total', ''),
                "textposition": "inside",
                "domain": {"x": [0, 0.48]},
                "name": "Expense",
                "hoverinfo": "label+percent+name",
                "hole": .4,
                "type": "pie"
            },
            {
                "values": revenue_df[fiscal_year],
                "labels": revenue_df['level1'].str.replace(' Total', ''),
                "textposition": "inside",
                "domain": {"x": [0.52, 1]},
                "name": "Revenue",
                "hoverinfo": "label+percent+name",
                "hole": .4,
                "type": "pie"
            }
        ],
        "layout": {
            "title": "Expense VS Revenue {}".format(fiscal_year),
            "annotations": [
                {
                    "font": {
                        "size": 16
                    },
                    "x": 0.20,
                    "y": 0.5,
                    "showarrow": False,
                    "text": "Expense"
                },
                {
                    "font": {
                        "size": 16
                    },
                    "x": 0.80,
                    "y": 0.5,
                    "showarrow": False,
                    "text": "Revenue"
                }
            ]
        }
    }


@app.callback(Output('exp-vs-rev-bar-chart', 'figure'),
              [Input('year-range-slider', 'value')])
def update_bar_chart(index):
    start = index[0]
    end = index[1] + 1
    return {
        "data": [
            {
                "x": years[start:end],
                "y": expense_total_df.iloc[0][start:end],
                "name": "Expense",
                "hoverinfo":"x+y+name",
                "type": "bar"
            },
            {
                "x": years[start:end],
                "y": revenue_total_df.iloc[0][start:end],
                "textposition":"inside",
                "name": "Revenue",
                "hoverinfo":"x+y+name",
                "type": "bar"
            }
        ],
        "layout": {
            "title": "Expense VS Revenue {}-{}".format(years[start], years[end - 1]),
            "barmode": "group",
            "bargap": 0.15,
            "bargroupgap": 0.1,
            "yaxis": {
                "title": "USD (Millions)"
            }
        }
    }


@app.callback(Output('exp-line-chart', 'figure'),
              [Input('exp-department-multi-dropdown', 'value')])
def update_exp_line_chart(department_picker):
    traces = []
    for department in department_picker:
        df = expense_df[expense_df['level1'] == department]
        traces.append({
            'x': years,
            'y': df[years].iloc[0],
            'name': department.replace(' Total', '')
        })
    fig = {
        'data': traces,
        'layout': {
            'title': 'Expense Trend by Department {}-{}'.format(years[0], years[-1]),
            "yaxis": {
                "title": "USD"
            }
        }
    }
    return fig


@app.callback(Output('rev-line-chart', 'figure'),
              [Input('rev-department-multi-dropdown', 'value')])
def update_rev_line_chart(department_picker):
    traces = []
    for department in department_picker:
        df = revenue_df[revenue_df['level1'] == department]
        traces.append({
            'x': years,
            'y': df[years].iloc[0],
            'name': department.replace(' Total', '')
        })
    fig = {
        'data': traces,
        'layout': {
            'title': 'Revenue Trend by Department {}-{}'.format(years[0], years[-1]),
            "yaxis": {
                "title": "USD"
            }
        }
    }
    return fig


if __name__ == '__main__':
    app.run_server()
