import inspect
import unittest
import numpy as np
from abc import ABCMeta
from timeseries import (
    TimeSeriesInterface,
    StreamTimeSeriesInterface,
    SizedContainerTimeSeriesInterface,
    SimulatedTimeSeries,
    ArrayTimeSeries,
    TimeSeries
)


class TestProject4(unittest.TestCase):
    """ Tests the accumulated expectations from the
        module 'Dunders and Operator Overloading on Time Series' """

    def setUp(self):
        times = list(range(10))
        values = [1]*10
        self.scores = []
        self.list_timeseries = TimeSeries(times, values)  # list based
        self.array_timeseries = ArrayTimeSeries(times, values)

    def test_attributes_exist_in_list_timeseries(self):
        expected_attributes = ['_times', '_values']
        self.assertListEqual(sorted(expected_attributes), sorted(vars(self.list_timeseries)))

    def test_attributes_exist_in_array_timeseries(self):
        expected_attributes = ['_times', '_values']
        self.assertListEqual(expected_attributes, list(vars(self.array_timeseries)))

    def _build_missing_methods(self, timeseries):
        expected_methods = [
            "__getitem__",
            "__setitem__",
            "__contains__",
            "__iter__",
            "values",
            "itervalues",
            "times",
            "itertimes",
            "items",
            "iteritems",
            "__len__",
            "__repr__",
            "mean",
            "median",
            "__abs__",
            "__bool__",
            "__neg__",
            "__pos__",
            "__eq__",
            "__add__",
            "__sub__",
            "__mul__"
        ]
        missing_methods = []
        for method in expected_methods:
            found_method = getattr(timeseries, method, None)
            if found_method:
                # XXX: This should throw by definition of method
                self.assertTrue(callable(found_method))
            else:
                missing_methods.append(method)
        return missing_methods

    def test_accumulated_methods_exist_in_list_timeseries(self):
        # XXX: Do this before running just so we know
        missing_methods = self._build_missing_methods(self.list_timeseries)
        self.assertListEqual(
            missing_methods, [],
            msg="The TimeSeries class does not contain the methods: {}".format(missing_methods))

    def test_accumulated_methods_exist_in_array_timeseries(self):
        # XXX: Do this before running just so we know
        missing_methods = self._build_missing_methods(self.array_timeseries)
        self.assertListEqual(
            missing_methods, [],
            msg="The TimeSeries class does not contain the methods: {}".format(missing_methods))

    def test_addition_with_valid_addition_expressions(self):
        # Previously testAdd1
        lhs = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
        rhs = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
        result = TimeSeries([1, 2, 3, 4], [0.2, 0.4, 0.6, 0.8])
        self.assertTrue(result == (lhs + rhs))
        self.assertTrue((rhs + lhs) == result)
        self.scores.append( ('#ar Lab15', 'add base', 1))

    def test_addition_with_invalid_types_should_throw_type_error(self):
        # Previously testAdd2
        expr = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])

        with self.assertRaises(TypeError):
            expr + 'Hello'
        with self.assertRaises(TypeError):
            'Hello' + expr
        with self.assertRaises(TypeError):
            expr + 1
        with self.assertRaises(TypeError):
            1 + expr
        with self.assertRaises(TypeError):
            expr + {}
        with self.assertRaises(TypeError):
            {} + expr

        self.scores.append( ('#ar Lab15', 'add adv', 3))

    def test_addition_with_not_implemented_types_should_throw_not_implemented_error(self):
        # Previously testAdd3
        expr = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])

        with self.assertRaises(NotImplementedError):
            expr + [1, 2, 3, 4]
        with self.assertRaises(NotImplementedError):
            [1, 2, 3, 4] + expr
        with self.assertRaises(NotImplementedError):
            expr + np.array([1, 2, 3, 4])
        with self.assertRaises(NotImplementedError):
            np.array([1, 2, 3, 4]) + expr

        self.scores.append( ('#ar Lab15', 'add not impl', 0))

    # XXX: Need to skip maybe
    @unittest.skip("This is not in the current course")
    def test_addition_with_integer_should_add_directly_to_values(self):
        # previously testAdd4 and testAdd6
        base_values = [0.1, 0.2, 0.3, 0.4]
        expr = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])

        for factor in [-2, -0.5, 0, 0.5, 2]:
            updated_values = [(factor + i) for i in base_values]
            result = TimeSeries([1, 2, 3, 4], updated_values)
            self.assertTrue(result == (expr + factor))
            self.assertTrue((expr + factor) == result)

        self.scores.append(('#ar Lab15', 'add + int val', 2))
        self.scores.append(('#ar Lab15', 'add + float val', 1))

    def test_addition_with_different_length_timeseries_should_throw_value_error(self):
        # previously testAdd7
        ts_a = TimeSeries([1, 2, 3, 4, 5], [0.1, 0.2, 0.3, 0.4, 0.5])
        ts_b = TimeSeries([1, 2, 3, 4], [0.2, 0.4, 0.6, 0.8])
        ts_c = TimeSeries([1, 2, 3], [0.5, 0.2, 0.9])
        ts_d = TimeSeries([1, 2], [1.1, 1.2])
        ts_e = TimeSeries([1], [0.1])
        ts_f = TimeSeries([], [])

        ts_all = [ts_a, ts_b, ts_c, ts_d, ts_e, ts_f]
        for i, ts_1 in enumerate(ts_all):
            for j, ts_2 in enumerate(ts_all):
                if i == j:
                    continue
                with self.assertRaises(ValueError):
                    ts_1 + ts_2
                with self.assertRaises(ValueError):
                    ts_2 + ts_1

        self.scores.append(('#ar Lab15', 'add + val err', 2))

    def testSub3(self):
        t_a = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
        t_b = TimeSeries([1, 2, 3, 4], np.array([0.1, 0.2, 0.3, 0.4]))
        t_c = TimeSeries([1, 2, 3, 4], [0.0, 0.0, 0.0, 0.0])
        t_d = TimeSeries([1, 2, 3, 4], [-0.9, -0.8, -0.7, -0.6])
        t_e = TimeSeries([1, 2, 3], [0.5, 0.2, 0.9])
        t_f = TimeSeries([], [])
        with self.assertRaises(NotImplementedError):
            t_a - [1, 2, 3, 4]
        with self.assertRaises(NotImplementedError):
            t_a - np.array([1, 2, 3, 4])

        scores.append(('#ar Lab15', 'sub not impl', 1))

    # def testSub4(self):
    #     t_a = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
    #     t_b = TimeSeries([1, 2, 3, 4], np.array([0.1, 0.2, 0.3, 0.4]))
    #     t_c = TimeSeries([1, 2, 3, 4], [0.0, 0.0, 0.0, 0.0])
    #     t_d = TimeSeries([1, 2, 3, 4], [-0.9, -0.8, -0.7, -0.6])
    #     t_e = TimeSeries([1, 2, 3], [0.5, 0.2, 0.9])
    #     t_f = TimeSeries([], [])

    #     val = 1
    #     val = int(val)
    #     self.assertTrue((t_a - val) == t_d)

    #     scores.append(('#ar Lab15', 'sub + int val', 2))

    # def testSub6(self):
    #     t_a = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
    #     t_b = TimeSeries([1, 2, 3, 4], np.array([0.1, 0.2, 0.3, 0.4]))
    #     t_c = TimeSeries([1, 2, 3, 4], [0.0, 0.0, 0.0, 0.0])
    #     t_d = TimeSeries([1, 2, 3, 4], [-0.9, -0.8, -0.7, -0.6])
    #     t_e = TimeSeries([1, 2, 3], [0.5, 0.2, 0.9])
    #     t_f = TimeSeries([], [])
    #     val = 1
    #     val = float(val)
    #     self.assertTrue((t_a - val) == t_d)

    #     scores.append(('#ar Lab15', 'sub + float val', 1))

    # def testSub7(self):
    #     t_a = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
    #     t_b = TimeSeries([1, 2, 3, 4], np.array([0.1, 0.2, 0.3, 0.4]))
    #     t_c = TimeSeries([1, 2, 3, 4], [0.0, 0.0, 0.0, 0.0])
    #     t_d = TimeSeries([1, 2, 3, 4], [-0.9, -0.8, -0.7, -0.6])
        t_e = TimeSeries([1, 2, 3], [0.5, 0.2, 0.9])
        t_f = TimeSeries([], [])

        with self.assertRaises(ValueError):
            t_a - t_e
        with self.assertRaises(ValueError):
            t_a - t_f

        scores.append(('#ar Lab15', 'sub + val err', 2))