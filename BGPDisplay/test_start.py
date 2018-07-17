from classes.helper.db_connector import PostgresConnector as DBC


db = {
    'name': 'bgp',
    'user': 'bgp',
    'password': '',
    'host': "pg.a0s.de"
}

print(db)
dbc = DBC(db)

dbc.update_vp_meta(None)
