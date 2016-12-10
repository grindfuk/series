import unittest
from io import StringIO
from tests.test_project_6_spec import MainTest as t6
from tests.test_project_7_spec import MainTest as t7
from tests.test_project_8_spec import MainTest as t8
from pprint import pprint

TEAM = 'jovhscript'


VERBOSITY = 2

def run6(runner, team):
    t6.group = team
    result = runner.run(unittest.makeSuite(t6))
    print('Test Project 6:', 100 * (result.testsRun/(result.testsRun + len(result.errors))), '%')
    print('Test Run', result.testsRun)
    print('Test Errors')
    for e in result.errors:
        for ea in e:
            print(ea)

def run7(runner, team):
    t7.group = team
    result = runner.run(unittest.makeSuite(t7))
    print('Test Project 7:', 100 * (result.testsRun/(result.testsRun + len(result.errors))), '%')
    print('Test Run', result.testsRun)
    print('Test Errors')
    for e in result.errors:
        for ea in e:
            print(ea)

def run8(runner, team):
    t8.group = team
    result = runner.run(unittest.makeSuite(t8))
    print('Test Project 8:', 100 * (result.testsRun/(result.testsRun + len(result.errors))), '%')
    print('Test Run', result.testsRun)
    print('Test Errors')
    for e in result.errors:
        for ea in e:
            print(ea)

runner = unittest.TextTestRunner(verbosity=VERBOSITY)
run7(runner, TEAM)
