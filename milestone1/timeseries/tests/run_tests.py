# run this file to obtain test stats + a score for a specific repo

import os
import sys

# Since the real run directory is set here, we need to add it to the PYTHON_PATH dynamically 
run_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_directory, 'timeseries'))

print('run_test.py ', run_directory)
        
import unittest
import all_tests

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromModule(all_tests)
    tr = unittest.TextTestRunner(verbosity=0, descriptions=False,buffer=True).run(suite)

    # New Rubric will be broken down into:
    # TimeSeries (60):
    # OOP (20):
    # Streaming TS (30):
    counter = {
        '#ts': 0,
        '#lz': 0,
        '#oop': 0,
        '#sts': 0,
        '#doc': 0
    }

    for score in all_tests.scores:
        key = score[0]
        if key not in counter.keys():
            raise Exception('Invalid Score. Please Fix! %s' %(key))
        counter[key] += 1

    print('-----------------------------------')
    for group, points in counter.items():
        print('{} score: {} P'.format(group, points))
    print('-----------------------------------')
    print('stats:')
    print('-----------------------------------')
    print('errors: \t{}'.format(len(tr.errors)))
    print('failures: \t{}'.format(len(tr.failures)))
    print('score stats:')

    total_score = 0
    for score in all_tests.scores:
        print('{}:\t{}\t{} P'.format(score[0], score[1][:100], score[2]))
    print('-----------------------------------')
    print('total score: {} P out of {} '.format(sum(counter.values()), all_tests.total_scores))
