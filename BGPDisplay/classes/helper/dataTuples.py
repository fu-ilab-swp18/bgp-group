from collections import namedtuple

VantagePointData = namedtuple('VantagePointData', ['vpid', 'vpaddr', 'rcid', 'timestamp', 'valid', 'unknown', 'invalid'])

RouteCollectorMeta = namedtuple('RouteCollectorMeta', ['rcid', 'timestamp', 'rcloc', 'peers', 'prefix4', 'prefix6'])

Route = namedtuple('RouteTable', ['vpid', 'rcid', 'prefix', 'isIPv4', 'type'])

Timeslot = namedtuple('Timeslot', ['start', 'stop'])
