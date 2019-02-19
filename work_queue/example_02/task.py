#! /usr/bin/env python

# create a 200MB file
with open('output', 'wb') as f:
    for i in range(0,20):
        line = 'a' * 1024 * 1024 * 10
        f.write(line)


