# Module imports
from FBApi import FBDataHandler
from elo import Elo

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
        self.standReq = FBD_Obj.get_standings()

    def run_calcs(self):
        tmDf = self.tmDf
        matchRes = self.matchReq['matches']
        standRes = self.standReq['standings']

        print('Performing calculations...')
        for match in matchRes:
            teams = (match['homeTeam']['id'], match['awayTeam']['id'])
            scores = (match['score']['fullTime']['homeTeam'], match['score']['fullTime']['awayTeam'])
            if scores[0] == scores[1]:
                wts = (0.5, 0.5)
            else:
                wts = (int(scores[0] > scores[1]), int(scores[1] > scores[0]))

            tmDf['data'][teams[0]]['fixtures'].append(teams[1])
            tmDf['data'][teams[0]]['results'].append(wts[0])
            tmDf['data'][teams[1]]['fixtures'].append(teams[0])
            tmDf['data'][teams[1]]['results'].append(wts[1])

            cRs = tuple(tmDf['data'][tm]['eloNow'] for tm in teams)
            nElo = Elo(R_tup=cRs, S_tup=wts)

            tmDf['data'][teams[0]]['eloRun'].append(float(nElo.Rnew[0]))
            tmDf['data'][teams[0]]['eloNow'] = float(nElo.Rnew[0])
            tmDf['data'][teams[1]]['eloRun'].append(float(nElo.Rnew[1]))
            tmDf['data'][teams[1]]['eloNow'] = float(nElo.Rnew[1])

        for lg_pos in standRes[0]['table']:
            tm_id = lg_pos['team']['id']
            tmDf['data'][tm_id]['tablePos'] = lg_pos['position']
            tmDf['data'][tm_id]['matches'] = lg_pos['playedGames']
            tmDf['data'][tm_id]['won'] = lg_pos['won']
            tmDf['data'][tm_id]['draw'] = lg_pos['draw']
            tmDf['data'][tm_id]['lost'] = lg_pos['lost']
            tmDf['data'][tm_id]['points'] = lg_pos['points']
            tmDf['data'][tm_id]['goalsFor'] = lg_pos['goalsFor']
            tmDf['data'][tm_id]['goalsAga'] = lg_pos['goalsAgainst']
            tmDf['data'][tm_id]['goalDiff'] = lg_pos['goalDifference']

        return tmDf

    def w_json(self, w_df, name):
        cwd = Path.cwd()
        file_nx = name + '.json'
        dir_desc = ['app', 'json', file_nx]

        w_dir = cwd.joinpath(*dir_desc)
        jd = json.dumps(w_df, indent=4, ensure_ascii=False)

        fj = open(w_dir, 'w', encoding='utf-8')
        fj.write(jd)
        fj.close()
