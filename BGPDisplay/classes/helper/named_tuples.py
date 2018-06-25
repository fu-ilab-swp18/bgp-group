from collections import namedtuple

VantagePointMeta = namedtuple('VantagePointMeta', ['vpid', 'rcid', 'timestamp', 'valid', 'unkonwn', 'invalid'])

RouteCollectorMeta = namedtuple('RouteCollectorMeta', ['rcid', 'timestamp', 'peers', 'prefix4', 'prefix6'])

Route = namedtuple('RouteTable', ['vpid', 'rcid', 'prefix', 'isIPv4', 'type'])
