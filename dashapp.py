import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_table
from dash_table.Format import Format, Scheme
from dash.dependencies import Input, Output
import pandas as pd
import requests_cache


# Initialize requests cache
requests_cache.install_cache('fbd_cache', backend='sqlite', expire_after=86400)

# Load HDF5 Storage
_H5 = 'fbd_storage.h5'

# Competition selections
df_compsix = pd.read_hdf(_H5, 'comps')
df_compini = df_compsix[['label', 'value']]


def set_table_header(comp_code):
    comp_label = df_compsix.loc[comp_code]['label']
    return comp_label


initial_comp = 'PL'
card_title = set_table_header(initial_comp)


def comp_elo_df(comp_code):
    hdf_key = comp_code.lower()
    df_static = pd.read_hdf(_H5, hdf_key)
    df_static['lastFix'] = df_static['fixtures'].apply(lambda x: df_static.loc[x[-1]]['tla'])
    res_map = {0: 'L', 0.5: 'D', 1: 'W'}
    df_static['lastRes'] = df_static['results'].apply(lambda x: res_map[x[-1]])
    df_static['lastDiff'] = df_static['eloRun'].apply(lambda x: x[-1] - x[-2])
    df_static['eloRk'] = df_static['eloNow'].rank(ascending=False)
    return df_static


def all_elo_df():
    active_comps = ['BL1', 'FL1', 'PL', 'ELC', 'PD', 'SA', 'PPL', 'DED']
    df_all = pd.concat([comp_elo_df(cc) for cc in active_comps], ignore_index=True)
    return df_all


df_static = comp_elo_df(initial_comp)
teams_list = [{'label': df_static.loc[ix]['name'], 'value': ix} for ix in df_static.index]
team_links = [html.Li(dcc.Link(team['label'], href=str(team['value']))) for team in teams_list]


def bkg_color_bins(df, n_bins=9, columns=['eloNow']):
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    if columns == 'all':
        if 'id' in df:
            df_numeric_cols = df.select_dtypes('number').drop(['id'], axis=1)
        else:
            df_numeric_cols = df.select_dtypes('number')
    else:
        df_numeric_cols = df[columns]
    df_max = df_numeric_cols.max().max()
    df_min = df_numeric_cols.min().min()
    ranges = [((df_max - df_min) * i) + df_min for i in bounds]
    styles = [
        {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
        {'if': {'column_type': 'text'}, 'textAlign': 'left'},
        {'if': {'column_type': 'numeric'}, 'textAlign': 'center'},
        {'if': {'column_id': 'lastRes'}, 'textAlign': 'center'},
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

        for column in df_numeric_cols:
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
            html.Div(
                style={'display': 'inline-block', 'width': '64px'},
                children=[
                    html.Div(
                        style={
                            'backgroundColor': backgroundColor,
                            'borderLeft': legend_border_left,
                            'borderRight': legend_border_right,
                            'borderTop': '2px rgb(64, 64, 64) solid',
                            'borderBottom': '2px rgb(64, 64, 64) solid',
                            'height': '32px'
                        }
                    ),
                    html.Small(round(min_bound), style={'paddingLeft': '-2px'})
                ]
            )
        )
        full_scale = html.Small(color_scale, style={'paddingLeft': '2px'})

    return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}), full_scale)


(styles, legend, full_scale) = bkg_color_bins(df_static)

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

layout_index = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Nav(
        children=[
            html.Div(
                children=[
                    html.A(
                        "Elo Football",
                        href="/",
                        className="uk-navbar-item uk-logo"
                    ),
                    html.Ul(
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
                                    "PageAlt",
                                    href="/page-alt"
                                ),
                                className=""
                            ),
                            html.Li(
                                id="page-location"
                            ),
                        ],
                        className="uk-navbar-nav"
                    ),
                ],
                className="uk-navbar-left"
            ),
        ],
        className="uk-navbar-container uk-navbar-transparent"
    ),
    html.Div(
        className="uk-container uk-margin-small",
        children=[
            html.Div(
                className="uk-container uk-margin-small",
                children=[
                    html.Div(
                        className="uk-card uk-card-default uk-card-small uk-card-body",
                        children=[
                            html.Span(
                                "Choose a Competition:",
                                className="uk-text"
                            ),
                            html.Div(
                                dcc.Dropdown(
                                    id='comps-dropdown',
                                    options=df_compini.to_dict('records'),
                                    placeholder="All Competitions",
                                    value=initial_comp
                                ),
                            className='uk-margin-small'
                            )
                        ]
                    ),
                    html.Div(
                        className="uk-card uk-card-default uk-card-small uk-card-body uk-margin-small",
                        children=[
                            html.P(
                                children=card_title,
                                className="uk-text-lead",
                                id="comp-title"
                            )
                        ]
                    )
                ],
            ),
            dcc.Tabs(
                id='tabs',
                value='league-view',
                parent_className='tabs',
                className='tabs-container',
                children=[
                    dcc.Tab(
                        label='Leagues',
                        value='league-view',
                        className='tab',
                        selected_className='tab--selected',
                        children=[
                            html.Div(
                                className="uk-card uk-card-default",
                                id="tab-content-1",
                                children=[
                                    html.Div(
                                        className="uk-card-body",
                                        children=[
                                            daq.ToggleSwitch(
                                                id='colorscale-toggle',
                                                color='#ffffff',
                                                label='Show color scale',
                                                size=36,
                                                style={'margin-bottom': '1.0em'},
                                                value=False
                                            ),
                                            dash_table.DataTable(
                                                id='elolgtable',
                                                columns=elo_columns,
                                                data=df_static.to_dict('records'),
                                                sort_action='custom',
                                                sort_mode='single',
                                                sort_by=[],
                                                style_cell={
                                                    'fontFamily': 'Inter var, Inter, Roboto, Nunito, Arial, sans-serif',
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
                                            ),
                                            html.Div(
                                                className="uk-card uk-card-small uk-padding-remove uk-margin-small uk-align-right",
                                                children=[
                                                    html.Div(
                                                        children=legend,
                                                        id="colorbins-legend",
                                                        className="uk-card-body"
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ],
                            ),
                        ],
                    ),
                    dcc.Tab(
                        label='Teams',
                        value='team-view',
                        className='tab',
                        selected_className='tab--selected',
                        children=[
                            html.Div(
                                className="uk-card uk-card-default",
                                id="tab-content-2",
                                children=[
                                    html.Div(
                                        className="uk-card-body",
                                        children=[
                                            html.Div([
                                                html.P(
                                                    "Teams List",
                                                    className="uk-text-lead"
                                                ),
                                            ],
                                            className="uk-margin-small"
                                            ),
                                            html.Ul(
                                                id="team-links",
                                                className="uk-list",
                                                children=team_links
                                            )
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
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

server = app.server
app.layout = layout_index


# Callbacks
@app.callback(dash.dependencies.Output('page-location', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    return html.A(pathname, href="#")


@app.callback(
    [Output('elolgtable', 'data'),
    Output('elolgtable', 'style_data_conditional'),
    Output('comp-title', 'children'),
    Output('colorbins-legend', 'children'),
    Output('team-links', 'children')],
    [Input('comps-dropdown', 'value'),
    Input('elolgtable', 'sort_by'),
    Input('colorscale-toggle', 'value')])
def update_table(value, sort_by, colorbins_bool):
    if value:
        df_static = comp_elo_df(value)
        card_title = set_table_header(value)
    else:
        df_static = all_elo_df()
        card_title = 'All Competitions'

    if len(sort_by):
        df_sorted = df_static.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc'
        )
    else:
        df_sorted = df_static.sort_values(
            'eloNow',
            ascending=False
        )
    teams_list = [{'label': df_static.loc[ix]['name'], 'value': ix} for ix in df_static.index]
    team_links = [html.Li(dcc.Link(team['label'], href=str(team['value']))) for team in teams_list]
    (styles, legend, full_scale) = bkg_color_bins(df_static)

    return df_sorted.to_dict('records'), styles, card_title, legend, team_links


if __name__ == '__main__':
    app.run_server(debug=True)
