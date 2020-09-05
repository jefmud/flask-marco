# main.py
from flask import (Flask, render_template, abort, redirect, request, url_for)
from gevent.pywsgi import WSGIServer
from forms import SpeciesQueryForm, GeneralQueryForm
import random
import config
import sys

app = Flask(__name__)
app.secret_key = 'jJKchjdofpow$Ru*d4s^28sMNe2'

####### databse
import pymongo
from pymongo import MongoClient
client = MongoClient("mongodb://localhost.org:27017")
db = client["ser"]
idents = db["idents"]
##############

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select')
def select():
    skipcount = random.randint(1, 50000)
    recs = idents.find({'mwePREDTOP':'species', 'mweCONFTOP': {'$gt':0.85} }).skip(skipcount).limit(15)
    return render_template('select.html',recs=recs)

@app.route('/species', methods=['GET','POST'])
def species_query():
    records_per_page = 15
    try:
        page = request.args.get('page',0)
        page = int(page)
    except:
        page = 0

    form = SpeciesQueryForm()
    if form.validate_on_submit():
        # process query
        query = {
            'mwePREDTOP':'species',
            'mweCONFTOP': {'$gte': form.detection_threshold.data},
            'mwsPREDTOP': form.species_select.data,
            'mwsCONFTOP': {'$gte': form.species_confidence.data}
        }
        recs = idents.find(query).skip(page * records_per_page).limit(records_per_page)
        return render_template('query_results.html', recs=recs, page=page)
    return render_template('species_query.html', form=form)
    
    def api_service(req):
    """a generic query interface"""
    query = {}

    # predict empty or species
    predict = request.args.get('predict','species')
    query['mwePREDTOP'] = predict

    # predict threshold on empty or species
    threshold = req.args.get('threshold', None)
    if threshold:
        try:
            query['mweCONFTOP'] = {'$gte': float(threshold)}
        except:
            pass

    # predict species
    species = req.args.get('species', 'all')
    if species.lower() != 'all':
        query['mwsPREDTOP'] = species

    # species model confidence
    confidence = req.args.get('confidence', None)
    if confidence:
        try:
            query['mwsCONFTOP'] = {'$gte': float(confidence)}
        except:
            pass

    # set season if needed
    season = req.args.get('season', None)
    if season:
        season = season.upper()
        if not 'SER_S' in season:
            season = 'SER_S' + season
        query['season'] = season

    # set start date if needed
    startdate = req.args.get('start',None)
    if startdate:
        query['captureDATE'] = {'$gte': startdate}

    # set enddate if needed
    enddate = req.args.get('end',None)
    if enddate:
        query['captureDATE'] = {'$lte': enddate }

    # set skip if needed
    skip = req.args.get('skip', 0)
    if skip:
        try:
            skip = int(skip)
        except:
            skip = 0

    # set limit if needed
    limit = req.args.get('limit', 0)
    # catch non integers in limit
    try:
        limit = int(limit)
    except:
        limit = 0

    print(query)
    return []
    if limit > 0:
        recs = idents.find(query).skip(skip).limit(limit)
    else:
        recs = idents.find(query).skip(skip)
    return recs

@app.route('/api/html')
def api_vi():
    """return api results in HTML"""
    recs = api_service(request)
    return render_template('select.html', recs=recs)

@app.route('/view/<captureID>')
def view(captureID):
    dkey = {'captureID':captureID}
    rec = idents.find_one(dkey)
    if rec:
        nas_url = 'http://serengeti.wfunet.wfu.edu/'
        recurl = nas_url + rec['pathname']
        return render_template('view.html', rec=rec, recurl=recurl)
    return abort(404)

@app.route('/query')
def query_api():
    return render_template("query.html")

def arg_val(key, value=None):
    if not(key in sys.argv):
        return value
    loc = sys.argv.index(key)
    if loc >= 0:
        return sys.argv[loc+1]
    else:
        return value

def arg_exists(key):
    if key in sys.argv:
        return True
    return False

if __name__ == '__main__':
    PORT = 5000
    HOST = '127.0.0.1'

    PORT = int(arg_val('--port', PORT))
    HOST = arg_val('--host', HOST)
    if arg_exists('--deploy'):
        http_server = WSGIServer(('', PORT), app)
        print("GEvent Greenlet server running on port {}".format(PORT))
        http_server.serve_forever()
    else:
        app.run(port=PORT, host='0.0.0.0')
