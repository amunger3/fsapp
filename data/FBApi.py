import re
import requests


class FBDataHandler:

    def __init__(self, league_id):
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

    def _get(self, url):
        """Handles all api.football-data.org requests."""
        req = requests.get(self.baseUrl + url, headers=self.headers)
        status_code = req.status_code
        if status_code == requests.codes.ok:
            return req
        else:
            print("Request Error:", status_code)
            return

    def get_teams(self):
        """Fetches all teams in the league for setup."""
        req = self._get('competitions/{id}/teams'.format(id=self.league_id))
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
                'results':   []
            }
        return tmsInit

    def get_league_results(self):
        """Fetches all results for a league season for analysis."""
        print("Getting league results...")
        req = self._get('competitions/{id}/matches'.format(id=self.league_id))
        return req.json()
