import time

# Open the file with read only permit
f = open('/Users/mx/Projects/Uni/bgp-group/bgp_dump.txt')
# use readline() to read the first line
i = 0
t = time.time()
line = f.readline()
while line:
    record = line.split('|')

    # i += 1
    # if i % 10000 == 0:
    #     print(i)

    # if len(record) < 2:
    #     print(record)
    #     line = f.readline()
    #     continue


    if record[1] == 'R' or record[1] == 'A':
        elem = {
            'type': record[1],
            'peer_asn': record[5],
            'peer_address': record[6],
            'fields': {
                'as-path': record[9],
                'prefix': record[7]
            }
        }

        rec = {
            'collector': record[4]
        }

    line = f.readline()

    # r_type,e_type,time_stamp,r_proj,r_rc,asn,ip,prefix,ip2,as_path,origin_as,a,b = line.split("|")
f.close()

print('Elapsed Time:', time.time() - t )
