import requests

import json
from pathlib import Path


def write_tojsondir(w_df, name):
    cwd = Path.cwd()
    file_nx = name + '.json'
    dir_desc = ['app', 'json', file_nx]

    w_dir = cwd.joinpath(*dir_desc)
    jd = json.dumps(w_df, indent=4)

    print("Writing JSON...")
    fj = open(w_dir, 'w')
    fj.write(jd)
    fj.close()


class FBDataEntry:

    def __init__(self):
        self.baseUrl = 'https://api.football-data.org/v2/'
        self.apiToken = '065434220db543f6aafdb8565d85d359'
        self.headers = { 'X-Auth-Token': self.apiToken }

    def _get(self, url, params):
        """Handles all api.football-data.org requests."""
        req = requests.get(self.baseUrl + url, headers=self.headers, params=params)
        status_code = req.status_code
        if status_code == requests.codes.ok:
            return req
        else:
            print("Request Error:", status_code)
            return

    def get_areas(self):
        """Fetches area relational data."""
        req = self._get('areas', params=None)
        return req.json()

    def get_comps(self, plan=None, areas=None):
        """Fetches all competitions covered by the API (optional params)."""
        if areas:
            if (type(areas) == str or type(areas) == int):
                areas_str = str(areas)
            elif (type(areas) == list or type(areas) == tuple):
                areas_str = ','.join([str(ai) for ai in areas])
            else:
                print("Please provide areas as an iterable.")
                areas_str = None
        else:
            areas_str = None
        params = {'plan': plan, 'areas': areas_str}
        req = self._get('competitions', params=params)
        return req.json()

    def get_teams(self):
        """Fetches all teams in the league for setup."""
        req = self._get('competitions/{id}/teams'.format(id=self.league_id), params=None)
        return req.json()


def reinit_statics(get_areas=True, get_comps=True, plan=None, areas=None):
    api_buddy = FBDataEntry()
    if get_areas:
        areas_df = api_buddy.get_areas()
        write_tojsondir(areas_df, 'areas')
    if get_comps:
        comps_df = api_buddy.get_comps(plan=plan, areas=areas)
        if (plan or areas):
            nameadd = plan + '_'
        else:
            nameadd = 'all'
        name = '-'.join(['competitions', nameadd])
        write_tojsondir(comps_df, name)


if __name__ == '__main__':
    reinit_statics(get_areas=True, get_comps=True, plan=None, areas=None)