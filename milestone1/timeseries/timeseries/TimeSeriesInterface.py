from abc import ABCMeta, abstractmethod


class TimeSeriesInterface(metaclass=ABCMeta):

    @abstractmethod
    def	__iter__ (self):
        """ iterates over values
        :return:
        """

    @abstractmethod
    def	itertimes(self):
        """ iterate over times
        :return:
        """

    @abstractmethod
    def	itervalues(self):
        """ iterate over values
        :return:
        """
    @abstractmethod
    def	iteritems(self):
        """ iterate over (time, value) tuples
        :return:
        """

    @abstractmethod
    def	values (self):
        """ access timeseries value data
        :return:
        """

    @abstractmethod
    def	times (self):
        """ access timeseries time data
        :return:
        """
    @abstractmethod
    def	items(self):
        """ list of (time, value) tuples
        :return:
        """
    @abstractmethod
    def	mean(self):
        """ returns mean of values
        :return:
        """

    @abstractmethod
    def	std(self):
        """ returns mean of values
        :return:
        """

    @abstractmethod
    def	median (self):
        """ returns median of values
        :return:
        """

    @abstractmethod
    def	__eq__ (self, rhs) :
        """ elementwise comparison of two timeseries
        :param rhs:
        :return:
        """

    @abstractmethod
    def	__neg__ (self, rhs):
        """ negate values of timeseries
        :return:
        """

    @abstractmethod
    def	__pos__ (self):
        """
        :return: returns identity
        """

    @abstractmethod
    def	__abs__ (self):
        """ returns l2 norm of timeseries values
        :return:
        """
    @abstractmethod
    def	__bool__ (self):
        """ returns whether the l2 norm of the timeseries values is non-zero
        :return:
        """

    @abstractmethod
    def	__add__ (self, rhs):
        """ adds two timeseries elementwise or with a constant

        :param rhs:
        :return:
        """

    @abstractmethod
    def	__sub__ (self, rhs):
        """ substracts two timeseries elementwise or with a constant
        :param rhs:
        :return:
        """

    @abstractmethod
    def	__mul__ (self, rhs):
        """ multiplies two timeseries elementwise or with a constant
        :param rhs:
        :return:
        """
