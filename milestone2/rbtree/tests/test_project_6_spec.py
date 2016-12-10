import unittest
from student_solutions import repo

SCORE = 0
TOTAL_SCORE = 0

class MainTest(unittest.TestCase):

    group = None

    def setUp(self):
        global StorageManagerInterface
        global SMTimeSeries
        global connect
        StorageManagerInterface = repo[self.group]["StorageManagerInterface"]
        SMTimeSeries = repo[self.group]["SMTimeSeries"]
        connect = repo[self.group]["connect"]

    def test_connect_creates_new_file(self):
        """ Test the connection method and make sure it works with a local file. """
        db = connect('testdb.db')

    def test_get_on_invalid_key(self):
        db = connect('testdb.db')
        with self.assertRaises(Exception):
            value = db.get('badkey')
            if value == None:
                raise Exception("Check that documentation expects this.")

    def test_set_string_key_string_value(self):
        """ Test that setting and then getting returns the expected value"""
        db = connect('testdb.db')
        db.set('rahul', 'professor')
        self.assertEqual('professor', db.get('rahul'))

    def test_set_duplicate_string_key_string_value(self):
        """ Test that setting a key again overrides the previous value """
        db = connect('testdb.db')
        db.set('rahul', 'professor')
        db.set('rahul', 'scholar')
        self.assertEqual('scholar', db.get('rahul'))

    def test_set_key_with_mutable_type(self):
        """ Test that setting a key with a mutable object should throw.
            This is bad because the object is mutable so your key is no longer unique """
        db = connect('testdb.db')
        with self.assertRaises(Exception):
            db.set([], 'immalist')
        with self.assertRaises(Exception):
            db.set({}, 'immadict')
        with self.assertRaises(Exception):
            class King(object):
                pass
            obj = King()
            db.set(obj, 'immaobject')

    @unittest.skip
    def test_set_key_with_immutable_types(self):
        """ OPTIONAL: Test that setting a key with an immutable type is either okay or throws an Error
            depending on the teams documentation. """
        db = connect('testdb.db')
        db.set(1, 'immanum')
        db.set(1.111, 'immanum')
        db.set((1,2), 'immatuple')
        db.set(True, 'immabool')

    '''
    def test_lock_behavior(self):
        """ OPTIONAL: Test that setting a key with an immutable type is either okay or throws an Error
            depending on the teams documentation. """
        db = connect('testdb.db')

        db.set(1, 'immanum')
        db.set(1.111, 'immanum')
        db.set((1,2), 'immatuple')
        db.set(True, 'immabool')
    '''
