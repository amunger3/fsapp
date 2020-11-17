import pandas as pd

from collections import defaultdict

aggregation = defaultdict(lambda: defaultdict(list))

def df_dd(in_df, teams_sel=None):
    if teams_sel:
        sel_df = in_df.query('tm_id in @teams_sel')
        in_dict = in_df.to_dict('records')
