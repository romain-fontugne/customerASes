import sys
import numpy as np
from subprocess import Popen, PIPE
from collections import defaultdict
import glob

import networkx as nx
import radix


class bgpRead(object):

    def __init__(self):
        self.customers = set()


    def read_rib(self, files, provider):
        """Read RIB files and populate the routing table and AS graph.
        """

        for f in glob.glob(files):
            p1 = Popen(["bgpdump", "-m", "-v", "-t", "change", f], stdout=PIPE, bufsize=-1)

            for line in p1.stdout: 
                res = line.split('|',15)
                zTd, zDt, zS, zOrig, zAS, zPfx, sPath, zPro, zOr, z0, z1, z2, z3, z4, z5 = res
                
                if zPfx == "0.0.0.0/0" or zAS == provider:
                    continue

                path = sPath.split(" ")
                try:
                    pindex = path.index(provider)
                except ValueError:
                    pindex = -1
                    pass

                if pindex != -1:
                    for asn in path[pindex:]:
                        self.customers.add(asn)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: %s providerASN RIBfile"
        sys.exit()
    provider = sys.argv[1]
    rib = sys.argv[2]

    br = bgpRead()
    br.read_rib(rib, provider)

    print br.customers

