#!/usr/bin/env python
import sys

fp=open('filename')
sys.stdout = open('mega1.txt', 'w')

for line in fp:
    fields = line.strip().split()
    chrm = fields[0]
    pos = int(fields[1])
    id1    = fields[2]
    if pos in range(149601, 1149601):
        print line
