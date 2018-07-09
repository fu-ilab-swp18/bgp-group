import json
from datetime import datetime, timezone

from .dataTuples import Timeslot


def check_ipv4(ip):
    if len(ip) <= 4:
        return False
    else:
        if ip[1] is '.' or ip[2] is '.' or ip[3] is '.':
            return True

    return False


def get_push_timestamp(time, hours=[0, 8, 16, 24]):
        # get closest push
        for i in range(0, len(hours)):
            if hours[i + 1] > time.hour:
                break

        time = time.replace(hour=hours[i], minute=0, second=0, microsecond=0)

        return int(time.timestamp())


def get_settings(settings_json):
    with open('settings.json') as f:
        return json.load(f)

    return False


def get_timestamp_now(slot=5):
    dt = datetime.now(timezone.utc)
    for i in range(0, 60, slot):
        if (i) > dt.minute:
            break

    dt = dt.replace(minute=(i - slot), second=0, microsecond=0)
    return int(dt.timestamp())

def get_timeslot(timestamp=None, slot=5):
    if not timestamp:
        return None

    dt = datetime.fromtimestamp(timestamp, timezone.utc)

    for i in range(0, 60, slot):
        if (i) > dt.minute:
            break

    dt_start = dt.replace(minute=(i - slot), second=0, microsecond=0)
    dt_stop = dt.replace(minute=(i), second=0, microsecond=0)

    dt_now = datetime.now(timezone.utc)
    if dt_now < dt_stop:
        dt_stop = dt_now

    return Timeslot(int(dt_start.timestamp()), int(dt_stop.timestamp()))



def init_next_timestamp(start_timestamp, slot=0):
    start_timestamp += 3600  # added 1h to push (1h = 3600s)
    dt = datetime.now(timezone.utc)
    for i in range(0, 60, slot):
        if (i) > dt.minute:
            break

    dt = dt.replace(minute=(i - slot), second=0, microsecond=0)
    now_timestamp = int(dt.timestamp())
    if now_timestamp > start_timestamp:
        return start_timestamp
    else:
        return now_timestamp


def split_prefix(prefix):
    """ Transforms a string "127.0.0.1/48" into ('127.0.0.1', 48) """
    ip_network_tuple = tuple(prefix.split('/'))
    return (ip_network_tuple[0], int(ip_network_tuple[1]))
