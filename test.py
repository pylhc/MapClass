#!/usr/bin/env python

import math
import copy
import sys
from os import system
#from simplex import Simplex

#from mapclass25 import *
#from mapclass import *
from mapclassMerge import *


betx=66.14532014
bety=17.92472388
gamma=3e6
ex=68e-8
ey=2e-8
sigmaFFS=[sqrt(ex*betx/gamma), sqrt(ex/betx/gamma), sqrt(ey*bety/gamma), sqrt(ey/bety/gamma), 0.01]

file='fort.18'
map=Map(6,file)
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
map2=Map(6,'5fort.18')
map.comp(map2)
