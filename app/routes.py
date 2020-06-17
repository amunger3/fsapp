from flask import Flask, render_template, request, jsonify
from app import app
import datetime
import json
import requests
import requests_cache
import time


@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    return value.strftime(format)

app.jinja_env.filters['datetimefilter'] = datetimefilter


@app.route('/')
def index():
    return render_template('index.html.jinja', title='Index',
                            current_time=datetime.datetime.now())