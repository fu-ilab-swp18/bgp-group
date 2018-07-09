from collections import defaultdict
from flask import Flask, g, jsonify
import os

from classes.helper.db_connector import PostgresConnector as DBConnector
from classes.helper.functions import *
from classes.helper.dataTuples import VantagePointData

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'A Query Generator will be here'


@app.route('/rc_data/<rcs>/latest')
@app.route('/rc_data/<rcs>/<int:timestamp>')
def get_rc_data(rcs, timestamp=None):
    rc_data = ()
    db = get_db()

    timeslot = get_timeslot(timestamp)

    rc_list = rcs.split(",")

    rc_data = db.get_rc_data(rc_list, timeslot)

    if not timestamp:
        timestamp = rc_data[0][1]
        timeslot = get_timeslot(timestamp)

    # build json from rc_data
    json_data = {
        "query": "/rc_data/{}/{}".format(rcs, timestamp),
        "timeslot": {"start": timeslot.start, "stop": timeslot.stop},
        "data": {}
    }

    for rc in rc_data:
        json_data['data'][rc[0]] = {
            "peers": rc[2],
            "prefix4": rc[3],
            "prefix6": rc[4],
        }

    return jsonify(json_data)


@app.route('/vp_data/<rcs>/all/latest')
@app.route('/vp_data/<rcs>/all/<int:timestamp>')
@app.route('/vp_data/<rcs>/<vps>/latest')
@app.route('/vp_data/<rcs>/<vps>/<int:timestamp>')
def get_vp_data(rcs, vps=None, timestamp=None):
    db = get_db()

    rc_list = rcs.split(",")
    vp_list = None
    if vps:
        vp_list = vps.split(",")

    timeslot = get_timeslot(timestamp)

    vp_data = db.get_vp_data(rc_list, vp_list, timeslot)

    if not timestamp:
        timestamp = vp_data[0][3]
        timeslot = get_timeslot(timestamp)

    vp_set = set()

    data = {}
    for rc in rc_list:
        data[rc] = defaultdict(dict)

    for vp in vp_data:
        cur = VantagePointData._make(vp)
        as_name = 'AS' + str(cur.vpid)
        vp_set.add(as_name)
        data[cur.rcid][as_name][cur.vpaddr] = {
            "valid": cur.valid,
            "unknown": cur.unknown,
            "invalid": cur.invalid
        }

    # vps = ','.join(list(vp_set))
    if not vps:
        vps = 'all'

    json_data = {
        "query": "/vp_data/{}/{}/{}".format(rcs, vps, timestamp),
        "timeslot": {"start": timeslot.start, "stop": timeslot.stop},
        "data": data
    }

    return jsonify(json_data)


def get_db():
    if 'db' not in g:
        settings = get_settings("../settings.json")
        settings["db"]["password"] = os.environ["PGPASS"]
        g.db = DBConnector(settings['db'])

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        del db
