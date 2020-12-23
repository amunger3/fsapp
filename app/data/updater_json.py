from static import LeagueConfigs
from run_calcs import EloRunCalc
import json


LC = LeagueConfigs()


def write_comps_metas():

    cwd = Path.cwd()
    file_nx = 'competitions-stored.json'
    dir_desc = ['app', 'json', file_nx]
    w_dir = cwd.joinpath(*dir_desc)
    fj = open(w_dir, 'r')
    dob = json.loads(fj.read())

    return dob


def json_handler(lg_key='PL', write=True):

    pl_erc = EloRunCalc(LC._IDS[lg_key], season='2020', stage='REGULAR_SEASON', status='FINISHED')
    df_comp = pl_erc.run_calcs()
    df_comp['attrs'] = LC._PROPERTIES[lg_key]

    print('Storing JSON for {0} (id: {1})'.format(lg_key, LC._IDS[lg_key]))
    if write:
        pl_erc.w_json(df_comp, lg_key)

    return (lg_key, df_comp)


if __name__ == '__main__':
    active_comps = ['BL', 'FL1', 'PL', 'ELC', 'PD', 'SA', 'PPL', 'DED']
    fbd = dict()
    fbd

    for comp in active_comps:
        print('Updating {0}'.format(comp))
        fbc = json_handler(lg_key=comp, write=True)
        fbd[fbc[0]] = fbc[1]

    jsd = json.dumps(fbd, indent=4, ensure_ascii=False)
    print('Writing Master JSON...')
    fsj = open('fbd.json', 'w', encoding='utf-8')
    fsj.write(jsd)
    fsj.close()
