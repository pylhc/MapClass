#!/usr/bin/env python

import math
import copy
import sys
from os import system
#from simplex import Simplex
from mapclass25 import *


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
