from static import LeagueConfigs
from run_calcs import EloRunCalc


LC = LeagueConfigs()
lgids = LC._IDS
lgpts = LC._PROPERTIES


def writerate_main(ignore=[]):

    for lgi in ignore:
        lgids.pop(lgi)

    mod_files = []

    for abr, idstr in lgids.items():

        print("Getting match data for {0}".format(abr))
        erc_inst = EloRunCalc(idstr)

        erc_inst.tmDf['attrs'] = lgpts[abr]
        erc_tmc = len(erc_inst.tmDf['data'].keys())

        print("Running calcs for {0}-team competition".format(erc_tmc))
        erc_df = erc_inst.run_calcs()

        print("Writing output file >-> {0}.json".format(abr))
        erc_inst.w_json(erc_df, abr)

        mod_files.append(abr + '.json')

    return mod_files


if __name__ == '__main__':
    writerate_main(ignore=['PL', 'ELC', 'PD', 'PPL', 'SA', 'DED'])
