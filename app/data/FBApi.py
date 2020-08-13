import re
import requests


class FBDataHandler:

    def __init__(self, league_id, season='2019', stage='REGULAR_SEASON', status='FINISHED'):
        self.baseUrl = 'https://api.football-data.org/v2/'
        self.apiToken = '065434220db543f6aafdb8565d85d359'
        self.headers = { 'X-Auth-Token': self.apiToken }
        self.league_ids = {
                            'ASL': '2024', 'BSA': '2013', 'BL' : '2002',
                            'FL1': '2015', 'PL' : '2021', 'ELC': '2016',
                            'PD' : '2014', 'SA' : '2019', 'PPL': '2017',
                            'DED': '2003', 'MLS': '2145', 'CL' : '2001',
                            'EL' : '2146'
                        }
        AZ = re.search(r"([A-Z])\w+", league_id)
        if AZ:
            self.league_id = self.league_ids[league_id]
        else:
            self.league_id = league_id
        self.season = season
        self.stage = stage
        self.status = status

    def _get(self, url, params={}):
        req = requests.get(self.baseUrl + url, headers=self.headers, params=params)
        status_code = req.status_code
        if status_code == requests.codes.ok:
            return req
        else:
            print("Request Error:", status_code)
            return

    def get_teams(self):
        params = {'season': self.season, 'stage': self.stage}
        req = self._get('competitions/{id}/teams'.format(id=self.league_id), params=params)
        return req.json()

    def df_setup(self):
        print("Setting up dataframe...")
        tmsReq = self.get_teams()
        tmsInit = {'attrs': {}, 'data': {}}
        for team in tmsReq['teams']:
            tmsInit['data'][team['id']] = {
                'name':      team['name'],
                'shortName': team['shortName'],
                'tla':       team['tla'],
                'eloRun':    [1500],
                'eloNow':    1500,
                'fixtures':  [],
                'results':   [],
                'tablePos':  0,
                'matches':   0,
                'won':       0,
                'draw':      0,
                'lost':      0,
                'points':    0,
                'goalsFor':  0,
                'goalsAga':  0,
                'goalDiff':  0
            }
        return tmsInit

    def get_league_results(self):
        params = {'season': self.season, 'stage': self.stage, 'status': self.status}
        print("Getting league results...")
        req = self._get('competitions/{id}/matches'.format(id=self.league_id), params=params)
        return req.json()

    def get_standings(self):
        params = {'season': self.season, 'stage': self.stage, 'standingType': 'TOTAL'}
        print("Getting league standings...")
        req = self._get('competitions/{id}/standings'.format(id=self.league_id), params=params)
        return req.json()
