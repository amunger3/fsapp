import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash_table.Format import Format, Scheme, Sign, Symbol
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import requests_cache


# Initialize requests cache
requests_cache.install_cache('fbd_cache', backend='sqlite', expire_after=86400)

# Load HDF5 Storage
hdf_file = 'fbd_storage.h5'


# Competition selections
df_compsix = pd.read_hdf(hdf_file, 'comps')
df_compini = df_compsix[['label', 'value']]


def set_table_header(comp_code):
    comp_label = df_compsix.loc[comp_code]['label']
    year_str = '/'.join([
        df_compsix.loc[comp_code]['currentSeason']['startDate'].split('-')[0][-2:],
        df_compsix.loc[comp_code]['currentSeason']['endDate'].split('-')[0][-2:]
    ])
    table_header_str = ' '.join([comp_label, year_str])
    return table_header_str


card_title = set_table_header('PL')


# Pandas DataFrame variable
def comp_elo_df(comp_code):
    hdf_key = comp_code.lower()
    df_static = pd.read_hdf(hdf_file, hdf_key)
    df_static['lastFix'] = df_static['fixtures'].apply(lambda x: df_static.loc[x[-1]]['tla'])
    res_map = {0: 'L', 0.5: 'D', 1: 'W'}
    df_static['lastRes'] = df_static['results'].apply(lambda x: res_map[x[-1]])
    df_static['lastDiff'] = df_static['eloRun'].apply(lambda x: x[-1] - x[-2])
    df_static['eloRk'] = df_static['eloNow'].rank(ascending=False)
    return df_static


# df functions
def get_last(ix):
    return ix[-1]


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
        {'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'},
        {'if': {'column_type': 'text'},
            'textAlign': 'left'},
        {'if': {'column_type': 'numeric'},
            'textAlign': 'center'},
        {'if': {'column_id': 'lastRes'},
            'textAlign': 'center'},
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
    {
        'id': 'eloRk',
        'name': ['Pos.', 'Elo'],
        'type': 'numeric',
        'format': Format(
            precision=0,
            scheme=Scheme.fixed
        )
    },
    {
        'id': 'tablePos',
        'name': ['Pos.', 'Pts'],
        'type': 'numeric',
        'format': Format(
            precision=0,
            scheme=Scheme.fixed
        )
    },
    {'id': 'shortName', 'name': ['Team', 'Name'], 'type': 'text'},
    {
        'id': 'eloNow',
        'name': ['Team', 'Elo'],
        'type': 'numeric',
        'format': Format(
            precision=0,
            scheme=Scheme.fixed
        )
    },
    {
        'id': 'matches',
        'name': ['Season', 'MP'],
        'type': 'numeric',
        'format': Format(
            precision=0,
            scheme=Scheme.fixed
        )
    },
    {
        'id': 'won',
        'name': ['Season', 'W'],
        'type': 'numeric',
        'format': Format(
            precision=0,
            scheme=Scheme.fixed
        )
    },
    {
        'id': 'lost',
        'name': ['Season', 'L'],
        'type': 'numeric',
        'format': Format(
            precision=0,
            scheme=Scheme.fixed
        )
    },
    {
        'id': 'draw',
        'name': ['Season', 'D'],
        'type': 'numeric',
        'format': Format(
            precision=0,
            scheme=Scheme.fixed
        )
    },
    {
        'id': 'points',
        'name': ['Season', 'Pts'],
        'type': 'numeric',
        'format': Format(
            precision=0,
            scheme=Scheme.fixed
        )
    },
    {
        'id': 'goalsFor',
        'name': ['Goals', 'GF'],
        'type': 'numeric',
        'format': Format(
            precision=0,
            scheme=Scheme.fixed
        )
    },
    {
        'id': 'goalsAga',
        'name': ['Goals', 'GA'],
        'type': 'numeric',
        'format': Format(
            precision=0,
            scheme=Scheme.fixed
        )
    },
    {
        'id': 'goalDiff',
        'name': ['Goals', 'GD'],
        'type': 'numeric',
        'format': Format(
            precision=0,
            scheme=Scheme.fixed
        )
    },
    {
        'id': 'lastDiff',
        'name': ['Last Match', '+/-'],
        'type': 'numeric',
        'format': Format(
            precision=0,
            scheme=Scheme.fixed
        )
    },
    {'id': 'lastRes', 'name': ['Last Match', 'Res'], 'type': 'text'},
    {'id': 'lastFix', 'name': ['Last Match', 'vs.'], 'type': 'text'},
]

# Dash App rendering
app = dash.Dash(
    __name__,
    assets_ignore='.*dash-default.*',
    meta_tags=[
        {
            'charset': 'utf-8'
        },
        {
            'http-equiv': 'X-UA-Compatible',
            'content': 'IE=edge'
        },
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1.0'
        }
    ],
    title='Football Elo Ratings',
    update_title=None
)

server = app.server

app.layout = html.Div([
    html.Nav(
        html.Div(
            html.Div(
                html.Div(
                    children=[
                        html.A(
                            "Elo Football",
                            href="/",
                            className="uk-navbar-item uk-logo"
                        ),
                        html.Ul(
                            className="uk-navbar-nav",
                            children=[
                                html.Li(
                                    html.A(
                                        "Home",
                                        href="/"
                                    ),
                                    className="uk-active"
                                ),
                                html.Li(
                                    html.A(
                                        "Reset",
                                        href="/"
                                    ),
                                    className=""
                                ),
                            ]
                        ),
                    ],
                    className="uk-navbar-left"
                ),
                className="uk-navbar"
            ),
            className="uk-container"
        ),
        className="uk-navbar-transparent"
    ),
    html.Div(
        className="uk-container uk-margin-medium",
        children=[
            html.Div([
                html.P(
                    "Choose a Competition:",
                    className="uk-text-lead"
                ),
                dcc.Dropdown(
                    id='comps-dropdown',
                    options=df_compini.to_dict('records'),
                    placeholder="Select a Competition",
                    value='PL'
                ),
            ], className="uk-margin-small"),
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
                                style_cell={
                                    'fontFamily': 'Inter, Roboto, Nunito, Arial, sans-serif',
                                    'fontSize': '17px'
                                },
                                style_cell_conditional=[
                                    {'if': {'column_id': 'eloRk'},
                                    'width': '5%'},
                                    {'if': {'column_id': 'tablePos'},
                                    'width': '5%'},
                                    {'if': {'column_id': 'shortName'},
                                    'width': '20%'},
                                    {'if': {'column_id': 'eloNow'},
                                    'width': '10%'},
                                    {'if': {'column_id': 'matches'},
                                    'width': '5%'},
                                    {'if': {'column_id': 'won'},
                                    'width': '5%'},
                                    {'if': {'column_id': 'lost'},
                                    'width': '5%'},
                                    {'if': {'column_id': 'draw'},
                                    'width': '5%'},
                                    {'if': {'column_id': 'points'},
                                    'width': '5%'},
                                    {'if': {'column_id': 'goalsFor'},
                                    'width': '5%'},
                                    {'if': {'column_id': 'goalsAga'},
                                    'width': '5%'},
                                    {'if': {'column_id': 'goalDiff'},
                                    'width': '5%'},
                                    {'if': {'column_id': 'lastDiff'},
                                    'width': '5%'},
                                    {'if': {'column_id': 'lastRes'},
                                    'width': '5%'},
                                    {'if': {'column_id': 'lastFix'},
                                    'width': '5%'},
                                ],
                                style_data_conditional=styles,
                                style_header={
                                    'backgroundColor': 'rgb(69, 74, 79)',
                                    'color':  'rgb(233, 233, 240)',
                                    'fontFamily': 'Inter, Roboto, Nunito, Arial, sans-serif',
                                    'fontSize': '18px',
                                    'fontWeight': '400',
                                    'paddingLeft': '8px',
                                    'paddingRight': '8px',
                                },
                                style_header_conditional=[
                                    {'if': {'column_type': 'text'},
                                        'textAlign': 'left'},
                                    {'if': {'column_type': 'numeric'},
                                        'textAlign': 'center'},
                                ],
                                merge_duplicate_headers=True,
                                style_as_list_view=False,
                            )
                        ]
                    )
                ]
            ),
            html.Div(
                html.Div(
                    children=[
                        html.P(
                            children=[
                                "Created by Alex Munger – 2020 | ",
                                html.A(
                                    "GitHub",
                                    href="https://amunger3.github.io"
                                ),
                            ],
                            className="uk-text-center"
                        ),
                    ],
                    className="uk-container"
                ),
                className="uk-margin-medium"
            ),
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
