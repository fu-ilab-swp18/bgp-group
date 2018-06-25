import time

# Open the file with read only permit
f = open('/Users/mx/Projects/Uni/bgp-group/bgp_dump.txt')
# use readline() to read the first line

t = time.time()
line = f.readline()
while line:
    line = f.readline()
f.close()

print('Elapsed Time:', time.time() - t )
