from collections import namedtuple

VantagePointMeta = namedtuple('VantagePointMeta', ['vpid', 'rcid', 'timestamp', 'valid', 'invalid', 'unkonwn'])

RouteCollectorMeta = namedtuple('RouteCollectorMeta', ['rcid', 'timestamp', 'rcloc', 'peers', 'prefix4', 'prefix6'])

Route = namedtuple('RouteTable', ['vpid', 'rcid', 'prefix', 'isIPv4', 'type'])

Timeslot = namedtuple('Timeslot', ['start', 'stop'])
