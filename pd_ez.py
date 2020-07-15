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


def json_to_hdf5(comp_code):

    pd_comp = load_comp(comp_code)
    print("Loaded JSON {0}.json as DataFrame...".format(comp_code))
    hdf = pd.HDFStore('fbd_storage.h5')
    lga_hdf = comp_code.lower()

    if hdf.__contains__(lga_hdf):
        print("data present at {0}...deleting key".format(lga_hdf))
        hdf.remove(lga_hdf)

    print("Storing DataFrame at /{0}".format(lga_hdf))
    pd_comp.to_hdf('fbd_storage.h5', lga_hdf)
    print("Storage of /{0} complete...".format(lga_hdf))
    hdf.close()

    return


if __name__ == '__main__':
    json_to_hdf5('BL')
