from timeseries import SimulatedTimeSeries
from timeseries.TimeSeriesInterface import TimeSeriesInterface
from abc import abstractmethod

class StreamTimeSeriesInterface(TimeSeriesInterface):
    """ A partial abstract class that defines the interface that any streaming
        time-series should have

	Attributes:
	    _mean: The running mean
	    _std: The running standard deviation

	Methods:

		__iter__ : iterates over values

		% Doesn't make sense in Stream. values : access timeseries value data
		% Doesn't make sense in Stream. itervalues : iterate over values
		% Doesn't make sense in Stream. times : access timeseries time data
		% Doesn't make sense in Stream. itertimes : iterate over times
		% Doesn't make sense in Stream. items : list of (time, value) tuples
		% Doesn't make sense in Stream. iteritems : iterate over (time, value) tuples
		% Doesn't make sense in Stream. __len__ : returns length of stored timeseries

		__repr__: abbreviating string representation

		mean : returns running mean of value
		median : returns running median of value

		__abs__ : returns l2 norm of timeseries values
		__bool__ : returns whether the l2 norm of the timeseries values is non-zero
		__neg__ : negate values of timeseries
		__pos__ : returns identity

		__eq__  : elementwise comparison of two timeseries
		__add__ : adds two timeseries elementwise or with a constant
		__sub__ : substracts two timeseries elementwise or with a constant
		__mul__ : multiplies two timeseries elementwise or with a constant
    """

    @abstractmethod
    def produce(self, chunk):
        """ Produces a chunk sized bunch of new elements into the TimeSeries whenever it is called.
        :param chunk:
        :return:
        """

    def online_mean(self):
        """ Returns the Streaming TimeSeries that returns series of averages when produce is called."""

        # Also add an online_mean and online_std for StreamTimeSeriesInterface time-series,
        # which themselves return the appropriate time-series.

        # These "online" methods should return new SimulatedTimeSeries of the appropriate type,
        # and when produce is called on them, should produce chunk means and standard deviations,
        # starting from the current state of the time series.
        # (notice that this will be the meaning of mean and std with non default chunk as well: ie, the last chunk observations' statistic )

        def online_mean(iterator):
            n = 0
            mu = 0
            for value in iterator:
                n += 1
                delta = value - mu
                mu = mu + delta / n
                yield mu

        generator = online_mean
        return SimulatedTimeSeries(online_mean)

    @abstractmethod
    def online_std(self):
        """ Returns the moving standard deviation of a Streaming TimeSeries """

    @abstractmethod
    def __eq__(self, chunk=1):
        """ Element-wise comparison of two chunks of streaming timeseries.
            The chunks must match
        :param chunk:
        :return:
        """

    @abstractmethod
    def __add__(self, chunk=1):
        """ Element-wise addition of two chunks of streaming TimeSeries or with a constant.
        :param chunk:
        :return:
        """

    @abstractmethod
    def __sub__(self, chunk=1):
        """ Substracts two streaming timeseries elementwise or with a constant.

        :param chunk:
        :return:
        """

    def __mul__ (self, chunk=1):
        """ Multiplies two timeseries elementwise or with a constant

        :param chunk:
        :return:
        """




