from static import LeagueConfigs
from run_calcs import EloRunCalc
import numpy as np
import pandas as pd

# NOTE: this file must be run from the project root to load the existing HDF Store


def hdf5_handler(lg_key='PL'):

    LC = LeagueConfigs()
    hdf = pd.HDFStore('fbd_storage.h5')
    lga_hdf = lg_key.lower()

    # Updating arrays
    if hdf.__contains__(lga_hdf):
        print("data present at {0}...deleting key".format(lga_hdf))
        hdf.remove(lga_hdf)

    pl_erc = EloRunCalc(LC._IDS[lg_key])
    print("Storing DataFrame at /{0}".format(lga_hdf))
    df_comp = pl_erc.run_calcs()
    pd_comp = pd.DataFrame.from_dict(df_comp['data'], orient='index')
    pd_comp.to_hdf('fbd_storage.h5', lga_hdf)
    print("Storage of /{0} complete...".format(lga_hdf))
    hdf.close()

    return


if __name__ == '__main__':
    active_comps = ['PL', 'PD', 'SA', 'ELC', 'PPL']
    for comp in active_comps:
        print('Updating {0}'.format(comp))
        hdf5_handler(lg_key=comp)