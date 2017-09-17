from flask import Flask, render_template
import flask_shelve
app = Flask(__name__)

import pandas as pd
import numpy as np
from urllib.request import urlopen
import re, zipfile, io
import json
import datetime
import calendar, time
from newspaper import Article

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper



app.config['SHELVE_FILENAME'] = 'shelve.db'
flask_shelve.init_app(app)

TONE_COLUMN = 34
QUADS_COLUMN = 29

#from flas site
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

def updateGdeltCSVs():
    print("getting latest file urls")
    latestFileInfo = urlopen("http://data.gdeltproject.org/gdeltv2/lastupdate.txt")
    latestFileUrls = []
    print("got latest file urls")
    for line in latestFileInfo:
        url = re.search("http:.*zip",line.decode()).group(0)
        latestFileUrls.append(url)
    latestFileCSVs = []
    for url in latestFileUrls:
        zipped = urlopen(url)
        z = zipfile.ZipFile(io.BytesIO(zipped.read()))
        file = z.open(z.namelist()[0])
        latestFileCSVs.append(file)
    return latestFileCSVs

def processGdeltData():
    files = updateGdeltCSVs()
    print("downloaded new files")
    print("loading db")
    db = flask_shelve.get_shelve('c')
    print("loaded db")
    df = pd.read_table(files[0],header=None)

    toneList = (df[TONE_COLUMN]*10).astype(int).sort_values()
    out = pd.cut(toneList, bins = 60)
    counts = pd.value_counts(out)
    counts = counts.reindex(out.cat.categories)
    tones = []
    for interval in counts._index:
        tones.append([float(interval.left),int(counts[interval])])
    tones = json.dumps(tones)
    db['toneHistData'] = tones

    counts = df[QUADS_COLUMN].value_counts()
    print(counts)
    counts = [counts[i] if i in counts._index else 0 for i in range(1,5)]
    print(counts)
    quads = []
    quads.append({'desc': 'e.g. agreement on policy', 'name':'Verbal Cooperation','y':int(counts[0])})
    quads.append({'desc': 'e.g. a trade deal', 'name':'Material Cooperation','y':int(counts[1])})
    quads.append({'desc': 'e.g. disagreement on policy','name':'Verbal Conflict','y':int(counts[2])})
    quads.append({'desc': 'e.g. a research war','name':'Material Conflict','y':int(counts[3])})
    db['quadPiData'] = json.dumps(quads)
    db['lastupdate'] = calendar.timegm(time.gmtime())

    urls = df.drop_duplicates(subset=60).sort_values(TONE_COLUMN)[60]
    listitems = []
    listitems.append("<b>Most Negative</b>")
    listitems.extend(["<a href=" + item + ">" + item + "</a>" for item in urls.iloc[0:10].tolist()])
    listitems.append("<b>Most Positive</b>")
    listitems.extend(["<a href=" + item + ">" + item + "</a>" for item in urls.iloc[-11:-1].tolist()])
    listitems.append("updated: " + datetime.datetime.now().strftime("%m/%d %H:%M:%S"))
    db["toneListData"] = json.dumps(listitems)

@app.route("/")
def root():
    db = flask_shelve.get_shelve('c')
    lastupdated = 0 if not 'lastupdate' in db.keys() else int(db['lastupdate'])
    timedelta = calendar.timegm(time.gmtime()) - lastupdated
    print(timedelta)
    if (timedelta>60*4):
        print("updating GDELT data")
        processGdeltData()
    return app.send_static_file('index.html')

@app.route("/api/<panelName>")
@crossdomain(origin='*')
def panelFeedData(panelName):
    print("getting panel thing")
    db = flask_shelve.get_shelve('c')


    data = None
    data = db[panelName]
    response = app.response_class(
        response=data,
        status=200,
        mimetype='application/json'
    )
    return response

    if panelName == "toneHistogram":
        pass
    if panelName == "mapData":
        pass
    if panelName == "extremeTones":
        pass
    if panelName == "quadClassPiChart":
        pass

@app.route("/api/update")
@crossdomain(origin='*')
def updateCSVs():
    processGdeltData()

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=9000)



#PROCESSING STEP GOES HERE

#MAKE A FUNCTION TO EXPOSE STUFF AS JSON

#REMEMBER, RADICAL SIMPLICITY. WE'RE NOT GOING FOR DATA EXPLORATION, WHAT ARE WE GOING FOR
