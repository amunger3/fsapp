from app.data.FBApi import FBDataHandler


def test_filters():
    filtered = FBDataHandler('BL', season='2020', stage='REGULAR_SEASON', status='FINISHED')
    f_res = filtered.get_league_results()
    print(f_res['matches'][-1]['status'])
    assert f_res['matches'][-1]['status'] == 'FINISHED'


if __name__ == '__main__':
    test_filters()