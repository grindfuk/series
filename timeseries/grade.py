import os
# os.chdir(path)
# Combined tests for all labs to run on Milestone I

import unittest
import numpy as np

print('running')

# for computing hamming distance
import distance

import os

# list of tuples
# (Lab, testinfo, points)
scores = []

__unittest = True

import sys
import shutil

# importing should also scored...


import_fail = False

import timeseries
import timeseries.TimeSeries as TimeSeries
# this is correct
try:
  import timeseries.TimeSeries as TimeSeries
  #scores.append( ('General', 'correct package', 5))
except:
  print('TimeSeries import error!')
  import_fail = True

try:
  # import lazy decorator
  from timeseries import lazy
except:
  print('lazy could not be imported')


# fix for team: cs207-project
try:
  from TimeSeries import TimeSeries
  from lazy import lazy
except:
  pass

