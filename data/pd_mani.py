from static import LeagueConfigs
from run_calcs import EloRunCalc
import numpy as np
import pandas as pd


def robustFrame(lga='PL'):

    LC = LeagueConfigs()
    hdf = pd.HDFStore('storage.h5')
    lga_hdf = lga.lower()

    # Updating tables?
    if hdf.__contains__(lga_hdf):
        print("data present at {0}...deleting key".format(lga_hdf))
        hdf.remove(lga_hdf)

    pl_erc = EloRunCalc(LC._IDS[lga])
    print("Storing DataFrame...")
    df_epl = pl_erc.run_calcs()
    pd_epl = pd.DataFrame.from_dict(df_epl['data'], orient='index')
    hdf[lga_hdf] = pd_epl
    hdf.close()

    return pd_epl


if __name__ == '__main__':
    robustFrame(lga='FL1')
    robustFrame(lga='SA')
    robustFrame(lga='ELC')
