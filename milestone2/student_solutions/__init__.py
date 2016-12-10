import os
import sys

current_dir = os.path.dirname(__file__)


class Repo(object):

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

    def load_team8(self):
        module = os.path.join(current_dir, 'ATeamHasNoName')
        sys.path.insert(0, module)
        module = os.path.join(current_dir, 'ATeamHasNoName', 'DB')
        sys.path.insert(0, module)
        module = os.path.join(current_dir, 'ATeamHasNoName', 'SimSearch')
        sys.path.insert(0, module)

        from student_solutions.ATeamHasNoName.StorageManagerInterface import StorageManagerInterface
        from student_solutions.ATeamHasNoName.SMTimeSeries import SMTimeSeries
        from student_solutions.ATeamHasNoName.DB.DB import DB
        from student_solutions.ATeamHasNoName.SimSearch.SimilaritySearch import ccor
        db = DB()
        return {
            'StorageManagerInterface': StorageManagerInterface,
            'FileStorageManager': StorageManagerInterface,
            'SMTimeSeries': SMTimeSeries,
            'connect': db.connect,
            'ccor': ccor
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
        if group == 'ecnc':
            return self.load_team4()
        if group == 'ATeamHasNoName':
            return self.load_team8()
        if group == 'jovhscript':
            return self.load_team9()

repo = Repo()
