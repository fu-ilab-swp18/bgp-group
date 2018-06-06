import sqlite3


class SQLiteConnector(object):
    """
    inspired by https://www.dataquest.io/blog/data-pipelines-tutorial/
    """

    def __init__(self, path_to_db="bgp.db", read_only=True):
        if read_only:
            self.connection = sqlite3.connect(
                'file:' + path_to_db + '?mode=ro', uri=True)
        else:
            self.connection = sqlite3.connect(path_to_db)
            self.init_db()

    def __del__(self):
        self.connection.close()

    def init_db(self):
        """Creates all the tables needed"""
        for statement in file('../sql/sqlite/create_tables.sql').read().split(';'):
            self.cur.execute(statement)

    def update_vantage_point_meta(self, vp_tuple):
        pass

    def update_route_collector_meta(self, vp_tuple):
        pass

    def bgp_reset(self):
        """Every 2 or 8 hours we get a hard reset to get on the current state"""
        pass

    # def get_records(self, timestamp):
    #     """Get all younger than timestamp"""
    #     cur = self.connection.cursor()
    #     cur.execute(
    #         "SELECT remote_addr,time_local FROM logs WHERE created > ?", [time_obj])
    #     resp = cur.fetchall()
    #     return resp
