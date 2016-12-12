import unittest
from student_solutions import repo
"""
NOTES:
    - There are 2 main concrete testable classes, the FileStorageManager and the SMTimeSeries
        What do we want to know about them?
    - The parts that we need to inspect will be their caching mechanism and whether it actually works.
"""

SCORE = 0
TOTAL_SCORE = 0

class MainTest(unittest.TestCase):

    group = None

    def setUp(self):
        global StorageManagerInterface
        global FileStorageManager
        global SMTimeSeries
        StorageManagerInterface = repo[self.group]["StorageManagerInterface"]
        FileStorageManager = repo[self.group]["FileStorageManager"]
        SMTimeSeries = repo[self.group]["SMTimeSeries"]

    def test_storage_manager_interface_has_abstract_methods(self):
        """  Test for the required abstract methods
        Ref:
        Create a new StorageManagerInterface which has the abstract methods:
        * store
        * size
        * get
        """
        for method in ["store", "size", "get"]:
            cls_attr = getattr(StorageManagerInterface, method)
            self.assertTrue(callable(cls_attr))

    def test_smtimeseries_has_method_from_db(self):
        for method in ["from_db"]:
            cls_attr = getattr(SMTimeSeries, method)
            self.assertTrue(callable(cls_attr))
        self.assertTrue(True)

    def test_smtimeseries_init_with_no_id(self):
        """ Check ths SMTimeSeries has id.
        NOTE: When checking, we should manually make sure that the id is accessible.
        """
        times = [1,2,3,4,5]
        values = [0.5, 0.3, 0.2, 0.3, 0.6]
        ts = SMTimeSeries(times, values)
        self.assertTrue(hasattr(ts, 'id') or hasattr(ts, '_id'))

    def test_smtimeseries_init_and_retrieve_with_string_id(self):
        """ Check that SMTimeSeries can be initialized with string id. """
        times = [1,2,3,4,5]
        values = [0.5, 0.3, 0.2, 0.3, 0.6]
        ts = SMTimeSeries(times, values, 'king')
        same_ts = SMTimeSeries.from_db('king')
        self.assertEqual(ts, same_ts)

    def test_smtimeseries_init_and_retrieve_with_int_id(self):
        """ Check that SMTimeSeries can be initialized with integer id. """
        times = [1,2,3,4,5]
        values = [1.5, 1.3, 1.2, 1.3, 1.6]
        ts = SMTimeSeries(times, values, 1)
        same_ts = SMTimeSeries.from_db(1)
        self.assertEqual(ts, same_ts)

    def test_smtimeseries_from_db(self):
        times = [1,2,3,4,5]
        values = [0.5, 0.3, 0.2, 0.3, 0.6]
        ts = SMTimeSeries(times, values)
        if hasattr(ts, 'id'):
            same_ts = SMTimeSeries.from_db(ts.id )
        if hasattr(ts, '_id'):
            same_ts = SMTimeSeries.from_db(ts._id )
        self.assertIsInstance(same_ts, SMTimeSeries)
        self.assertEqual(ts, same_ts)

    def test_smtimeseries_bad_init(self):
        """ This should match the spec in the StorageManagerInterface unless it is specifically
            decoupled. But then, SM should specify what it allows rather than having the user
            follow it down the StorageManager chain """
        times = [1,2,3,4,5]
        values = [2.5, 2.3, 2.2, 2.3, 2.6]
        with self.assertRaises(Exception):
            ts = SMTimeSeries(times, values, 1.5)
        with self.assertRaises(Exception):
            ts = SMTimeSeries(times, values, True)
        with self.assertRaises(Exception):
            ts = SMTimeSeries(times, values, (1,2))
        with self.assertRaises(Exception):
            ts = SMTimeSeries(times, values, [1,2])
        with self.assertRaises(Exception):
            ts = SMTimeSeries(times, values, {'1':2})

    def test_file_storage_manager_bad_init(self):
        """ Should initialize with either 1: file-descriptor or 2: str """
        with self.assertRaises(Exception):
            FileStorageManager()
        with self.assertRaises(Exception):
            FileStorageManager(101)
        with self.assertRaises(Exception):
            FileStorageManager([])
        with self.assertRaises(Exception):
            FileStorageManager({})

    def test_file_storage_manager_store_with_string(self):
        """ FileStorageManager should be able to store with a string id """
        times = [1,2,3,4,5, 6]
        values = [2.5, 2.3, 2.2, 2.3, 2.6, 3.0]
        ts = SMTimeSeries(times, values, 1.5)
        fs = FileStorageManager('test.dat')
        fs.store('great.dat', ts)

    def test_file_storage_manager_store_with_int(self):
        """ FileStorageManager should be able to store with an int id """
        times = [1,2,3,4,5, 6]
        values = [2.5, 2.3, 2.2, 2.3, 2.6, 3.0]
        fs = FileStorageManager('test.dat')
        ts = SMTimeSeries(times, values, 1.5)
        fs.store(42, ts)

    def test_file_storage_manager_store_non_ts(self):
        """ Check that storing anything other than a timeseries is bad. """
        fs = FileStorageManager('test.dat')
        with self.assertRaises(Exception):
            fs.store('baddataid', [1,2,3])
        with self.assertRaises(Exception):
            fs.store('baddata', {'dict':2})
        with self.assertRaises(Exception):
            fs.store('baddata', True)
        with self.assertRaises(Exception):
            fs.store('baddata', 1)
        with self.assertRaises(Exception):
            fs.store('baddata', 'string')

    def test_file_storage_manager_store_with_invalid_id_types(self):
        times = [1,2,3,4,5, 6]
        values = [2.5, 2.3, 2.2, 2.3, 2.6, 3.0]
        ts = SMTimeSeries(times, values, 1.5)
        fs = FileStorageManager('test.dat')
        with self.assertRaises(Exception):
            fs.store(1, ts)
        with self.assertRaises(Exception):
            fs.store(True, ts)
        with self.assertRaises(Exception):
            fs.store([], ts)
        with self.assertRaises(Exception):
            fs.store({}, ts)
        with self.assertRaises(Exception):
            fs.store(ts, ts)

    def test_file_storage_manager_size(self):
        times = [1,2,3,4,5, 6]
        values = [2.5, 2.3, 2.2, 2.3, 2.6, 3.0]
        ts = SMTimeSeries(times, values, 1.5)
        fs = FileStorageManager('test.dat')
        fs.store('great.dat', ts)
        self.assertEqual(fs.size('great.dat'), 6)

    def test_file_storage_manager_size_bad_id(self):
        fs = FileStorageManager('test.dat')
        with self.assertRaises(Exception):
            size = fs.size('unknown.dat')
            if size is None:
                raise Exception('Returning None is also valid but 0 isn\'t valid!')
        with self.assertRaises(Exception):
            size = fs.size(24)
            if size is None:
                raise Exception('Returning None is also valid but 0 isn\'t valid!')

    def test_file_storage_manager_get(self):
        """ FileStorageManager should be able to get using either string or int """
        fs = FileStorageManager('test.dat')
        ts_str = fs.get('great.dat')
        self.assertEqual(ts_str.times, [1,2,3,4,5,6])
        self.assertEqual(ts_str.values, [2.5, 2.3, 2.2, 2.3, 2.6, 3.0])
        ts_int = fs.get(42)
        self.assertEqual(ts_str.times, [1,2,3,4,5,6])
        self.assertEqual(ts_str.values, [2.5, 2.3, 2.2, 2.3, 2.6, 3.0])

    def test_file_storage_manager_get_invalid_id(self):
        """ FileStorageManager should raise some type of exception or throw none when the file is unknown. """
        fs = FileStorageManager('test.dat')
        with self.assertRaises(Exception):
            ts = fs.get('unknown.dat')
            if ts is None:
                raise Exception('Returning None is also valid!')
        with self.assertRaises(Exception):
            ts = fs.get(123)
            if ts is None:
                raise Exception('Returning None is also valid!')

    def test_file_storage_manager_get_non_int_string(self):
        """ FileStorageManager should ONLY use int or string to get back a TimeSeries """
        fs = FileStorageManager('test.dat')
        with self.assertRaises(Exception):
            ts = fs.get()
        with self.assertRaises(Exception):
            ts = fs.get(1.01)
        with self.assertRaises(Exception):
            ts = fs.get(True)
        with self.assertRaises(Exception):
            ts = fs.get([])
        with self.assertRaises(Exception):
            ts = fs.get({})
