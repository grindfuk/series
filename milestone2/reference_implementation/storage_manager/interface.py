import abc
import uuid


class StorageManagerInterface(abc.ABC):
    """ Interface for id based persistent storage for python objects """

    def generate_storage_id(self):
        """ Returns a new FAPP unique storage_id """
        return uuid.uuid4()

    @abc.abstractmethod
    def store(self, storage_id, obj):
        """ Stores a given object with the index `storage_id`

        Parameters
        ----------
        storage_id : int / string
            id of object we want to store
        object : Python Object

        Returns
        -------
        object : with attribute storage_id set

        Notes
        -----
        - Storage calls to duplicate `storage_id`s  will be a last-write behavior.
        """

    @abc.abstractmethod
    def size(self, storage_id):
        """ Returns the size of the object defined by the object's __len__

        Parameters
        ----------
        storage_id : int / string
            id of object we want

        Returns
        -------
        int: Length of the time series in storage corresponding to `id`

        Raises:
        -------
            KeyError: if `storage_id` does not exist
        """

    @abc.abstractmethod
    def get(self, storage_id):
        """ Retrieves an object from storage by `storage_id`

        Parameters
        ----------
        storage_id : int / string
            id of object we want to get

        Returns
        -------
        object : with attribute storage_id set

        Raises:
        -------
            KeyError: if `storage_id` does not exist
        """
