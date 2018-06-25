class LocalRecord(object):
    """docstring for OwnRecord"""
    def __init__(self, collector, time, elem):
        self.collector = collector
        self.elem = elem
        self.status = "valid"
        self.time = time
        self.next = 0

    def get_next_elem(self):
        if self.next == 0:
            self.next = 1
            return self.elem
        else:
            return False

class LocalElement(object):
    def __init__(self, the_type, peer_asn, peer_address, fields):
        self.type = the_type
        self.peer_asn = peer_asn
        self.peer_address = peer_address
        self.fields = fields

class LocalStream(object):
    """docstring for OwnStream"""
    def __init__(self, path):
        self.f = open(path)

    def __del__(self):
        self.f.close()

    def start(self):
        pass

    def get_next_record(self):
        line = self.f.readline()

        if not line:
            return False

        record = line.split('|')

        elem = LocalElement('D', 0, 0, {})

        if record[1] == 'R' or record[1] == 'U':

            elem = LocalElement(
                the_type=record[1],
                peer_asn=record[5],
                peer_address=record[6],
                fields = {
                    'as-path': record[9],
                    'prefix': record[7]
                }
            )

        elif record[1] == 'W':
            pass

        return LocalRecord(collector=record[4], time=record[2], elem=elem)
