# Combined tests for Projects 1-5 to run on Milestone I

import re
import inspect
import numbers
import logging
import unittest
import numpy as np
from abc import ABCMeta

# for computing hamming distance
import distance

# This is a preliminary format for Automated Scoring
# (Lab, testinfo, points)
scores = []
total_scores = 0

# Note:
# importing does not need to be scored since Project 5 is so diverse

from timeseries.TimeSeries import TimeSeries
from timeseries.ArrayTimeSeries import ArrayTimeSeries
try:
    from timeseries.SimulatedTimeSeries import SimulatedTimeSeries
except:
    print('SimulatedTimeSeries could not be imported')
    exit(1)
try:
    from timeseries.TimeSeriesInterface import TimeSeriesInterface
except:
    print('SimulatedTimeSeries could not be imported')
    exit(1)
try:
    from timeseries.StreamTimeSeriesInterface import StreamTimeSeriesInterface
except:
    print('SimulatedTimeSeries could not be imported')
    exit(1)
try:
    from timeseries.SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
except:
    print('SimulatedTimeSeries could not be imported')
    exit(1)
try:
    from timeseries import lazy
except:
    print('lazy could not be imported')
    exit(1)


def zero_generator():
    while True:
        yield 0


ALL_CONCRETE_CLASSES = [('ts', TimeSeries), ('ats', ArrayTimeSeries), ('sts', SimulatedTimeSeries)]
SIZED_CONCRETE_CLASSES = ALL_CONCRETE_CLASSES[:2]


def score(number):
    def test_check(f):
        def test_deco(self, *args, **kwargs):
            global total_scores
            total_scores += number
            return f(self, *args, **kwargs)
        test_deco.__name__ = f.__name__
        return test_deco
    return test_check

class TestTSBasics(unittest.TestCase):

    @score(3)
    def test_valid_init(self):
        """ All the sized timeseries __init__ constructors should take
            any sequence-like thing. Unsized should take a generator.
        """
        # NOTE: Depending on intepretation, this might be safe
        ts = TimeSeries([0], [0])
        ats = ArrayTimeSeries([0], [0])
        sts = SimulatedTimeSeries(zero_generator)
        scores.append(('#ts', 'init valid ts, ats, sts', 3))

    @score(2)
    def test_invalid_init_with_different_length_inputs(self):
        """ Different lengths should not be allowed for fixed timeseries. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            # NOTE: Depending on intepretation, this might be safe
            with self.assertRaises((Exception, AssertionError, ValueError)):
                ts_class([1.0, 2], [])
            with self.assertRaises((Exception, AssertionError, ValueError)):
                ts_class([], [1.])
            scores.append(('#ts', 'init %s with different len (times, values)' % (i), 1))

    @score(2)
    def test_invalid_init_with_empty_input(self):
        """ Should fail on empty input ie. ts(). Exception is not given by project SPEC. """
        for i, ts_class in ALL_CONCRETE_CLASSES:
            with self.assertRaises(Exception):
                ts_class()
            scores.append(('#ts', 'init %s with empty input' % (i), 1))

    @score(2)
    def test_invalid_init_with_number_input(self):
        """ Should fail on number input ie. ts(42). Exception is not given by project SPEC. """
        for i, ts_class in ALL_CONCRETE_CLASSES:
            try:
                with self.assertRaises(Exception):
                    ts_class(42)
                with self.assertRaises(Exception):
                    ts_class(42, 42)
                with self.assertRaises(Exception):
                    ts_class(42.1)
                with self.assertRaises(Exception):
                    ts_class(42.1, 42.1)
                with self.assertRaises(Exception):
                    ts_class(4+2j)
                with self.assertRaises(Exception):
                    ts_class(4+2j, 4+2j)
                scores.append(('#ts', 'init %s with number input [42, 42.1, 4+2j]' % (i), 1))
            except Exception as e:
                raise Exception('Exception not raised on %s' % (ts_class)) from e

    @score(2)
    def test_valid_length(self):
        """ Should return valid sizes on list, even the empty one """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            cases = [([], 0),
                     ([1], 1),
                     ([1,2,3, 4, 5], 5)
                    ]
            for case in cases:
                try:
                    self.assertEqual(len(TimeSeries(case[0], case[0])), case[1])
                    self.assertEqual(TimeSeries(case[0], case[0]).__len__(), case[1])
                except Exception as e:
                    raise Exception('Failure with %s on case %s' % (i, case)) from e
            scores.append(('#ts', 'valid length returned with %s' % (i), 1))

    @score(2)
    def test_valid_getitem(self):
        """ Should return a tuple or list of time, value when using getitem with index """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1.5, 2.5, 3.5, 7.0], [0.1, 0.2, 0.3, 0.4])
            ts_value = ts[1]
            # The interface is not specified so we can accept any of these
            self.assertTrue(
                ts_value == 0.2 or
                ts_value == (2.5, 0.2) or
                ts_value == [2.5, 0.2]
            )
            scores.append(('#ts', '%s getitem returns the indexed time/value' % (i), 1))

    @score(2)
    def test_valid_getitem_with_negative_index(self):
        """ Should return a tuple or list of time, value when using getitem with negative index """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1.5, 2.5, 3.5, 7.0], [0.1, 0.2, 0.3, 0.4])
            ts_value = ts[-1]
            expected_ts_value = ts[3]
            self.assertEqual(ts_value, expected_ts_value)
            scores.append(('#ts', '%s getitem [-1] returns the indexed time/value' % (i), 1))

    @score(2)
    def test_invalid_getitem_with_non_integer_get_index(self):
        """ Should throw when using getitem with float, str index """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1.5, 2.5, 3.5, 7.0], [0.1, 0.2, 0.3, 0.4])
            with self.assertRaises(Exception):
                ts[2.0]
            with self.assertRaises(Exception):
                ts['2']
            scores.append(('#ts', '%s getitem [2.0, "2"] should error' % (i), 1))

    @score(2)
    def test_valid_setitem(self):
        """ Should update a tuple or list of time, value when using getitem with index """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1.5, 2.5, 3.5, 7.0], [0.1, 0.2, 0.3, 0.4])
            try:
                ts[0] = -0.9
            except:
                raise Exception('Could not setitem with %s' % ts_class)
            ts_value = ts[0]
            self.assertTrue(
                ts_value == -0.9 or
                ts_value == (1.5, -0.9) or
                ts_value == [1.5, -0.9]
                , '%s: Expected (1.5, -0.9) but got %s' % (i, str(ts_value)))
            scores.append(('#ts', '%s setitem updates the indexed time/value' % (i), 1))

    @score(2)
    def test_valid_setitem_with_negative_index(self):
        """ Should update a tuple or list of time, value when using getitem with negative index """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1.5, 2.5, 3.5, 7.0], [0.1, 0.2, 0.3, 0.4])
            try:
                ts[-1] = -0.9
            except:
                raise Exception('Could not setitem with %s' % ts_class)
            ts_value = ts[-1]
            expected_ts_value = ts[3]
            self.assertEqual(ts_value, expected_ts_value)
            scores.append(('#ts', '%s setitem updates the indexed time/value' % (i), 1))

    @score(2)
    def test_invalid_setitem_with_invalid_set_value(self):
        """ Should throw when trying to set with an invalid set value. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1.5, 2.5, 3.5, 7.0], [0.1, 0.2, 0.3, 0.4])
            with self.assertRaises(Exception):
                ts[0] = None
            with self.assertRaises(Exception):
                ts[0] = 'str'
            with self.assertRaises(Exception):
                ts[0] = ('str', 'str')
            # NOTE: This may be acceptable depending on the student's interface.
            with self.assertRaises(Exception):
                ts[0] = [1, 1]
            with self.assertRaises(Exception):
                ts[0] = (1, 1)
            scores.append(('#ts', '%s should throw on setitem[x]=[None, "str", ("str", "str"), ["str", "str"], [1,1], (1,1)]' % (i), 1))

    @score(2)
    def test_invalid_setitem_with_non_integer_set_index(self):
        """ Should throw when using setitem with float, str index """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1.5, 2.5, 3.5, 7.0], [0.1, 0.2, 0.3, 0.4])
            with self.assertRaises(Exception):
                ts[2.0] = 1
            with self.assertRaises(Exception):
                ts['2'] = 1
            scores.append(('#ts', '%s setitem[2.0, "2"]=(1,1) should error' % (i), 1))

    @score(3)
    def test_valid_nonempty_str_and_repr(self):
        """ All concrete classes should have a __str__() and __repr__(). Repeats are acceptable. """
        ts = TimeSeries([0], [0])
        ats = ArrayTimeSeries([0], [0])
        sts = SimulatedTimeSeries(zero_generator)
        for ts_class in [ts, ats, sts]:
            dunder_str = str(ts_class)
            dunder_repr = repr(ts_class)
            self.assertNotEqual(dunder_str, '')
            self.assertNotEqual(dunder_repr, '')
        scores.append(('#ts', 'all concrete classes should have non-empty str and repr', 1))

    @score(1)
    def test_valid_nondefault_str_and_repr(self):
        """ All concrete classes should have non-default __str__() and __repr__(). """
        ts = TimeSeries([0], [0])
        ats = ArrayTimeSeries([0], [0])
        sts = SimulatedTimeSeries(zero_generator)
        self.assertNotRegexpMatches('^<.*.TimeSeries object at .*>$', str(ts))
        self.assertNotRegexpMatches('^<.*.TimeSeries object at .*>$', repr(ts))
        self.assertNotRegexpMatches('^<.*.ArrayTimeSeries object at .*>$', str(ats))
        self.assertNotRegexpMatches('^<.*.ArrayTimeSeries object at .*>$', repr(ats))
        self.assertNotRegexpMatches('^<.*.SimulatedTimeSeries object at .*>$', str(sts))
        self.assertNotRegexpMatches('^<.*.SimulatedTimeSeries object at .*>$', repr(sts))
        scores.append(('#ts', 'all concrete classes should have non-default str and repr', 1))

    @score(2)
    def test_valid_contains_returns_true(self):
        """ All sized classes should return true when it contains a value. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1.5, 2.5, 3.5, 7.0], [0.1, 0.2, 0.3, 0.4])
            # NOTE: This interface might be different for groups since it isn't specified directly
            self.assertTrue(0.2 in ts)
            self.assertTrue(ts.__contains__(0.1))
            scores.append(('#ts', '%s should implement __contains__(value) == True' % i, 1))

    @score(2)
    def test_valid_contains_returns_false(self):
        """ All sized classes should return False when it does not contain a value. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1.5, 2.5, 3.5, 7.0], [0.1, 0.2, 0.3, 0.4])
            # NOTE: This interface might be different for groups since it isn't specified directly
            self.assertFalse(42 in ts)
            self.assertFalse(ts.__contains__(-10))
            scores.append(('#ts', '%s should implement __contains__(value) == False' % i, 1))

    @score(2)
    def test_contains_with_invalid_values(self):
        """ All sized classes should return False or throw exception when it does not contain a non-numeric value. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1.5, 2.5, 3.5, 7.0], [0.1, 0.2, 0.3, 0.4])
            try:
                self.assertFalse('Hello World!' in ts)
            except:
                # Any Exception is fine if that is the interface
                pass
            try: self.assertFalse([] in ts)
            except: pass
            try: self.assertFalse(None in ts)
            except: pass
            try: self.assertFalse(True in ts)
            except: pass
            try: self.assertFalse(False in ts)
            except: pass
            scores.append(('#ts', 'all sized concrete classes should implement something for __contains__(any type) == False', 1))

    @score(2)
    def test_iteration_over_values_in_sized_class(self):
        """ All sized classes should be iterable over the length of the time-series """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1.5, 2.5, 3.5, 7.0], [0.1, 0.2, 0.3, 0.4])
            expected_values = [0.1, 0.2, 0.3, 0.4]
            expected_length = 0
            for value in ts:
                # This was an earlier interface but it should be okay if they kept it
                if isinstance(value, (tuple, list)):
                    self.assertEqual(expected_values, value[1])
                elif isinstance(value, numbers.Number):
                    self.assertEqual(expected_values[expected_length], value)
                else:
                    raise Exception('Invalid Type')
                expected_length += 1
            self.assertEqual(expected_length, len(ts))
            scores.append(('#ts', '%s class should be iterable over the length' % i, 1))

    @score(2)
    def test_values_property_in_sized_class(self):
        """ All sized classes should have a fixed length values property """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            expected_values = [0.1, 0.2, 0.3, 0.4]
            ts = ts_class(expected_values, [0.1, 0.2, 0.3, 0.4])
            self.assertEqual(list(ts.values()), expected_values)
            scores.append(('#ts', '%s class should have valid values property' % i, 1))

    @score(2)
    def test_times_property_in_sized_class(self):
        """ All sized classes should have a fixed length times property """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            expected_times = [1.5, 2.5, 3.5, 7.0]
            ts = ts_class(expected_times, [0.1, 0.2, 0.3, 0.4])
            self.assertEqual(list(ts.times()), expected_times)
            scores.append(('#ts', '%s class should have valid times property' % i, 1))

    @score(2)
    def test_items_property_in_sized_class(self):
        """ All sized classes should have a fixed length items property """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1.5, 2.5, 3.5, 7.0], [0.1, 0.2, 0.3, 0.4])
            self.assertEqual(list(ts.items()), [(1.5, 0.1), (2.5, 0.2), (3.5, 0.3), (7.0, 0.4)])
            scores.append(('#ts', '%s class should have valid items property' % i, 1))

class TestTSInterpolation(unittest.TestCase):

    @score(2)
    def test_interpolation_with_simple_input(self):
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = TimeSeries([0, 5, 10], [1, 2, 3])
            ares = ts.interpolate([1])
            self.assertEqual(ares.values()[0], 1.2)
            self.assertEqual(ares.times()[0], 1)
            ares = ts.interpolate([2.5, 7.5])
            self.assertEqual(list(ares.values()), [1.5, 2.5])
            self.assertEqual(list(ares.times()), [2.5, 7.5])
            scores.append(('#ts', 'test interpol base', 3))

    @score(2)
    def test_interpolation_against_boundarys(self):
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = TimeSeries([0, 5, 10], [1, 2, 3])
            # Boundary conditions
            ares = ts.interpolate([-100, 100])
            self.assertEqual(list(ares.values()), [1, 3])
            self.assertEqual(list(ares.times()), [-100, 100])
            scores.append(('#ts', '%s interpolate against boundaaryts' % i, 1))

    @score(2)
    def test_interpolation_against_empty(self):
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([0, 5, 10], [1, 2, 3])
            ares = ts.interpolate([])
            self.assertEqual(list(ares.values()), [])
            self.assertEqual(list(ares.times()), [])
            scores.append(('#ts', '%s interpolate with empty ts' % i, 1))


class TestTSLaziness(unittest.TestCase):

    @score(2)
    def test_lazy_propery_with_sized_timeseries(self):
        """ Sized Timeseries should have a lazy property that wraps a self function. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1, 2, 3, 4], [1, 4, 9, 16])
            self.assertEqual(str(ts), str(ts.lazy.eval()))
            scores.append(('#lz', '%s valid lazy property that wraps function' % i, 1))

    @score(2)
    def test_lazy_wrapped_length_with_sized_timeseries(self):
        """ Should execute the example check_length which makes len lazy """
        @lazy
        def check_length(a, b):
            return len(a) == len(b)
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            thunk = check_length(ts_class(range(0, 4), range(1, 5)), ts_class(range(0, 4), range(1, 5)))
            self.assertEqual(thunk.eval(), True)
            scores.append(('#lz', '%s valid lazy property that wraps len' % i, 1))

    @score(2)
    def test_lazy_add_and_lazy_mul_with_sized_timeseries(self):
        """ Should execute lazy add and multiply recursively. """
        @lazy
        def lazy_add(a, b):
            return a + b

        @lazy
        def lazy_mul(a, b):
            return a + b

        @lazy
        def lazy_equal(a, b):
            return a == b

        @lazy
        def check_length(a, b, c):
            return lazy_equal(lazy_add(len(a), len(b)), lazy_add(len(b), len(c))).eval()

        for i, ts_class in SIZED_CONCRETE_CLASSES:
            thunk2 = check_length(ts_class(range(0, 4), range(1, 5)),
                                  ts_class(range(0, 4), range(1, 5)),
                                  ts_class(range(5, 9), range(2, 6)))
            self.assertEqual(thunk2.eval(), True)
            scores.append(('#lz', '%s valid lazy recursion that wraps add/mul' % i, 1))


class TestTSMean(unittest.TestCase):

    @score(2)
    def test_valid_mean_with_one_entry_sized_timeseries(self):
        """ Sized Timeseries should return mean equal to the value if len == 1. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = TimeSeries([1], [-10])
            self.assertEqual(ts.mean(), -10)
            scores.append(('#ts', '%s valid mean when len == 1' % i, 1))

    @score(2)
    def test_valid_mean_with_two_entry_sized_timeseries(self):
        """ Sized Timeseries should return mean when len > 1. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            tsa = TimeSeries([1, 2], [1, 2])
            tsb = TimeSeries([1, 2, 3, 4], [1, 2, 3, 4])
            self.assertEqual(tsa.mean(), 1.5)
            self.assertEqual(tsb.mean(), np.array([1, 2, 3, 4]).mean())
            scores.append(('#ts', '%s valid mean when len > 1' % i, 1))

    @score(2)
    def test_invalid_mean_with_no_entry_sized_timeseries(self):
        """ Sized Timeseries should throw when calling mean and len == 0. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = TimeSeries([], [])
            with self.assertRaises(Exception):
                ts.mean()
            scores.append(('#ts', '%s throws on mean() when len == 0' % i, 1))


class TestTSIterators(unittest.TestCase):

    @score(2)
    def test_itertimes_with_sized_timeseries(self):
        """ Sized Timeseries should return times when itertimes called. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            times = [1, 2, 3, 4]
            values = [0.1, 0.2, 0.3, 0.4]
            ts = ts_class(times, values)
            for i, time in enumerate(ts.itertimes()):
                self.assertEqual(time, times[i])
            scores.append(('#ts', '%s itertimes() should iterate over times' % i, 1))

    @score(2)
    def test_itervalues_with_sized_timeseries(self):
        """ Sized Timeseries should return values when itervalues called. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            times = [1, 2, 3, 4]
            values = [0.1, 0.2, 0.3, 0.4]
            ts = ts_class(times, values)
            for i, value in enumerate(ts.itervalues()):
                self.assertEqual(value, values[i])
            scores.append(('#ts', '%s itervalues() should iterate over values' % i, 1))

    @score(2)
    def test_iteritems_with_sized_timeseries(self):
        """ Sized Timeseries should return tuple (time, value) when iteritems called. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            times = [1, 2, 3, 4]
            values = [0.1, 0.2, 0.3, 0.4]
            ts = ts_class(times, values)
            for i, item in enumerate(ts.iteritems()):
                self.assertEqual(item, (times[i], values[i]))
            scores.append(('#ts', '%s itervalues() should iterate over values' % i, 1))


class TestTSUnaryyOperators(unittest.TestCase):

    @score(2)
    def test_valid_plus_sign_operator_with_positive_value_sized_timeseries(self):
        """ Sized Timeseries with positive values with the unary-plus applied should not change. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
            self.assertTrue(+(ts) == ts)
            scores.append(('#ts', '%s unary+ should not change positive values' % i, 1))

    @score(2)
    def test_valid_unary_minus_sign_operator_with_sized_timeseries(self):
        """ Sized Timeseries with negative values with the unary-plus applied should not change. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            tsa = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
            tsb = ts_class([1, 2, 3, 4], [-0.1, -0.2, -0.3, -0.4])
            self.assertEqual(-(tsa), tsb)
            self.assertEqual(-(tsb), tsa)
            scores.append(('#ts', '%s unary- should change all negative values' % i, 1))

    @score(2)
    def test_abs_operator_with_nonempty_sized_timeseries(self):
        """ Sized Timeseries with any length > 0 should return l2 norm when abs applied. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1, 2], [20., -9.])
            self.assertEqual(abs(ts), list(np.sqrt([20. * 20. + 9 * 9])))
            scores.append(('#ts', '%s abs should return l2 norm for lengths > 0' % i, 1))

    @score(2)
    def test_abs_operator_with_empty_sized_timeseries(self):
        """ Sized Timeseries with no length should throw when abs applied. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            with self.assertRaises(Exception):
                abs(ts_class([], []))
            scores.append(('#ts', '%s abs should throw for lengths == 0' % i, 1))

    @score(2)
    def test_bool_operator_with_nonempty_sized_timeseries(self):
        """ Sized Timeseries with any length > 0 should return True when l2 norm is non-zero. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            tsa = TimeSeries([1, 2, 3, 4, 5], [0.1, 0.2, 0.3, 0.4, 0.5])
            tsb = TimeSeries([1], [0.1])
            self.assertTrue(bool(tsa))
            self.assertTrue(bool(tsb))
            scores.append(('#ts', '%s bool should return true for lengths > 0' % i, 1))

    @score(2)
    def test_bool_operator_with_nonempty_sized_timeseries(self):
        """ Sized Timeseries with any length > 0 should return False when l2 norm is zero. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = TimeSeries([0, 1, 2, 3], [0, 0, 0, 0])
            self.assertFalse(bool(ts))
            scores.append(('#ts', '%s bool should return false when l2 norm is 0' % i, 1))

    @score(2)
    def test_bool_operator_with_empty_sized_timeseries(self):
        """ Sized Timeseries with any length == 0 should throw or return False when bool applied. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = TimeSeries([], [])
            temp = None
            try:
                temp = bool(ts)
            except:
                # Either throws
                pass
            else:
                # or returns False
                self.assertFalse(temp)
            scores.append(('#ts', '%s bool should return false or throw for lengths == 0' % i, 1))

class TestTSBinaryOperators(unittest.TestCase):

    @score(2)
    def test_addition_with_valid_addition_expressions(self):
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            lhs = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
            rhs = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
            result = ts_class([1, 2, 3, 4], [0.2, 0.4, 0.6, 0.8])
            self.assertTrue(result == (lhs + rhs))
            self.assertTrue((rhs + lhs) == result)
            scores.append( ('#ts', 'add basic', 1))

    @score(2)
    def test_addition_with_invalid_types_should_throw_type_error(self):
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])

            with self.assertRaises(TypeError):
                ts + 'Hello'
            with self.assertRaises(TypeError):
                'Hello' + ts
            with self.assertRaises(TypeError):
                ts + {}
            with self.assertRaises(TypeError):
                {} + ts

            scores.append( ('#ts', 'add errors', 1))

    @score(2)
    def test_addition_with_not_implemented_types_should_throw_not_implemented_error(self):
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            expr = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])

            with self.assertRaises(NotImplementedError):
                expr + [1, 2, 3, 4]
            # with self.assertRaises(NotImplementedError):
            #    [1, 2, 3, 4] + expr
            with self.assertRaises(NotImplementedError):
                expr + np.array([1, 2, 3, 4])

            scores.append( ('#ts', 'add not impl', 0))

    @score(2)
    def test_addition_with_integer_should_add_directly_to_values(self):
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            base_values = [0.1, 0.2, 0.3, 0.4]
            expr = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])

            for factor in [-2, -0.5, 0, 0.5, 2]:
                updated_values = [(factor + i) for i in base_values]
                result = ts_class([1, 2, 3, 4], updated_values)
                self.assertTrue(result == (expr + factor))
                self.assertTrue((expr + factor) == result)

            scores.append(('#ts', 'add + int val', 1))

    @score(2)
    def test_addition_with_different_length_timeseries_should_throw_value_error(self):
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts_a = ts_class([1, 2, 3, 4, 5], [0.1, 0.2, 0.3, 0.4, 0.5])
            ts_b = ts_class([1, 2, 3, 4], [0.2, 0.4, 0.6, 0.8])
            ts_c = ts_class([1, 2, 3], [0.5, 0.2, 0.9])
            ts_d = ts_class([1, 2], [1.1, 1.2])
            ts_e = ts_class([1], [0.1])
            ts_f = ts_class([], [])
            ts_all = [ts_a, ts_b, ts_c, ts_d, ts_e, ts_f]
            for i, ts_1 in enumerate(ts_all):
                for j, ts_2 in enumerate(ts_all):
                    if i == j:
                        continue
                    with self.assertRaises(ValueError):
                        ts_1 + ts_2
                    with self.assertRaises(ValueError):
                        ts_2 + ts_1
            scores.append(('#ts', 'add ts with different lengths', 1))

    @score(2)
    def test_valid_equality_check_with_valid_length_sized_timeseries(self):
        """ Sized Timeseries with the same size should work with equality condition. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            tsa = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
            tsb = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
            tsc = ts_class([1, 2, 3, 4], [0.5, 0.2, 0.9, 0.4])
            self.assertEqual(tsa, tsb)
            self.assertNotEqual(tsa, tsc)
            self.assertNotEqual(tsb, tsc)
            scores.append(('#ts', '%s class should be/not be equal on ts with the same sizes' % i, 1))

    @score(2)
    def test_invalid_equality_check_with_different_length_sized_timeseries(self):
        """ Sized Timeseries with the different sizes should throw error. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            tsa = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
            tsb = TimeSeries([1, 2, 3], [0.5, 0.2, 0.9])
            tsc = TimeSeries([], [])
            with self.assertRaises(ValueError):
                tsa == tsb
            with self.assertRaises(ValueError):
                tsa == tsc
            with self.assertRaises(ValueError):
                tsb == tsc
            scores.append(('#ts', '%s class equality check should throw when ts classes have different sizes' % i, 1))

    @score(2)
    def test_invalid_equality_check_against_invalid_types(self):
        """ Sized Timeseries should throw when equality checked with invalid types. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
            with self.assertRaises(TypeError):
                ts == 4
            with self.assertRaises(NotImplementedError):
                ts == [1, 2, 3, 4]
            with self.assertRaises(NotImplementedError):
                ts == np.array([1, 2, 3, 4])
            scores.append(('#ts', '%s class equality check should throw when not compared to ts class' % i, 1))

    @score(2)
    def test_valid_subtraction_with_valid_length_sized_timeseries(self):
        """ Sized Timeseries with the same size should work with subtraction. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            tsa = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
            tsb = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
            tsc = ts_class([1, 2, 3, 4], [0.0, 0.0, 0.0, 0.0])
            self.assertEqual(tsa - tsb, tsc)
            scores.append(('#ts', '%s class should subtract on valid ts sizes' % i, 1))

    @score(2)
    def test_valid_subtraction_with_int(self):
        """ Sized Timeseries should subtract element by element. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1, 2, 3, 4], [1.1, 1.2, 1.3, 1.4])
            ts_expect = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
            self.assertEqual(ts - 1, ts_expect)
            scores.append(('#ts', 'sub int', 1))

    @score(2)
    def test_valid_subtraction_with_float(self):
        """ Sized Timeseries should subtract element by element. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
            ts_expect = ts_class([1, 2, 3, 4], [0.0, 0.1, 0.2, 0.3])
            self.assertEqual(ts - 0.1, ts_expect)
            scores.append(('#ts', 'sub float', 1))

    @score(2)
    def test_invalid_subtraction_with_array_list(self):
        """ Sized Timeseries should throw not-implemented error. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
            with self.assertRaises(NotImplementedError):
                ts - [1, 2, 3, 4]
            with self.assertRaises(NotImplementedError):
                ts - np.array([1, 2, 3, 4])
            scores.append(('#ts', 'sub array list', 1))

    @score(2)
    def test_invalid_subtraction_with_different_length_sized_timeseries(self):
        """ Sized Timeseries with the same size should work with subtraction. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            t_a = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
            t_e = ts_class([1, 2, 3], [0.5, 0.2, 0.9])
            t_f = ts_class([], [])
            with self.assertRaises(ValueError):
                t_a - t_e
            with self.assertRaises(ValueError):
                t_a - t_f
            scores.append(('#ts', 'sub diff ts lengths', 1))

    @score(2)
    def test_invalid_subtraction_with_string(self):
        """ Sized Timeseries should throw TypeError when subtracting with string. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
            with self.assertRaises(TypeError):
                ts - 'Hello'
            with self.assertRaises(TypeError):
                'Hello' - ts
            scores.append(('#ts', '%s class should throw when subtracting from string' % i, 1))

    @score(2)
    def test_valid_multiplication_with_valid_length_sized_timeseries(self):
        """ Sized Timeseries with the same size should work with multiplication """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts_a = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
            ts_b = ts_class([1, 2, 3, 4], [2.0, 3.0, 3.0, 2.0])
            ts_c = ts_class([1, 2, 3, 4], [0.2, 0.6, 0.9, 0.8])
            self.assertEqual(ts_a * ts_b, ts_c)
            scores.append(('#ts', '%s class should multiply on valid ts sizes' % i, 1))

    @score(2)
    def test_invalid_multiplication_with_string(self):
        """ Sized Timeseries should throw TypeError when multiplying with string. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
            with self.assertRaises(TypeError):
                ts * 'Hello'
            scores.append(('#ts', '%s class should throw when multiplying with string' % i, 1))

    @score(2)
    def test_invalid_multiplication_with_list_array(self):
        """ Sized Timeseries should throw when multiplying with list/array. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
            with self.assertRaises(NotImplementedError):
                ts * [1, 2, 3, 4]
            with self.assertRaises(NotImplementedError):
                ts * np.array([1, 2, 3, 4])
            scores.append(('#ts', '%s class should throw when multiplying with list/array' % i, 1))

    @score(2)
    def test_valid_multiplication_with_integer(self):
        """ Sized Timeseries should multiply all values by integer. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            factor = 2
            tsa = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
            tsb = ts_class([1, 2, 3, 4], [0.2, 0.4, 0.6, 0.8])
            self.assertEqual(tsa * factor, tsb)
            scores.append(('#ts', '%s class should multiply values by integer factor' % i, 1))

    @score(2)
    def test_valid_multiplication_with_float(self):
        """ Sized Timeseries should multiply all values by float. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            factor = 2.2
            tsa = ts_class([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
            tsb = ts_class([1, 2, 3, 4], [0.22, 0.44, 0.66, 0.88])
            tsc = tsa * factor
            self.assertEqual(tsc, tsb)
            scores.append(('#ts', '%s class should multiply values by float factor' % i, 1))

    @score(2)
    def test_invalid_multiplication_with_inconsistent_sizes(self):
        """ Sized Timeseries should throw when multiplying a differently-sized time-series. """
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            tsa = TimeSeries([1, 2, 3, 4, 5], [0.1, 0.2, 0.3, 0.4, 0.5])
            tsb = TimeSeries([1, 2, 3], [0.5, 0.2, 0.9])
            tsc = TimeSeries([], [])
            with self.assertRaises(ValueError):
                tsa * tsb
            with self.assertRaises(ValueError):
                tsa * tsc
            with self.assertRaises(ValueError):
                tsb * tsc
            scores.append(('#ts', '%s class should throw when multiplying two differently-sized timeseries' % i, 1))


class TestTimeSeriesDocs(unittest.TestCase):

    @score(2)
    def test_all_required_methods_have_docstrings(self):
        """ Make sure that all the required methods are well documented """
        DOCSTRING_LENGTH = 5
        REQUIRED_DOCSTRINGS = ['__init__', '__str__', 'items', '__contains__',
                               '__iter__', '__eq__', '__add__', '__sub__', '__mul__',
                               'itertimes', 'itervalues', 'iteritems', '__abs__', '__bool__']
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1, 2, 3], [1, 2, 3])
            for method in REQUIRED_DOCSTRINGS:
                try:
                    if len(getattr(ts, method, '').__doc__.strip()) > DOCSTRING_LENGTH:
                        scores.append(('#doc', 'item docstrings: ' + method, 1))
                except AttributeError:
                    scores.append(('#doc', 'item docstrings: ' + method, 0))
                    continue
                except Exception as e:
                    logging.exception(e)
                    scores.append(('#doc', 'item docstrings: ' + method, 0))

    @score(2)
    def test_class_has_docstring(self):
        for i, ts_class in SIZED_CONCRETE_CLASSES:
            ts = ts_class([1, 2, 3], [1, 2, 3])
            self.assertIsNotNone(ts.__doc__)
            self.assertTrue(len(ts.__doc__) > 10)
            scores.append(('#doc', 'class docstrings', 1))

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
            "std",
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

    @score(1)
    def test_accumulated_methods_exist_in_list_timeseries(self):
        missing_methods = self._build_missing_methods(ArrayTimeSeries)
        self.assertListEqual(
            missing_methods, [],
            msg="The TimeSeries class does not contain the methods: {}".format(missing_methods))
        scores.append(('#ts', 'timeseries has all required methods', 1))

    @score(1)
    def test_accumulated_methods_exist_in_array_timeseries(self):
        missing_methods = self._build_missing_methods(TimeSeries)
        self.assertListEqual(
            missing_methods, [],
            msg="The TimeSeries class does not contain the methods: {}".format(missing_methods))
        scores.append(('#ts', 'timeseries does not have all required methods', 1))

class TestInterfaceSpec(unittest.TestCase):
    """ Tests the module 'Time Series Interface and Implementation. """

    @score(1)
    def test_that_timeseriesinterface_is_abc(self):
        self.assertIsInstance(TimeSeriesInterface, ABCMeta)
        scores.append(('#ts', 'timeseries interface is abstract', 1))

    @score(1)
    def test_class_hierachy_of_timeseries(self):
        class_history= inspect.getmro(TimeSeries)
        self.assertIn('TimeSeries', str(class_history[0]))
        self.assertIn('SizedContainerTimeSeriesInterface', str(class_history[1]))
        self.assertIn('TimeSeriesInterface', str(class_history[2]))
        scores.append(('#ts', 'list timeseries follows interface', 1))

    @score(1)
    def test_class_hierachy_of_array_timeseries(self):
        class_history= inspect.getmro(ArrayTimeSeries)
        self.assertIn('ArrayTimeSeries', str(class_history[0]))
        self.assertIn('SizedContainerTimeSeriesInterface', str(class_history[1]))
        self.assertIn('TimeSeriesInterface', str(class_history[2]))
        scores.append(('#ts', 'array timeseries follows interface', 1))

    @score(1)
    def test_class_hierachy_of_simulated_timeseries(self):
        class_history= inspect.getmro(SimulatedTimeSeries)
        self.assertIn('SimulatedTimeSeries', str(class_history[0]))
        self.assertIn('StreamTimeSeriesInterface', str(class_history[1]))
        self.assertIn('TimeSeriesInterface', str(class_history[2]))
        scores.append(('#ts', 'streaming timeseries follows interface', 1))
