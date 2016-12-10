"""
NOTES:
    - Testing for completeness of the database interface rather than internal architecture due to the
        freedom given to rewrite the internal architecture however they want as long as it
        implements the RBTree. It might be wise to find a way to visualize the RB nodes
        after committing.
"""
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

    def test_set_key_with_mutable_types(self):
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
        with self.assertRaises(Exception):
            db.set(True, 'immabool')

    def test_set_key_with_immutable_types(self):
        """ OPTIONAL: Test that setting a numeric type as the key and the filename as the value is okay
            but there should be documentation around why they did that. """
        db = connect('testdb.db')
        db.set(1, 'immaint.db')
        db.set(1.111, 'immafloat.db')
        db.set((1,2), 'immatuple.db')

    def test_read_lock_behavior_non_commit_scenario(self):
        """ The db connection must commit before another connection has access to that data.
            However, the first connection has local access to its uncommitted data. """
        db1 = connect('testdb.db')
        db2 = connect('testdb.db')
        db1.set(22, 'R')
        db1.set(33, 'Python')
        db1.set(44, 'Java')
        with self.assertRaises(Exception):
            db2.get('R')
            db2.get('Python')
            db2.get('Java')
        self.assertEqual(22, db1.get('R'))
        self.assertEqual(33, db1.get('Python'))
        self.assertEqual(44, db1.get('Java'))
        db1.commit()
        self.assertEqual(db2.get('R'), 22)
        self.assertEqual(db2.get('Python'), 33)
        self.assertEqual(db2.get('Java'), 33)

    def test_simultaneos_connections_and_last_write_behavior(self):
        """ OPTIONAL + Extra Credit: The db connection will only prefer the last commit.
            You could expect that `sets` are timestamped and so the last commit was
            correct but in this functional model, it is easier to use last write.
            Simultaneous Writes are not required to be supported. """
        db1 = connect('testdb.db')
        db1.set(50, 'R')
        db2 = connect('testdb.db')
        db2.set(50, 'Python')
        db3 = connect('testdb.db')
        db3.set(50, 'Java')
        db1.commit()
        db3.commit()
        db2.commit()
        self.assertEqual(db2.get(50), 'Python')

