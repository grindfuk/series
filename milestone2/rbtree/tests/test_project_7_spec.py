import unittest
import numpy as np
from student_solutions import repo

SCORE = 0
TOTAL_SCORE = 0

def tsmaker(m, s, j):
    t = np.arange(0.0, 1.0, 0.01)
    v = norm.pdf(t, m, s) + j*np.random.randn(100)
    return ts.TimeSeries(t, v)

def fixed_timeseries(times, values, timeseries_cls):
    try:
        return timeseries_cls(times=list(times), values=list(values))
    except:
        return timeseries_cls(list(times), list(values))

def random_timeseries(amplitude, timeseries_cls):
    times = np.arange(0.0, 1.0, 0.01)
    values = amplitude*np.random.random(100)
    assert(len(times) == len(values))
    try:
        return timeseries_cls(times=list(times), values=list(values))
    except:
        return timeseries_cls(list(times), list(values))


class MainTest(unittest.TestCase):

    group = None

    def setUp(self):
        global StorageManagerInterface
        global SMTimeSeries
        global TimeSeries
        global stand
        global ccor
        global kernel_corr
        StorageManagerInterface = repo[self.group]["StorageManagerInterface"]
        SMTimeSeries = repo[self.group]["SMTimeSeries"]
        TimeSeries = repo[self.group]["TimeSeries"]
        ccor = repo[self.group]['ccor']
        stand = repo[self.group]['stand']
        kernel_corr = repo[self.group]['kernel_corr']

    def test_storage_manager_interface_has_abstract_methods(self):
        """  Test for the required abstract methods
        Ref:
        Create a new StorageManagerInterface which has the abstract methods:
        * store
        * size
        * get
        """
        for method in ["store", "size", "get"]:
            cls_attr = getattr(StorageManagerInterface, method)
            self.assertTrue(callable(cls_attr))

    def test_smtimeseries_has_method_from_db(self):
        for method in ["from_db"]:
            cls_attr = getattr(SMTimeSeries, method)
            self.assertTrue(callable(cls_attr))
        print(self.group)
        self.assertTrue(True)

    def test_stand_with_random_distribution(self):
        """ Optional: This method can be done in one go as a timeseries classmethod. """
        ts = random_timeseries(2, TimeSeries)
        ts_standardized = stand(ts, ts.mean(), ts.std())
        self.assertIsInstance(ts_standardized, TimeSeries)
        self.assertAlmostEqual(0, ts_standardized.mean())
        self.assertAlmostEqual(1, ts_standardized.std())

    def test_stand_with_bad_input(self):
        ts = random_timeseries(2, TimeSeries)
        with self.assertRaises(Exception):
            ts_standardized = stand(ts, None, None)
        with self.assertRaises(Exception):
            ts_standardized = stand(1, 1, 1)
        with self.assertRaises(Exception):
            ts_standardized = stand('1','1','1')

    def test_ccorr_with_random_distributions(self):
        ts1 = random_timeseries(2, TimeSeries)
        ts2 = random_timeseries(4, TimeSeries)
        cross_correlation = ccor(
            stand(ts1, ts1.mean(), ts1.std()),
            stand(ts2, ts2.mean(), ts2.std()))
        print(cross_correlation)
        self.assertGreater(cross_correlation, 0)
        self.assertLess(cross_correlation, 1)
