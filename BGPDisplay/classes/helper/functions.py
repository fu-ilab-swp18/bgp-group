import json
from datetime import datetime, timezone


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


def get_timestamp_now(slot=0):
    dt = datetime.now(timezone.utc)
    for i in range(0, 60, slot):
        if (i) > dt.minute:
            break

    dt = dt.replace(minute=(i - slot), second=0, microsecond=0)
    return int(dt.timestamp())


def split_prefix(prefix):
    """ Transforms a string "127.0.0.1/48" into ('127.0.0.1', 48) """
    ip_network_tuple = tuple(prefix.split('/'))
    return (ip_network_tuple[0], int(ip_network_tuple[1]))
