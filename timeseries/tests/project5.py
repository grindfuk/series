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

    def test_that_timeseriesinterface_is_abc(self):
        self.assertIsInstance(TimeSeriesInterface, ABCMeta)

    def test_class_hierachy_of_timeseries(self):
        class_history= inspect.getmro(TimeSeries)
        self.assertTupleEqual(
            class_history,
            (TimeSeries, SizedContainerTimeSeriesInterface, TimeSeriesInterface, object)
        )

    def test_class_hierachy_of_array_timeseries(self):
        class_history= inspect.getmro(ArrayTimeSeries)
        self.assertTupleEqual(
            class_history,
            (ArrayTimeSeries, SizedContainerTimeSeriesInterface, TimeSeriesInterface, object)
        )

    def test_class_hierachy_of_simulated_timeseries(self):
        class_history= inspect.getmro(SimulatedTimeSeries)
        self.assertTupleEqual(
            class_history,
            (SimulatedTimeSeries, StreamTimeSeriesInterface, TimeSeriesInterface, object)
        )

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

