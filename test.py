#!/usr/bin/env python

import math
import argparse

from mapclassMerge import *

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

print "--------------------------------"

print "generatelistx"
map.generatelist('x',sigmaFFS)
print "generatelisty"
map.generatelist('y',sigmaFFS)
print "generatelistpx"
map.generatelist('px',sigmaFFS)
print "generatelistpy"
map.generatelist('py',sigmaFFS)

print "------------------------------"
print "@comp fort.18, 5fort.18"
map2=Map(args.order,'5fort.18')
print map.comp(map2)

print "\n\n########## GaussianDelta ##########"

map=Map(args.order,file,True)
print "sigmax=",sqrt(map.sigma('x',sigmaFFS)),";"
print "sigmay=",sqrt(map.sigma('y',sigmaFFS)),";"
print "sigmapx=",sqrt(map.sigma('px',sigmaFFS)),";"
print "sigmapy=",sqrt(map.sigma('py',sigmaFFS)),";"

print "--------------------------------"

print "generatelistx"
map.generatelist('x',sigmaFFS)
print "generatelisty"
map.generatelist('y',sigmaFFS)
print "generatelistpx"
map.generatelist('px',sigmaFFS)
print "generatelistpy"
map.generatelist('py',sigmaFFS)

print "------------------------------"
print "@comp fort.18, 5fort.18"
map2=Map(args.order,'5fort.18',True)
print map.comp(map2)
