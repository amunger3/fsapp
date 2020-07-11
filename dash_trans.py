import dash
import dash_table
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

# Dash App rendering
app = dash.Dash(__name__)

app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df_static.columns],
    data=df_static.to_dict('records'),
)

# Run Server
if __name__ == '__main__':
    app.run_server(debug=True)
