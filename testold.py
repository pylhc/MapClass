#!/usr/bin/env python

from math import *
import argparse
import sys

from mapclass import Map
from mapclassGaussianDelta25 import Map as MapD

parser = argparse.ArgumentParser(description='Tester for MapClass')
parser.add_argument('-o', help='Run the test at a given order',
                    action='store', type=int, dest='order', default=6)
args = parser.parse_args()

betx=66.14532014
bety=17.92472388
gamma=3e6
ex=68e-8
ey=2e-8
sigmaFFS=[sqrt(ex*betx/gamma), sqrt(ex/betx/gamma), sqrt(ey*bety/gamma), sqrt(ey/bety/gamma), 0.01]

file='fort.18'
map=Map(args.order,file)
print "sigmax=",sqrt(map.sigma('x',sigmaFFS)),";"
print "sigmay=",sqrt(map.sigma('y',sigmaFFS)),";"
print "sigmapx=",sqrt(map.sigma('px',sigmaFFS)),";"
print "sigmapy=",sqrt(map.sigma('py',sigmaFFS)),";"
print "offsetx=",map.offset('x',sigmaFFS),";"
print "offsety=",map.offset('y',sigmaFFS),";"
print "offsetpx=",map.offset('px',sigmaFFS),";"
print "offsetpy=",map.offset('py',sigmaFFS),";"

print "\n\n########## GaussianDelta ##########"

map=MapD(args.order,file)
print "sigmax=",sqrt(map.sigma('x',sigmaFFS)),";"
print "sigmay=",sqrt(map.sigma('y',sigmaFFS)),";"
print "sigmapx=",sqrt(map.sigma('px',sigmaFFS)),";"
print "sigmapy=",sqrt(map.sigma('py',sigmaFFS)),";"
print "offsetx=",map.offset('x',sigmaFFS),";"
print "offsety=",map.offset('y',sigmaFFS),";"
print "offsetpx=",map.offset('px',sigmaFFS),";"
print "offsetpy=",map.offset('py',sigmaFFS),";"
