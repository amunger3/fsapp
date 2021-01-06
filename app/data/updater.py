from static import LeagueConfigs
from run_calcs import EloRunCalc
from write_statics import FBDataEntry

from datetime import datetime

import pandas as pd


# NOTE: this file must be run from the project root to load the existing HDF Store

LC = LeagueConfigs()


def comps_updater():

    FBDE = FBDataEntry()
    comps_all = FBDE.get_comps()
    comps_list = comps_all['competitions']
    comps_dict = dict()

    # Removes competitions with null code
    comps_dict.update([(comp['code'], comp) for comp in comps_list])

    stored_dict = LC._IDS
    stored_dict.update([(id_code, comps_dict[id_code]) for id_code in stored_dict.keys()])

    for key, val in stored_dict.items():
        cs_dates = (datetime.fromisoformat(val['currentSeason']['startDate']),
                    datetime.fromisoformat(val['currentSeason']['endDate']))
        yr_str = '/'.join([str(dt.year)[-2:] for dt in cs_dates])
        val['label'] = ' '.join([val['area']['name'], chr(8211), val['name'], yr_str])
        if key == val['code']:
            val['value'] = val.pop('code')

    hdf = pd.HDFStore(LC._H5)
    if hdf.__contains__('comps'):
        print('data present at /comps...deleting key')
        hdf.remove('comps')
    hdf.close()

    stored_df = pd.DataFrame.from_dict(stored_dict, orient='index')
    stored_df.to_hdf(LC._H5, 'comps')
    print('Storage of /comps complete...')
    hdf.close()

    return stored_dict


def hdf5_handler(lg_key='PL'):

    lga_hdf = lg_key.lower()
    hdf = pd.HDFStore(LC._H5)

    # Updating arrays
    if hdf.__contains__(lga_hdf):
        print('data present at {0}...deleting key'.format(lga_hdf))
        hdf.remove(lga_hdf)

    hdf.close()

    pl_erc = EloRunCalc(LC._IDS[lg_key], season='2020', stage='REGULAR_SEASON', status='FINISHED')
    print('Storing DataFrame at /{0}'.format(lga_hdf))
    df_comp = pl_erc.run_calcs()
    pd_comp = pd.DataFrame.from_dict(df_comp['data'], orient='index')
    pd_comp.to_hdf(LC._H5, lga_hdf)
    print('Storage of /{0} complete...'.format(lga_hdf))

    hdf.close()

    return


if __name__ == '__main__':
    # comps_updater() # Only run when necessary or will throw 400 errors.
    active_comps = ['BL1', 'FL1', 'PL', 'ELC', 'PD', 'SA', 'PPL', 'DED']
    for comp in active_comps:
        print('Updating {0}'.format(comp))
        hdf5_handler(lg_key=comp)
