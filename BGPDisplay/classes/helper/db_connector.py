import psycopg2 as pg
import os.path


class PostgresConnector(object):
    """Connects to a Database and offers the methods to
    update the predefined tables"""

    def __init__(self, db):
        self.conn = pg.connect(
            dbname=db["name"], user=db["user"], host=db["host"], password=db["password"]
        )

    def __del__(self):
        self.conn.close()

    def update_vp_meta(self, vp_meta):

        cur = self.conn.cursor()
        dirname = os.path.dirname(__file__)
        spl_path = os.path.join(dirname, '..', 'sql', 'postgres', 'update_vp_meta.sql')

        with open(spl_path, 'r') as f:
            statements = f.read().split(';')

            for rc, peers in vp_meta.items():
                for vp, peer in peers.items():
                    cur.execute(statements[0], peer)

        self.conn.commit()
        cur.close()

    def update_rc_meta(self, rc_meta):

        cur = self.conn.cursor()
        dirname = os.path.dirname(__file__)
        spl_path = os.path.join(dirname, '..', 'sql', 'postgres', 'update_rc_meta.sql')

        with open(spl_path, 'r') as f:
            statements = f.read().split(';')

            for rc, meta in rc_meta.items():
                    cur.execute(statements[0], meta)

        self.conn.commit()
        cur.close()
