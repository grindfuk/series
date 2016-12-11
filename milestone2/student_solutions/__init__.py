import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))


class Repo(object):

    def load_team1(self):
        module = os.path.join(current_dir, 'slac207')
        sys.path.insert(0, module)
        module = os.path.join(current_dir, 'slac207', 'timeseries')
        sys.path.insert(0, module)
        module = os.path.join(current_dir, 'slac207', 'tsbtreedb')
        sys.path.insert(0, module)

        from student_solutions.slac207.timeseries.Timeseries import TimeSeries
        from student_solutions.slac207.timeseries.SMTimeSeries import SMTimeSeries
        from student_solutions.slac207.timeseries.StorageManager import FileStorageManager, StorageManagerInterface
        from student_solutions.slac207.cs207rbtree.RedBlackTree import DBDB

        def connect(dbname):
            try:
                f = open(dbname, 'r+b')
            except IOError:
                fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
                f = os.fdopen(fd, 'r+b')
            return DBDB(f)

        def stand(*args, **kwargs):
            raise Exception('Missing Function stand or equivalent')

        def ccor(*args, **kwargs):
            raise Exception('Missing Function ccor or equivalent')

        def max_corr_at_phase(*args, **kwargs):
            raise Exception('Missing Function max_corr_at_phase or equivalent')

        def kernel_corr(*args, **kwargs):
            raise Exception('Missing Function kernel_corr or equivalent')

        return {
            'StorageManagerInterface': StorageManagerInterface,
            'FileStorageManager': FileStorageManager,
            'SMTimeSeries': SMTimeSeries,
            'TimeSeries': TimeSeries,
            'connect': connect,
            'stand': stand,
            'ccor': ccor,
            'kernel_corr': kernel_corr,
            'max_corr_at_phase': max_corr_at_phase
        }

    def load_team2(self):
        print('NOTE: Add __init__.py to root directory since cs207project\storagemanager\smtimeseries.py calls it')
        module = os.path.join(current_dir, 'gitrdone4', 'cs207project')
        sys.path.insert(0, module)
        # module = os.path.join(current_dir, 'gitrdone4', 'cs207project', 'rbtree')
        # sys.path.insert(0, module)
        # module = os.path.join(current_dir, 'gitrdone4', 'cs207project', 'simsearch')
        # sys.path.insert(0, module)
        # module = os.path.join(current_dir, 'gitrdone4', 'cs207project', 'storagemanager')
        # sys.path.insert(0, module)
        module = os.path.join(current_dir, 'gitrdone4', 'cs207project', 'timeseries')
        sys.path.insert(0, module)
        # module = os.path.join(current_dir, 'gitrdone4', 'cs207project', 'tsbtreedb_for_team4')
        module = os.path.join(current_dir, 'gitrdone4')
        sys.path.insert(0, module)

        from cs207project.storagemanager.smtimeseries import SMTimeSeries
        from cs207project.storagemanager.storagemanagerinterface import StorageManagerInterface
        from cs207project.storagemanager.filestoragemanager import FileStorageManager
        from cs207project.timeseries.timeseries import TimeSeries
        from cs207project.simsearch._corr import (stand, ccor, kernel_corr, max_corr_at_phase)
        from cs207project.rbtree.redblackDB import connect

        return {
            'StorageManagerInterface': StorageManagerInterface,
            'FileStorageManager': FileStorageManager,
            'SMTimeSeries': SMTimeSeries,
            'TimeSeries': TimeSeries,
            'connect': connect,
            'stand': stand,
            'ccor': ccor,
            'kernel_corr': kernel_corr,
            'max_corr_at_phase': max_corr_at_phase
        }

    def load_team3(self):
        print("NOTE: The tsbtreedb has a bad sys.path ammend in the correlation.py file.")
        print("The imports are not consistent which is bad and we have to hack around it")

        module = os.path.join(current_dir, 'cs207-2016', 'timeseries')
        assert(os.path.exists(module))
        sys.path.insert(0, module)
        from storage_manager import SMTimeSeries, StorageManagerInterface, FileStorageManager
        from timeseries import TimeSeries
        sys.path.remove(module)

        module = os.path.join(current_dir, 'cs207-2016')
        assert(os.path.exists(module))
        sys.path.insert(0, module)

        from importlib import reload
        import timeseries
        reload(timeseries)

        from tsbtreedb.correlation import correlation
        from tsbtreedb.lab10 import connect
        correlation_cls = correlation()

        return {
            'StorageManagerInterface': StorageManagerInterface,
            'FileStorageManager': FileStorageManager,
            'SMTimeSeries': SMTimeSeries,
            'TimeSeries': TimeSeries,
            'connect': connect,
            'stand': correlation_cls.stand,
            'ccor': correlation_cls.ccor,
            'kernel_corr': correlation_cls.kernel_corr,
            'max_corr_at_phase': correlation_cls.max_corr_at_phase
        }

    def load_team4(self):
        module = os.path.join(current_dir, 'ecnc')
        sys.path.insert(0, module)
        module = os.path.join(current_dir, 'ecnc', 'timeseries')
        sys.path.insert(0, module)
        module = os.path.join(current_dir, 'ecnc', 'tsbtreedb')
        sys.path.insert(0, module)

        from student_solutions.ecnc.timeseries.StorageManagerInterface import StorageManagerInterface
        from student_solutions.ecnc.timeseries.SMTimeSeries import SMTimeSeries
        from student_solutions.ecnc.timeseries.TimeSeries import TimeSeries
        from student_solutions.ecnc.tsbtreedb.unbalancedDB import connect
        from student_solutions.ecnc.tsbtreedb.crosscorr import ccor, max_corr_at_phase, kernel_corr, standardize
        from student_solutions.ecnc.timeseries.FileStorageManager import FileStorageManager
        def stand(x,y,z):
            return standardize(x)
        return {
            'StorageManagerInterface': StorageManagerInterface,
            'FileStorageManager': FileStorageManager,
            'SMTimeSeries': SMTimeSeries,
            'TimeSeries': TimeSeries,
            'connect': connect,
            'stand': stand,
            'ccor': ccor,
            'kernel_corr': kernel_corr,
            'max_corr_at_phase': max_corr_at_phase
        }

    def load_team5(self):
        # Might need to add __init__.py to directories here
        print('NOTE: Please add __init__.py to p7_simsearch')

        module = os.path.join(current_dir, 'glacierscse')
        assert(os.path.exists(module))
        sys.path.insert(0, module)

        from timeseries.StorageManagerInterface import StorageManagerInterface
        from timeseries.FileStorageManager import FileStorageManager
        from timeseries.SMTimeSeries import SMTimeSeries
        from timeseries.TimeSeries import TimeSeries
        from timeseries.cs207rbtree import connect

        from p7_simsearch.calculateDistance import stand, ccor, kernel_corr, max_corr_at_phase

        return {
            'StorageManagerInterface': StorageManagerInterface,
            'FileStorageManager': FileStorageManager,
            'SMTimeSeries': SMTimeSeries,
            'TimeSeries': TimeSeries,
            'connect': connect,
            'stand': stand,
            'ccor': ccor,
            'kernel_corr': kernel_corr,
            'max_corr_at_phase': max_corr_at_phase
        }

    def load_team6(self):
        module = os.path.join(current_dir, 'CSE-O1')
        assert(os.path.exists(module))
        sys.path.insert(0, module)

        module = os.path.join(current_dir, 'CSE-O1', 'cs207rbtree')
        assert(os.path.exists(module))
        sys.path.insert(0, module)

        module = os.path.join(current_dir, 'CSE-O1', 'timeseries')
        assert(os.path.exists(module))
        sys.path.insert(0, module)

        from timeseries.SMTimeSeries import SMTimeSeries
        from timeseries.TimeSeries import TimeSeries
        from timeseries.TimeSeriesDistance import stand, ccor, kernel_corr, max_corr_at_phase
        from storagemanager.SMInterface import StorageManagerInterface
        from storagemanager.FileStorageManager import FileStorageManager
        from cs207rbtree.database import connect

        return {
            'StorageManagerInterface': StorageManagerInterface,
            'FileStorageManager': FileStorageManager,
            'SMTimeSeries': SMTimeSeries,
            'TimeSeries': TimeSeries,
            'connect': connect,
            'stand': stand,
            'ccor': ccor,
            'kernel_corr': kernel_corr,
            'max_corr_at_phase': max_corr_at_phase
        }

    def load_team7(self):

        module = os.path.join(current_dir, 'rubix-cube')
        assert(os.path.exists(module))
        sys.path.insert(0, module)

        # This dir is nested!
        module = os.path.join(current_dir, 'rubix-cube', 'cs207rbtree')
        assert(os.path.exists(module))
        sys.path.insert(0, module)

        from timeseries.SMTimeSeries import SMTimeSeries
        from timeseries.TimeSeries import TimeSeries
        from timeseries.calculateDistance import stand, ccor, kernel_corr, max_corr_at_phase
        from timeseries.StorageManagerInterface import StorageManagerInterface
        from timeseries.FileStorageManager import FileStorageManager
        from cs207rbtree import connect

        return {
            'StorageManagerInterface': StorageManagerInterface,
            'FileStorageManager': FileStorageManager,
            'SMTimeSeries': SMTimeSeries,
            'TimeSeries': TimeSeries,
            'connect': connect,
            'stand': stand,
            'ccor': ccor,
            'kernel_corr': kernel_corr,
            'max_corr_at_phase': max_corr_at_phase
        }

    def load_team8(self):
        print('NOTE: Please add __init__.py to SimSearch Directory')
        print('NOTE: Please add __init__.py to DB Directory')
        print('NOTE: Please add __init__.py to DB ATeamHasNoName')

        module = os.path.join(current_dir, 'ATeamHasNoName')
        sys.path.insert(0, module)
        module = os.path.join(current_dir, 'ATeamHasNoName', 'DB')
        sys.path.insert(0, module)
        module = os.path.join(current_dir, 'ATeamHasNoName', 'SimSearch')
        sys.path.insert(0, module)

        from student_solutions.ATeamHasNoName.StorageManagerInterface import StorageManagerInterface
        from student_solutions.ATeamHasNoName.SMTimeSeries import SMTimeSeries
        from student_solutions.ATeamHasNoName.TimeSeries import TimeSeries
        from student_solutions.ATeamHasNoName.DB.DB import DB
        from student_solutions.ATeamHasNoName.SimSearch.SimilaritySearch import stand, ccor, kernel_corr, max_corr_at_phase

        db = DB()
        return {
            'StorageManagerInterface': StorageManagerInterface,
            'FileStorageManager': StorageManagerInterface,
            'SMTimeSeries': SMTimeSeries,
            'TimeSeries': TimeSeries,
            'connect': db.connect,
            'stand': stand,
            'ccor': ccor,
            'kernel_corr': kernel_corr,
            'max_corr_at_phase': max_corr_at_phase
        }

    def load_team9(self):

        module = os.path.join(current_dir, 'jovhscript')
        sys.path.insert(0, module)
        module = os.path.join(current_dir, 'jovhscript', 'timeseries')
        sys.path.insert(0, module)
        module = os.path.join(current_dir, 'jovhscript', 'timeseries', 'Similarity')
        sys.path.insert(0, module)

        from student_solutions.jovhscript.timeseries.series import SMTimeSeries, TimeSeries
        from student_solutions.jovhscript.timeseries.interfaces import StorageManagerInterface
        from student_solutions.jovhscript.timeseries.Similarity.BinarySearchDatabase import connect
        from student_solutions.jovhscript.timeseries.Similarity.distances import stand, ccor, kernel_corr, max_corr_at_phase
        from student_solutions.jovhscript.timeseries.FileStorageManager import FileStorageManager

        return {
            'StorageManagerInterface': StorageManagerInterface,
            'FileStorageManager': FileStorageManager,
            'SMTimeSeries': SMTimeSeries,
            'TimeSeries': TimeSeries,
            'connect': connect,
            'stand': stand,
            'ccor': ccor,
            'kernel_corr': kernel_corr,
            'max_corr_at_phase': max_corr_at_phase
        }

    def __getitem__(self, group):
        if group == 'slac207':
            return self.load_team1()
        if group == 'gitrdone4':
            return self.load_team2()
        if group == 'cs207-2016':
            return self.load_team3()
        if group == 'ecnc':
            return self.load_team4()
        if group == 'glacierscse':
            return self.load_team5()
        if group == 'CSE-01':
            return self.load_team6()
        if group == 'rubix-cube':
            return self.load_team7()
        if group == 'ATeamHasNoName':
            return self.load_team8()
        if group == 'jovhscript':
            return self.load_team9()

repo = Repo()

if __name__ == "__main__":
    sys.path.insert(0, './')
    sys.path.insert(0, './student_solutions')
    # repo['slac207'] # Working
    # repo['gitrdone4'] # Working
    # repo['cs207-2016'] # Working
    # repo['ecnc'] # Working
    # repo['glacierscse'] # Working
    # repo['CSE-01'] # Working
    # repo['rubix-cube'] # Working
    # repo['ATeamHasNoName'] # Working
    # repo['jovhscript'] # Working
