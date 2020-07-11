from pathlib import Path
import datetime
import json
import requests
import requests_cache
import time
from flask import Flask, render_template, request, jsonify
from app import app
from app.data.static import LeagueConfigs


def get_json(lg_abr, mime=0):
    approot = Path.cwd()
    lg_nx = lg_abr + '.json'
    tojsondir = ['app', 'json', lg_nx]
    fullpath = approot.joinpath(*tojsondir)
    fpo = open(fullpath, 'r')
    json_fpo = json.load(fpo)
    fpo.close()
    if mime:
        return jsonify(json_fpo)
    else:
        return json_fpo


@app.route('/')
def index():
    return render_template('index.html.jinja', title='Elo Football App – Index',
                            comps=LeagueConfigs._IDS,
                            current_time=datetime.datetime.now())


@app.route("/comp/<lg_abr>")
def elo_lgtable(lg_abr):
    elo_lgobj = get_json(lg_abr, mime=0)
    return render_template('elotable.html.jinja', title=lg_abr,
                            dfo=elo_lgobj,
                            current_time=datetime.datetime.now())


@app.route("/comp/<lg_abr>/json")
def raw_return(lg_abr):
    json_rawapi = get_json(lg_abr, mime=1)
    return json_rawapi
