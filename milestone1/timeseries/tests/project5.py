import inspect
import unittest
from abc import ABCMeta
from timeseries import (
    TimeSeriesInterface,
    StreamTimeSeriesInterface,
    SizedContainerTimeSeriesInterface,
    SimulatedTimeSeries,
    ArrayTimeSeries,
    TimeSeries
)


class TestProject5(unittest.TestCase):
    """ Tests the module 'Time Series Interface and Implementation. """

    def test_extra_credit_mean_of_sizedcontainertimeseriesinterface(self):
        self.assertTrue(
            hasattr(TimeSeries, "mean")
            or
            hasattr(SizedContainerTimeSeriesInterface, "mean")
            or
            (hasattr(TimeSeries, "mean") and hasattr(ArrayTimeSeries, "mean"))
        )

    def test_extra_credit_std_of_sizedcontainertimeseriesinterface(self):
        self.assertTrue(
            hasattr(TimeSeries, "std")
            or
            hasattr(SizedContainerTimeSeriesInterface, "std")
            or
            (hasattr(TimeSeries, "std") and hasattr(ArrayTimeSeries, "std"))
        )

    def test_extra_credit_online_mean_of_streamtimeseries(self):
        self.assertTrue(hasattr(StreamTimeSeriesInterface, "online_mean"))

    def test_extra_credit_std_of_sizedcontainertimeseries(self):
        self.assertTrue(hasattr(StreamTimeSeriesInterface, "online_std"))

