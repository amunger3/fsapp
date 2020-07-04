from pathlib import Path
import datetime
import json
import requests
import requests_cache
import time
from flask import Flask, render_template, request, jsonify
from app import app
from app.data.static import LeagueConfigs


@app.route('/')
def index():
    return render_template('index.html.jinja', title='Elo Football App – Index',
                            comps=LeagueConfigs._IDS,
                            current_time=datetime.datetime.now())