import unittest
from io import StringIO
import os
import sys
from pprint import pprint

sys.path.insert(0, os.getcwd())

try:
    from tests.test_project_6_spec import MainTest as t6
    from tests.test_project_7_spec import MainTest as t7
    from tests.test_project_8_spec import MainTest as t8
except:
    from test_project_6_spec import MainTest as t6
    from test_project_7_spec import MainTest as t7
    from test_project_8_spec import MainTest as t8

TEAM = 'jovhscript'

VERBOSITY = 2

def run6(runner, team):
    t6.group = team
    result = runner.run(unittest.makeSuite(t6))
    print('Test Project 6:', 100 * (result.testsRun/(result.testsRun + len(result.errors))), '%')
    print('Test Run', result.testsRun)
    return 

def run7(runner, team):
    t7.group = team
    result = runner.run(unittest.makeSuite(t7))
    print('Test Project 7:', 100 * (result.testsRun/(result.testsRun + len(result.errors))), '%')
    print('Test Run', result.testsRun)

def run8(runner, team):
    t8.group = team
    result = runner.run(unittest.makeSuite(t8))
    print('Test Project 8:', 100 * (result.testsRun/(result.testsRun + len(result.errors))), '%')
    print('Test Run', result.testsRun)

if __name__ == '__main__':
    if len(sys.argv) >  1:
    	TEAM = sys.argv[1]
    runner = unittest.TextTestRunner(verbosity=VERBOSITY)
    run6(runner, TEAM)
    run7(runner, TEAM)
    run8(runner, TEAM)
