from datetime import datetime, timezone
from flask import Flask, g, jsonify
import os

from classes.helper.db_connector import PostgresConnector as DBConnector
from classes.helper.functions import *
app = Flask(__name__)

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


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
