#! /usr/bin/env python
import sys

# by default 200 MB
size=200

try:
    size=int(sys.argv[1])
except IndexError:
    pass

size *= 1024*1024

accum = 0
# create a 200MB file
with open('output', 'wb') as f:
    while accum < size:
	line = 'a' * 1024 * 1024 * 10
        accum += len(line)
        f.write(line)

