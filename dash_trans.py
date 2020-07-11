import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash_table.Format import Format, Scheme, Sign, Symbol
import pandas as pd

import json
from pathlib import Path


# Loading JSON
approot = Path.cwd()
lg_abr = 'PL'
lg_nx = lg_abr + '.json'
tojsondir = ['app', 'json', lg_nx]
fullpath = approot.joinpath(*tojsondir)
fpo = open(fullpath, 'r')
json_fpo = json.load(fpo)
fpo.close()

# Pandas DataFrame setup
df_x = pd.DataFrame.from_dict(json_fpo['data'], orient='index')
df_static = df_x[['name', 'shortName', 'tla', 'eloNow']]


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
        'rgb(215,48,39)',
        'rgb(244,109,67)',
        'rgb(253,174,97)',
        'rgb(254,224,139)',
        'rgb(255,255,191)',
        'rgb(217,239,139)',
        'rgb(166,217,106)',
        'rgb(102,189,99)',
        'rgb(26,152,80)'
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
                'color': 'rgb(16, 16, 16)',
                'fontWeight': 'bold'
            })
        legend.append(
            html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
                html.Div(
                    style={
                        'backgroundColor': backgroundColor,
                        'borderLeft': '1px rgb(64, 64, 64) solid',
                        'height': '16px'
                    }
                ),
                html.Small(round(min_bound), style={'paddingLeft': '2px'})
            ])
        )
        full_scale = html.Small(color_scale, style={'paddingLeft': '2px'})

    return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}), full_scale)


(styles, legend, full_scale) = discrete_background_color_bins(df_static)

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
            html.Div(
                className="uk-card uk-card-default",
                children=[
                    html.Div(
                        html.H3(
                            "English Premier League Elo Ratings 2019-2020",
                            className="uk-card-title"
                        ),
                        className="uk-card-header"
                    ),
                    html.Div(
                        className="uk-card-body",
                        children=[
                            html.Div(legend, style={'float': 'right'}),
                            dash_table.DataTable(
                                id='elolgtable',
                                columns=[
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
                                    ],
                                data=df_static.to_dict('records'),
                                sort_action='native',
                                style_cell={
                                    'fontFamily': 'Nunito, Roboto, Inter, Arial, sans-serif',
                                    'fontSize': '17px'
                                },
                                style_data_conditional=styles,
                                style_header={
                                    'backgroundColor': 'rgb(50, 23, 77)',
                                    'color':  'rgb(248, 255, 236)',
                                    'fontWeight': 'bold'
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

# Run Server
if __name__ == '__main__':
    app.run_server(debug=True)
