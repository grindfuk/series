from timeseries.TimeSeriesInterface import TimeSeriesInterface
from abc import abstractmethod

class SizedContainerTimeSeriesInterface(TimeSeriesInterface):

    @abstractmethod
    def __len__(self):
        """
        :return: length of stored timeseries
        """

    @abstractmethod
    def __getitem__(self, index):
        """
        :param index: the index of the stored value
        :return: the element stored at index position
        """

    @abstractmethod
    def __setitem__(self, index, val):
        """
        :param index: the index of the stored value
        :param val: the new value
        :return: the val.

        Side-Effect:
            Updates element at index position
        """

    @abstractmethod
    def __contains__(self, time):
        """ check whether time point is contained
        :param time:
        :return:
        """
