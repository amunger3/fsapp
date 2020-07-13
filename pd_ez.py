import json
from pathlib import Path
import pandas as pd
from pandas.io.json import json_normalize


def load_comp(comp_code):
    cwd = Path.cwd()
    desc = ['app', 'json', '.'.join((comp_code, 'json'))]
    jpath = cwd.joinpath(*desc)
    fjp = open(jpath, 'r')
    jload = json.load(fjp)
    fjp.close()
    jx = pd.DataFrame.from_dict(jload['data'], orient='index')
    return jx
