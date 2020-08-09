# Module imports
print("Importing...")
from FBApi import FBDataHandler
import elo

# Built-in modules
import json
from pathlib import Path


# Calculations class
class EloRunCalc:

    def __init__(self, league_id, season='2019', stage='REGULAR_SEASON', status='FINISHED'):
        self.season = season
        self.stage = stage
        self.status = status
        FBD_Obj = FBDataHandler(league_id, season=self.season, stage=self.stage, status=self.status)
        self.tmDf = FBD_Obj.df_setup()
        self.matchReq = FBD_Obj.get_league_results()

    def run_calcs(self):
        tmDf = self.tmDf
        matchRes = self.matchReq['matches']

        print("Performing calculations...")
        for match in matchRes:
            team_1 = match['homeTeam']['id']
            team_2 = match['awayTeam']['id']

            score_1 = match['score']['fullTime']['homeTeam']
            score_2 = match['score']['fullTime']['awayTeam']

            if score_1 == score_2:
                wght_1 = 0.5
                wght_2 = 0.5
            else:
                wght_1 = int(score_1 > score_2)
                wght_2 = int(score_2 > score_1)

            tmDf['data'][team_1]['fixtures'].append(team_2)
            tmDf['data'][team_1]['results'].append(wght_1)
            tmDf['data'][team_2]['fixtures'].append(team_1)
            tmDf['data'][team_2]['results'].append(wght_2)

            cElo_1 = tmDf['data'][team_1]['eloNow']
            cElo_2 = tmDf['data'][team_2]['eloNow']

            nElos = elo.up_rating(cElo_1, cElo_2, wght_1, wght_2)
            nElo_1 = nElos[0]
            nElo_2 = nElos[1]

            tmDf['data'][team_1]['eloRun'].append(float(nElo_1))
            tmDf['data'][team_1]['eloNow'] = float(nElo_1)
            tmDf['data'][team_2]['eloRun'].append(float(nElo_2))
            tmDf['data'][team_2]['eloNow'] = float(nElo_2)

        return tmDf

    def w_json(self, w_df, name):
        cwd = Path.cwd()
        file_nx = name + '.json'
        dir_desc = ['json', file_nx]

        w_dir = cwd.joinpath(*dir_desc)
        jd = json.dumps(w_df, indent=4)

        print("Writing JSON...")
        fj = open(w_dir, 'w')
        fj.write(jd)
        fj.close()
