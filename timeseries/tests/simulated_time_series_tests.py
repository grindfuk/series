import inspect
import unittest
from abc import ABCMeta
from timeseries import (
    StreamTimeSeriesInterface,
)
from timeseries.SimulatedTimeSeries import SimulatedTimeSeries
from itertools import count
from random import normalvariate, random
import logging

import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)
logging.basicConfig(level=logging.DEBUG)

def make_data(m, stop=None):
    for _ in count():
        if stop and _ > stop:
            break
        yield 1.0e09 + normalvariate(0, m * random())

def make_ones(x):
    while True:
        yield 1

def make_tuples(counter={}):
    if 'n' not in counter:
        counter['n'] = 0
    while True:
        yield (counter['n'], 2)
        counter['n'] += 1

class TestSimulatedTimeSeries(unittest.TestCase):

    def test_simulated_timeseries_initialization(self):
        """ Use make_data as a generator"""
        # Generator must be pre-primed
        generator = make_data(1, stop=None)
        ts = SimulatedTimeSeries(generator)
        print(ts.produce(2))
        logging.info(list(ts.produce(2)))

    def test_simulated_timeseries_produce_chunk(self):
        """ Test that make_ones returns the right number of chunks. """
        generator = make_ones(1)
        ts = SimulatedTimeSeries(generator)
        values = list(ts.produce(2))
        self.assertEqual(values, [1, 1])

    def test_simulated_timeseries_produce_tuple_chunks(self):
        """ Test that the timeseries is generated correctly with the right number of chunks. """
        generator = make_tuples(1)
        ts = SimulatedTimeSeries(generator)
        values = list(ts.produce(2))
        self.assertEqual(values, [1, 1])

