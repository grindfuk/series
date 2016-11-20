"""
Reference Implementation for the TimeSeries class and Further Assignments. 
"""

import numpy as np
import numbers
from timeseries.lazy import *
from timeseries.SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface


# to avoid float problems, allow some tolerance!
tolerance = 10 ** (-9)


class TimeSeries(SizedContainerTimeSeriesInterface):
    """
	A class to store a non-uniform timeseries

	Attributes:
		_times: the time points of the given time series
		_values: the values of the given time series

	Methods:

		__getitem__ : returns the element stored at index position
		__setitem__ : updates element at index position 
		__contains__ : check whether time point is contained
		__iter__ : iterates over values

		values : access timeseries value data
		itervalues : iterate over values
		times : access timeseries time data
		itertimes : iterate over times
		items : list of (time, value) tuples
		iteritems : iterate over (time, value) tuples

		__len__ : returns length of stored timeseries
		__repr__: abbreviating string representation

		mean : returns mean of values
		median : returns median of values

		__abs__ : returns l2 norm of timeseries values
		__bool__ : returns whether the l2 norm of the timeseries values is non-zero
		__neg__ : negate values of timeseries
		__pos__ : returns identity

		__eq__  : elementwise comparison of two timeseries
		__add__ : adds two timeseries elementwise or with a constant
		__sub__ : substracts two timeseries elementwise or with a constant
		__mul__ : multiplies two timeseries elementwise or with a constant
	"""

    def __init__(self, times_or_values, values=None):
        """ Initializes TimeSeries object with data as times and values

		make sure they are of the same type
		data should be a sequence object

		Parameters
		----------
		times : the timepoints associated with the values
		values : the values of the timeseries
		"""
        try:
            if values is not None:
                times = list(times_or_values)
                values = list(values)
            else:
                values = list(times_or_values)
                times = list(range(len(values)))
        except:
            raise TypeError('times and values must be coercible to internal storage type (list)')

        assert isinstance(times, list), 'times should be a list'
        assert isinstance(values, list), 'values should be a list'

        if len(times) != len(values):
            raise ValueError('times and values should have the same length')
        if len(values):
            # XXX: Make this better
            print(not isinstance(times[0], (int, float, complex)))
            if not isinstance(times[0], (int, float, complex)):
                raise ValueError('times and values must be numeric type')

        self._times = list(times)
        self._values = list(values)

    def __len__(self):
        """
		returns length of TimeSeries

		>>> ts = TimeSeries([0.5, 1., 2., 4.], [1, 2, 3, 4])
		>>> len(ts)
		4
		>>> len(TimeSeries([], []))
		0
		"""
        return len(self._times)

    def __getitem__(self, index):
        """
		Gets the value of the timeseries at the position index.
		This implementation does not search against times.

		Parameters
		----------
		index : the position to query for 

		Returns
		-------
		timeseries value at position index

		>>> ts = TimeSeries([0.5, 0.7, 0.8, 1.0], [0.5, 1., 2., 4.])
		>>> ts[0]
		0.5
		>>> ts[3]
		4.0
		"""
        assert(isinstance(index, int))
        return self._values[index]

    def __setitem__(self, index, value):
        """
        Updates the value of timeseries at position index.
        We currently do not allow changing times to preserve order.

		Parameters
		----------
		index : position to update
		val : new value to update timeseries at position index with

		>>> ts = TimeSeries([0.5, 0.7, 0.8, 1.0], [0.5, 1., 2., 4.])
		>>> ts[0] = 2.0
		2.0
		>>> ts[0]
		2.0
		"""
        try:
            assert(isinstance(index, int))
            assert(isinstance(value, numbers.Number))
        except Exception as e:
            raise Exception("setitem must be of the form `object[int] = Number`") from e
        self._values[index] = value
        return self._values[index]

    def __contains__(self, value):
        """
		Checks whether value is contained within stored time points

		Parameters
		----------
		value: value point to check for whether it is contained

		Returns
		-------
		true if value point is contained else false
		"""
        return (value in self._values)

    def __iter__(self):
        """
		iterates over values 
		"""
        for v in self._values:
            yield v

    def itertimes(self):
        """
		iterate over time points
		"""
        for t in self._times:
            yield t

    def itervalues(self):
        """
		iterate over values
		"""
        return self.__iter__()

    def iteritems(self):
        """
		iterate over (time, value) tuples
		"""
        for item in self.items():
            yield item

    # @property
    def values(self):
        """
		returns stored values
		"""
        return self._values

    # @property
    def times(self):
        """
		returns stored time points
		"""
        return self._times

    # @property
    def items(self):
        """
		Returns
		-------
		returns sequence of (time, value) tuples
		"""
        return zip(self._times, self._values)

    def interpolate(self, times):
        """
		interpolates a new time sequence from the old one

		Parameters
		----------
		times : time points for which the new timeseries shall be interpolated

		Returns
		-------
		new timeseries object with time points times and interpolated values
		"""
        # interpolate for all given points
        if len(times) > 0:
            vals = []
            for t in times:
                # find nearest point using numpy binary search (right index, i.e. the larger one)
                indR = np.searchsorted(self._times, t, side='right')

                # handle special cases at boundaries
                if indR == 0:
                    vals.append(self._values[0])
                elif indR == len(self):
                    vals.append(self._values[-1])
                else:
                    # interpolate
                    # p(x) = f(x_0) + (f(x_1) - f(x_0)) / (x_1 - x_0) (x - x_0)
                    interp_val = self._values[indR - 1] + (self._values[indR] - self._values[indR - 1]) / \
                                                          (self._times[indR] - self._times[indR - 1]) * (
                                                          t - self._times[indR - 1])

                    vals.append(interp_val)

            return TimeSeries(times, vals)
        # empty list submitted, return empty timeseries!
        else:
            return TimeSeries([], [])

    @property
    def lazy(self):
        """
		Returns
		-------
		returns lazified version of TimeSeries class 
		"""

        def id_fun(*args, **kwargs):
            return self

        return LazyOperation(id_fun, self)

    def mean(self):
        """
		Returns
		-------
		mean of stored values

		>>> ts = TimeSeries([0, 1], [5.0, 6.0])
		>>> ts.mean()
		5.5
		"""
        if len(self) == 0:
            raise ValueError
        return np.array(self._values).mean()

    def median(self):
        """
		Returns
		-------
		median of stored values

		>>> ts = TimeSeries([0, 1, 2], [4.0, 6.0, 4.0])
		>>> ts.median()
		4.0
		"""
        if len(self) == 0:
            raise ValueError
        return np.median(self._values)

    def std(self):
        """
        :return: standard deviation of the stored values.
        """
        return np.std(self._values)

    def __eq__(self, rhs):
        """
		Parameters
		----------
		rhs : timeseries to compare to

		Returns
		-------
		true if values of timeseries match and time domain is equal, false else

		>>> ta = TimeSeries([1, 2], [0.4, 0.5])
		>>> tb = TimeSeries([1, 2], [-0.4, 0.8])
		>>> ta == ta
		True
		>>> ta == tb
		False
		"""
        print(rhs)
        print(self)
        if not isinstance(rhs, TimeSeries):
            if isinstance(rhs, (np.ndarray, list)):
                raise NotImplementedError
            else:
                raise TypeError('can not compare TimeSeries to {}'.format(type(rhs)))

        # this could be seen also as return false
        if len(self) != len(rhs):
            raise ValueError(str(self) + ' and ' + str(rhs) + 'must have the same time points')

        if not np.allclose(self._times, rhs.times(), atol=tolerance):
            raise ValueError(str(self) + ' and ' + str(rhs) + 'must have the same time points')

        return np.allclose(self._values, rhs.values(), atol=tolerance)

    def __add__(self, rhs):
        """
		Parameters
		----------
		rhs : timeseries or constant to add

		Returns
		-------
		new timeseries object as result of the addition
		"""
        if isinstance(rhs, (TimeSeries)):
            if len(self) != len(rhs):
                raise ValueError(str(self) + ' and ' + str(rhs) + 'must have the same time points')

            if not np.allclose(self._times, rhs.times(), atol=tolerance):
                raise ValueError(str(self) + ' and ' + str(rhs) + 'must have the same time points')
            return TimeSeries(self._times, self._values + rhs.values())

        elif isinstance(rhs, (int, float)):
            return TimeSeries(self._times, self._values + rhs)
        else:
            if isinstance(rhs, (np.ndarray, list)):
                raise NotImplementedError
            else:
                raise TypeError('can not compare time series to {}'.format(type(rhs)))

    def __sub__(self, rhs):
        """
		Parameters
		----------
		rhs : timeseries or constant to substract

		Returns
		-------
		new timeseries object as result of the substraction
		"""
        if isinstance(rhs, (TimeSeries)):
            if len(self) != len(rhs):
                raise ValueError(str(self) + ' and ' + str(rhs) + 'must have the same time points')

            if not np.allclose(self._times, rhs.times(), atol=tolerance):
                raise ValueError(str(self) + ' and ' + str(rhs) + 'must have the same time points')
            updated_values = [
                self._values[i] - rhs.values()[i] for i in range(len(self._values))
            ]
            return TimeSeries(self._times, updated_values)

        elif isinstance(rhs, (int, float)):
            return TimeSeries(self._times, self._values - rhs)
        else:
            if isinstance(rhs, (np.ndarray, list)):
                raise NotImplementedError
            else:
                raise TypeError('can not compare time series to {}'.format(type(rhs)))

    def __mul__(self, rhs):
        """
		Parameters
		----------
		rhs : timeseries or constant to multiply with

		Returns
		-------
		new timeseries object as result of the multiplication
		"""
        if isinstance(rhs, (TimeSeries)):
            if len(self) != len(rhs):
                raise ValueError(str(self) + ' and ' + str(rhs) + 'must have the same time points')

            if not np.allclose(self._times, rhs.times(), atol=tolerance):
                raise ValueError(str(self) + ' and ' + str(rhs) + 'must have the same time points')

            rhs_values = rhs.values()
            updated_values = [ self._values[i] * rhs_values[i] for i in range(len(rhs_values)) ]
            return TimeSeries(self._times, updated_values)

        elif isinstance(rhs, (int, float)):
            updated_values = list(map(lambda x: x*rhs, self._values))
            return TimeSeries(self._times, updated_values)
        else:
            if isinstance(rhs, (np.ndarray, list)):
                raise NotImplementedError
            else:
                raise TypeError('can not compare time series to {}'.format(type(rhs)))

    def __abs__(self):
        """
		Returns
		-------
		returns l2 norm of the series values
		"""
        assert (len(self) > 0)
        updated_values = [self._values[i]**2 for i in range(len(self._values))]
        return np.sqrt(np.sum(updated_values))

    def __bool__(self):
        """
		Returns
		-------
		returns whether l2 norm of the series values is positive
		"""
        return bool(abs(self) > tolerance)

    def __neg__(self):
        """
		Returns
		-------
		returns series with negated values
		"""
        updated_values = [-1*self._values[i] for i in range(len(self._values))]
        return TimeSeries(self._times, updated_values)

    def __pos__(self):
        """
		Returns
		-------
		returns identity (unary +)
		"""
        return TimeSeries(self._times, self._values)

    def __repr__(self):
        """
		returns formal string representation

		Returns
		-------
		formal string representation of timeseries class
		"""
        if len(self) > 0:
            return '<{},{}-TimeSeries>'.format(type(self._times[0]), type(self._values[0]))
        else:
            return '<empty-TimeSeries'

    def __str__(self):
        """
		informal string representation in a descriptive manner
		outputs elements at the start and end of the timeseries

		Returns
		-------
		informal string representation
		"""

        # print out all values if less or equal than 5 values
        if len(self) <= 5:
            return 'TimeSeries(t={}, v={})'.format(str(list(self._times)), str(list(self._values)))
        else:
            return 'TimeSeries(t=[{}, {}, ..., {}, {}], v=[{}, {}, ..., {}, {}])'.format( \
                self._times[0], self._times[1], self._times[-2], self._times[-1], \
                self._values[0], self._values[1], self._values[-2], self._values[-1])
