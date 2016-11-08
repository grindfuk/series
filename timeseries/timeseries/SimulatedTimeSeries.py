from timeseries.StreamTimeSeriesInterface import StreamTimeSeriesInterface
import logging

class SimulatedTimeSeries(StreamTimeSeriesInterface):

    def __init__(self, generating_function):
        """ Initializes a SimulatedTimeSeries object with a time-series point-generator

        The generator must return a timeseries point of the form (time, value)

        Parameters
        ----------
        generator: the generator used from producing the timeseries points
        """
        self.generator = generating_function
        self.n = 0
        self.mu = 0
        self.std = 0

    def _update_moving_mean_and_std(self, value):
        self.n += 1
        delta = value - self.mu
        self.mu = self.mu + delta/self.n
        if (value - self.mu) == 0:
            self.std = 0
        else:
            self.std = self.std + delta/(value - self.mu)

    def produce(self, chunk=1):
        """ Produces a chunk sized bunch of new elements into the timeseries whenever it is called.

        :param chunk: The number of values to produce into the timeseries
        :return:
        """
        assert(isinstance(chunk, int))
        for i in range(chunk):
            value = next(self.generator)
            logging.debug(value)
            self._update_moving_mean_and_std(value)
            yield value

    @property
    def mean(self):
        """ Returns the moving average of a Streaming TimeSeries """
        return self.mu

    @property
    def std(self):
        """ Returns the moving standard deviation of a Streaming TimeSeries """
        return self.std

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