import os
import json
from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash_table.Format import Format, Scheme, Sign, Symbol
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import requests
import requests_cache


# Initialize requests cache
requests_cache.install_cache('fbd_cache', backend='sqlite', expire_after=86400)

# Load HDF5 Storage
hdf_file = 'fbd_storage.h5'


# Competition selections
df_comps = pd.read_hdf(hdf_file, 'comps')
df_comps.rename(columns={'name': 'label', 'code': 'value'}, inplace=True)
df_compsix = df_comps.set_index('value', drop=False)
df_compini = df_comps[['label', 'value']]


def set_table_header(comp_code):
    comp_name = df_compsix.loc[comp_code]['label']
    area_name = df_compsix.loc[comp_code]['area']['name']
    year_str = '/'.join([
        df_compsix.loc[comp_code]['currentSeason']['startDate'].split('-')[0][-2:],
        df_compsix.loc[comp_code]['currentSeason']['endDate'].split('-')[0][-2:]
        ])
    table_header_str = area_name + ': ' + comp_name + ' ' + year_str
    return table_header_str


card_title = set_table_header('PL')


# Pandas DataFrame variable
def comp_elo_df(comp_code):
    hdf_key = comp_code.lower()
    df_static = pd.read_hdf(hdf_file, hdf_key)
    # df_static = df_x[['name', 'shortName', 'tla', 'eloNow']]
    return df_static


df_static = comp_elo_df('PL')


# Colorbins setup
def discrete_background_color_bins(df, n_bins=9, columns=['eloNow']):
    import colorlover
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    if columns == 'all':
        if 'id' in df:
            df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
        else:
            df_numeric_columns = df.select_dtypes('number')
    else:
        df_numeric_columns = df[columns]
    df_max = df_numeric_columns.max().max()
    df_min = df_numeric_columns.min().min()
    ranges = [
        ((df_max - df_min) * i) + df_min
        for i in bounds
    ]
    styles = [
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        },
        {
            'if': {
                'column_type': 'text'  # 'text' | 'any' | 'datetime' | 'numeric'
            },
            'textAlign': 'left'
        }
    ]
    legend = []
    color_scale = [
        'rgb(214,83,80)',
        'rgb(242,129,95)',
        'rgb(253,176,98)',
        'rgb(254,224,139)',
        'rgb(255,255,191)',
        'rgb(217,239,139)',
        'rgb(164,216,105)',
        'rgb(108,211,105)',
        'rgb(80,226,143)'
        ]
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        backgroundColor = color_scale[i - 1]
        # color = 'white' if i > len(bounds) / 2. else 'inherit'

        for column in df_numeric_columns:
            styles.append({
                'if': {
                    'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
                'backgroundColor': backgroundColor,
                'color': 'rgb(8, 8, 8)',
                'fontWeight': '500'
            })

        legend_border_left = '1px rgb(64, 64, 64) solid'
        legend_border_right = '1px rgb(64, 64, 64) solid'
        if i == 1:
            legend_border_left = '2px rgb(64, 64, 64) solid'
        elif i == n_bins:
            legend_border_right = '2px rgb(64, 64, 64) solid'
        legend.append(
            html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
                html.Div(
                    style={
                        'backgroundColor': backgroundColor,
                        'borderLeft': legend_border_left,
                        'borderRight': legend_border_right,
                        'borderTop': '2px rgb(64, 64, 64) solid',
                        'borderBottom': '2px rgb(64, 64, 64) solid',
                        'height': '16px'
                    }
                ),
                html.Small(round(min_bound), style={'paddingLeft': '2px'})
            ])
        )
        full_scale = html.Small(color_scale, style={'paddingLeft': '2px'})

    return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}), full_scale)


(styles, legend, full_scale) = discrete_background_color_bins(df_static)

elo_columns = [
    {'id': 'shortName', 'name': 'Team', 'type': 'text'},
    {'id': 'tla', 'name': 'TLA', 'type': 'text'},
    {
        'id': 'eloNow',
        'name': 'Elo (Cur.)',
        'type': 'numeric',
        'format': Format(
            precision=0,
            scheme=Scheme.fixed
        )
    }
]

# Dash App rendering
app = dash.Dash(
    __name__,
    assets_ignore='.*main.*',
    meta_tags=[
        {
            'http-equiv': 'X-UA-Compatible',
            'content': 'IE=edge'
        },
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1.0'
        }
    ]
)

server = app.server

app.layout = html.Div([
    html.Nav(
        html.Div(
            html.Div(
                html.Ul(
                    className="uk-navbar-nav",
                    children=[
                        html.Li(
                            html.A(
                                "Home",
                                href="/"
                            ),
                            className=""
                        )
                    ]
                ),
                className="uk-navbar-center"
            ),
            className="uk-container"
        ),
        className="uk-navbar uk-navbar-transparent"
    ),
    html.Div(
        className="uk-container uk-margin-medium",
        children=[
            html.Div([
                dcc.Dropdown(
                    id='comps-dropdown',
                    options=df_compini.to_dict('records'),
                    placeholder="Select a Competition",
                    value='PL'
                ),
                html.Div(id='comps-output-container')
            ]),
            html.Div(
                className="uk-card uk-card-default",
                children=[
                    html.Div(
                        html.H3(
                            children=card_title,
                            className="uk-card-title",
                            id="tablecard-title"
                        ),
                        className="uk-card-header"
                    ),
                    html.Div(
                        className="uk-card-body",
                        children=[
                            html.Div(
                                children=legend,
                                style={'float': 'right'},
                                id="colorbins-legend"
                            ),
                            dash_table.DataTable(
                                id='elolgtable',
                                columns=elo_columns,
                                data=df_static.to_dict('records'),
                                sort_action='native',
                                sort_mode='multi',
                                style_cell={
                                    'fontFamily': 'Inter, Roboto, Nunito, Arial, sans-serif',
                                    'fontSize': '17px'
                                },
                                style_data_conditional=styles,
                                style_header={
                                    'backgroundColor': 'rgb(50, 23, 77)',
                                    'color':  'rgb(248, 255, 236)',
                                    'fontWeight': '500'
                                },
                                style_header_conditional=[
                                    {
                                        'if': {
                                            'column_type': 'text'  # 'text' | 'any' | 'datetime' | 'numeric'
                                            },
                                        'textAlign': 'left'
                                    }
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
])


# Callbacks
@app.callback(
    [Output('elolgtable', 'data'),
    Output('elolgtable', 'style_data_conditional'),
    Output('tablecard-title', 'children'),
    Output('colorbins-legend', 'children')],
    [Input('comps-dropdown', 'value')])
def update_table(value):
    df_static = comp_elo_df(value)
    card_title = set_table_header(value)
    (styles, legend, full_scale) = discrete_background_color_bins(df_static)
    return df_static.to_dict('records'), styles, card_title, legend


# Run Server
if __name__ == '__main__':
    app.run_server(debug=True)
