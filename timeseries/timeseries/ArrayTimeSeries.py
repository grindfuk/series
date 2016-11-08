import numpy as np
from timeseries.TimeSeries import TimeSeries
from timeseries.SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface

class ArrayTimeSeries(SizedContainerTimeSeriesInterface):

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

        >>> ts = TimeSeries([0.5, 1., 2., 4.], [1, 2, 3, 4])
        >>> len(ts)
        4
        >>> len(TimeSeries([], []))
        0
        """
        return len(self._times)

    def __getitem__(self, time):
        """
        returns value of timeseries at position index

        Parameters
        ----------
        index : the position to query for

        Returns
        -------
        timeseries value at position index

        >>> ts = TimeSeries([0.5, 0.7, 0.8, 1.0], [0.5, 1., 2., 4.])
        >>> ts[0.5]
        0.5
        >>> ts[1.0]
        4.0
        """

        # we sorted the array in the constructor, this means we can use binary search
        # for a quick lookup!
        # if the value is not found, returns the next higher one
        ind = np.searchsorted(self._times, time, side='right')

        # make sure index is within range
        ind = max(min(ind, len(self) - 1), 0)

        if abs(time - self._times[ind]) < tolerance:
            return self._values[ind]
        # is the previous element a better fit?
        if abs(time - self._times[ind - 1]) < tolerance:
            return self._values[ind - 1]
        # the value could not be looked up, raise an IndexError!
        raise IndexError
        return np.NaN

    def __setitem__(self, time, val):
        """
        updates value of timeseries at position index

        Parameters
        ----------
        index : position to update
        val : new value to update timeseries at position index with

        >>> ts = TimeSeries([0.5, 0.7, 0.8, 1.0], [0.5, 1., 2., 4.])
        >>> ts[0.8]
        2.0
        >>> ts[0.8] = 5.0
        >>> ts[0.8]
        5.0
        """

        # we sorted the array in the constructor, this means we can use binary search
        # for a quick lookup!
        # if the value is not found, returns the next higher one
        ind = np.searchsorted(self._times, time, side='right')

        # make sure index is within range
        ind = max(min(ind, len(self) - 1), 0)

        if abs(time - self._times[ind]) < tolerance:
            self._values[ind] = float(val)
            return
        # is the previous element a better fit?
        if abs(time - self._times[ind - 1]) < tolerance:
            self._values[ind - 1] = float(val)
            return
        # the value could not be looked up, raise an IndexError!
        raise IndexError

    def __contains__(self, time):
        """
        checks whether time is contained within stored time points

        Parameters
        ----------
        time : time point to check for whether it is contained

        Returns
        -------
        true if time point is contained, false else
        """
        # we sorted the array in the constructor, this means we can use binary search
        # for a quick lookup!
        # if the value is not found, returns the next higher one
        ind = np.searchsorted(self._times, time, side='right')

        # make sure index is within range
        ind = max(min(ind, len(self) - 1), 0)

        if abs(time - self._times[ind]) < tolerance:
            return True
        # is the previous element a better fit?
        if abs(time - self._times[ind - 1]) < tolerance:
            return True
        return False

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
        return self._values.mean()

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
        if not isinstance(rhs, TimeSeries):
            if isinstance(rhs, (np.ndarray, list)):
                raise NotImplementedError
            else:
                raise TypeError('can not compare time series to {}'.format(type(rhs)))

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
            return TimeSeries(self._times, self._values - rhs.values())

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
            return TimeSeries(self._times, self._values * rhs.values())

        elif isinstance(rhs, (int, float)):
            return TimeSeries(self._times, self._values * rhs)
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
        return TimeSeries(self._times, -self._values)

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
