import unittest
from student_solutions import repo

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
        print(self.group)
        self.assertTrue(True)

    def test_smtimeseries_init(self):
        """ Check ths SMTimeSeries has id.
        NOTE: When checking, we should manually make sure that the id is accessible.
        """
        times = [1,2,3,4,5]
        values = [0.5, 0.3, 0.2, 0.3, 0.6]
        ts = SMTimeSeries(times, values)
        self.assertTrue(hasattr(ts, 'id') or hasattr(ts, '_id'))

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

    def test_smtimeseries_init_with_string_id(self):
        """ Check that SMTimeSeries can be initialized with string id. """
        times = [1,2,3,4,5]
        values = [0.5, 0.3, 0.2, 0.3, 0.6]
        ts = SMTimeSeries(times, values, 'king')
        same_ts = SMTimeSeries.from_db('king')
        self.assertEqual(ts, same_ts)

    def test_smtimeseries_init_with_int_id(self):
        """ Check that SMTimeSeries can be initialized with integer id. """
        times = [1,2,3,4,5]
        values = [1.5, 1.3, 1.2, 1.3, 1.6]
        ts = SMTimeSeries(times, values, 1)
        same_ts = SMTimeSeries.from_db(1)
        self.assertEqual(ts, same_ts)

    def test_smtimeseries_init_with_float_id(self):
        """ OPTIONAL: Check that SMTimeSeries can be initialized with float id. """
        times = [1,2,3,4,5]
        values = [2.5, 2.3, 2.2, 2.3, 2.6]
        ts = SMTimeSeries(times, values, 1.5)
        same_ts = SMTimeSeries.from_db(1.5)
        self.assertEqual(ts, same_ts)

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

    def test_file_storage_manager_store(self):
        """ OPTIONAL: Check that SMTimeSeries can be initialized with float id. """
        times = [1,2,3,4,5, 6]
        values = [2.5, 2.3, 2.2, 2.3, 2.6, 3.0]
        ts = SMTimeSeries(times, values, 1.5)
        fs = FileStorageManager('test.dat')
        fs.store('thisid', ts)

    def test_file_storage_manager_store_non_ts(self):
        """ Check that storing anything other than a timeseries is bad. """
        times = [1,2,3,4,5, 6]
        fs = FileStorageManager('test.dat')
        with self.assertRaises(Exception):
            fs.store('thisid', times)

    def test_file_storage_manager_store_with_mutable_ids(self):
        times = [1,2,3,4,5, 6]
        values = [2.5, 2.3, 2.2, 2.3, 2.6, 3.0]
        ts = SMTimeSeries(times, values, 1.5)
        fs = FileStorageManager('test.dat')
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
            fs.size('unknown.dat')

    def test_file_storage_manager_get(self):
        fs = FileStorageManager('test.dat')
        ts = fs.get('great.dat')
        self.assertEqual(ts.times, [1,2,3,4,5,6])
        self.assertEqual(ts.values, [2.5, 2.3, 2.2, 2.3, 2.6, 3.0])

    def test_file_storage_manager_get_bad_id(self):
        """ FileStorageManager should """
        fs = FileStorageManager('test.dat')
        with self.assertRaises(Exception):
            ts = fs.get('unknown.dat')
            if ts == None:
                raise Exception('Returning None is also valid!')

    def test_file_storage_manager_get_non_string(self):
        """ FileStorageManager should """
        fs = FileStorageManager('test.dat')
        with self.assertRaises(Exception):
            ts = fs.get()
        with self.assertRaises(Exception):
            ts = fs.get(1)
        with self.assertRaises(Exception):
            ts = fs.get([])
        with self.assertRaises(Exception):
            ts = fs.get({})

