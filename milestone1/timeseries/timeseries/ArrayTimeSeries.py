import numbers
import numpy as np
from timeseries.lazy import *
from timeseries.SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface

# to avoid float problems, allow some tolerance!
tolerance = 10 ** (-9)

class ArrayTimeSeries(SizedContainerTimeSeriesInterface):
    """ Doc taken from timeseries mostly """

    def __init__(self, times, values):
        """
        initializes TimeSeries object with data as values
        make sure they are of the same type

        data should be a sequence object

        Parameters
        ----------
        times : the timepoints associated with the values
        values : the values of the timeseries

        """

        # make sure they have the same length
        assert len(times) == len(values), 'times and values should have the same length'

        # cast iterable object to list first to allow for numpy copying
        # cast explicitly to float to avoid any cast problems
        self._times = np.array(list(times), copy=True, dtype=float)
        self._values = np.array(list(values), copy=True, dtype=float)

        # the times should be monotonically increasing, resort arrays!
        sorted_idxs = np.argsort(self._times)
        self._times = self._times[sorted_idxs]
        self._values = self._values[sorted_idxs]

    def __len__(self):
        """
        returns length of TimeSeries

        >>> ts = ArrayTimeSeries([0.5, 1., 2., 4.], [1, 2, 3, 4])
        >>> len(ts)
        4
        >>> len(ArrayTimeSeries([], []))
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

        >>> ts = ArrayTimeSeries([0.5, 0.7, 0.8, 1.0], [0.5, 1., 2., 4.])
        >>> ts[0]
        0.5
        >>> ts[3]
        4.0
        """
        assert (isinstance(index, int))
        return self._values[index]

    def __setitem__(self, index, value):
        """
        Updates the value of timeseries at position index.
        We currently do not allow changing times to preserve order.

        Parameters
        ----------
        index : position to update
        val : new value to update timeseries at position index with

        >>> ts = ArrayTimeSeries([0.5, 0.7, 0.8, 1.0], [0.5, 1., 2., 4.])
        >>> ts[0] = 2.0
        2.0
        >>> ts[0]
        2.0
        """
        try:
            assert (isinstance(index, int))
            assert (isinstance(value, numbers.Number))
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
        return value in self._values

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

            return ArrayTimeSeries(times, vals)
        # empty list submitted, return empty timeseries!
        else:
            return ArrayTimeSeries([], [])

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

        >>> ts = ArrayTimeSeries([0, 1], [5.0, 6.0])
        >>> ts.mean()
        5.5
        """
        if len(self) == 0:
            raise ValueError
        return self._values.mean()

    def median(self):
        """
        Returns
        -------
        median of stored values

        >>> ts = ArrayTimeSeries([0, 1, 2], [4.0, 6.0, 4.0])
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

        >>> ta = ArrayTimeSeries([1, 2], [0.4, 0.5])
        >>> tb = ArrayTimeSeries([1, 2], [-0.4, 0.8])
        >>> ta == ta
        True
        >>> ta == tb
        False
        """
        if not isinstance(rhs, ArrayTimeSeries):
            if isinstance(rhs, (np.ndarray, list)):
                raise NotImplementedError
            else:
                raise TypeError('can not compare time series to {}'.format(type(rhs)))

        # this could be seen also as return false
        if len(self) != len(rhs):
            raise ValueError(str(self) + ' and ' + str(rhs) + 'must have the same time points')

        return np.allclose(self._values, rhs.values())

    def __radd__(self, lhs):
        return self + lhs

    def __add__(self, rhs):
        """
        Parameters
        ----------
        rhs : timeseries or constant to add

        Returns
        -------
        new timeseries object as result of the addition
        """
        if isinstance(rhs, (ArrayTimeSeries)):
            if len(self) != len(rhs):
                raise ValueError(str(self) + ' and ' + str(rhs) + 'must have the same time points')

            if not np.allclose(self._times, rhs.times(), atol=tolerance):
                raise ValueError(str(self) + ' and ' + str(rhs) + 'must have the same time points')
            return ArrayTimeSeries(self._times, self._values + rhs.values())

        elif isinstance(rhs, (int, float)):
            return ArrayTimeSeries(self._times, self._values + rhs)
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
        if isinstance(rhs, (ArrayTimeSeries)):
            if len(self) != len(rhs):
                raise ValueError(str(self) + ' and ' + str(rhs) + 'must have the same time points')
            return ArrayTimeSeries(self._times, self._values - rhs.values())

        elif isinstance(rhs, (int, float)):
            return ArrayTimeSeries(self._times, self._values - rhs)
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
        if isinstance(rhs, (ArrayTimeSeries)):
            if len(self) != len(rhs):
                raise ValueError(str(self) + ' and ' + str(rhs) + 'must have the same time points')
            return ArrayTimeSeries(self._times, self._values * rhs.values())

        elif isinstance(rhs, (int, float)):
            return ArrayTimeSeries(self._times, self._values * rhs)
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

        return np.sqrt(np.sum(self._values * self._values))

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
        return ArrayTimeSeries(self._times, -self._values)

    def __pos__(self):
        """
        Returns
        -------
        returns identity (unary +)
        """
        return ArrayTimeSeries(self._times, self._values)

    def __repr__(self):
        """
        returns formal string representation

        Returns
        -------
        formal string representation of timeseries class
        """
        if len(self) > 0:
            return '<{},{}-ArrayTimeSeries>'.format(type(self._times[0]), type(self._values[0]))
        else:
            return '<empty-ArrayTimeSeries'

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
            return 'ArrayTimeSeries(t={}, v={})'.format(str(list(self._times)), str(list(self._values)))
        else:
            return 'ArrayTimeSeries(t=[{}, {}, ..., {}, {}], v=[{}, {}, ..., {}, {}])'.format( \
                self._times[0], self._times[1], self._times[-2], self._times[-1], \
                self._values[0], self._values[1], self._values[-2], self._values[-1])
