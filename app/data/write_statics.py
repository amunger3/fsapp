import requests

import json
from pathlib import Path

from static import LeagueConfigs


def write_tojsondir(w_df, name):
    cwd = Path.cwd()
    file_nx = name + '.json'
    dir_desc = ['app', 'json', file_nx]

    w_dir = cwd.joinpath(*dir_desc)
    jd = json.dumps(w_df, indent=4, ensure_ascii=False)

    print("Writing JSON...")
    fj = open(w_dir, 'w', encoding='utf-8')
    fj.write(jd)
    fj.close()


def write_comps_metas():
    cwd = Path.cwd()
    file_nx = 'competitions-stored.json'
    dir_desc = ['app', 'json', file_nx]
    w_dir = cwd.joinpath(*dir_desc)
    fj = open(w_dir, 'r')
    dob = json.loads(fj.read())
    return dob


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

    def get_teams(self, comp_id):
        """Fetches all teams in the league for setup."""
        req = self._get('competitions/{0}/teams'.format(comp_id), params=None)
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


def update_teams():
    comps = write_comps_metas()
    api_buddy = FBDataEntry()
    master_teams = dict()
    for comp in comps['competitions']:
        tms_cdf = api_buddy.get_teams(str(comp['id']))
        master_teams[str(comp['id'])] = tms_cdf
    write_tojsondir(master_teams, 'teams')




if __name__ == '__main__':
    # reinit_statics(get_areas=True, get_comps=True, plan=None, areas=None)
    update_teams()