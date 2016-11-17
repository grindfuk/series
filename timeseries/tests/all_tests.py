# Combined tests for all labs to run on Milestone I

import logging
import unittest
import numpy as np

# for computing hamming distance
import distance

import os

# list of tuples
# (Lab, testinfo, points)
scores = []

__unittest = True

import sys
import shutil

# importing should also scored...


import_fail = False

# this is correct
try:
  import timeseries.TimeSeries as TimeSeries
  #scores.append( ('General', 'correct package', 5))
except:
  print('TimeSeries import error!')
  import_fail = True

try:
  # import lazy decorator
  from timeseries import lazy
except:
  print('lazy could not be imported')


# fix for team: cs207-project
try:
  from TimeSeries import TimeSeries
  from lazy import lazy
except:
  pass

# Combined tests for all labs to run on Milestone I

# Lab10 tests...
class TestTSBasics(unittest.TestCase):

  def test_init1(self):
    '''__init__ constructor should take any sequence-like thing.'''
    t = TimeSeries([], [])

    # different lengths should not be allowed
    with self.assertRaises((Exception, AssertionError, ValueError)):
      t = TimeSeries([1.0, 2], [])

    with self.assertRaises((Exception, AssertionError, ValueError)):
      t = TimeSeries([], [1.])

    scores.append(('#ac Lab10', 'init wrong len', 2))
  def test_init2(self):
    # wrong init parameters
    with self.assertRaises(Exception):
      t = TimeSeries() # Empty not okay. Zero-length is.
    with self.assertRaises(Exception):
      t = TimeSeries(42) # Non-sequence initialization.
    with self.assertRaises(Exception):
      t = TimeSeries(42, 42) # Non-sequence initialization.
    scores.append(('#ac Lab10', 'init wrong vals', 2))


  def test_len2(self):

    with self.assertRaises(Exception):
      self.assertEqual(len(TimeSeries()), 0)
    scores.append(('#ac Lab10', 'len excep', 1))
  def test_len3(self):
    self.assertEqual(len(TimeSeries([], [])), 0)
    self.assertEqual( len(TimeSeries([1,2,3], [1, 2, 3])), 3 )
    self.assertEqual( TimeSeries([1,2,3], [1, 2, 3]).__len__(), 3 )
    scores.append(('#ac Lab10', 'len base', 1))

  def test_getitem1(self):
    t = TimeSeries([1.5, 2.5, 3.5, 7.0], [0.1, 0.2, 0.3, 0.4])

    self.assertEqual(t[1.5], 0.1)
    self.assertEqual(t.__getitem__(3.5), 0.3)

    scores.append(('#ac Lab10', 'getitem base', 1))
  def test_getitem2(self):
    t = TimeSeries([1.5, 2.5, 3.5, 7.0], [0.1, 0.2, 0.3, 0.4])
    with self.assertRaises(IndexError):
      self.assertEqual(t[-1], 0)

    with self.assertRaises(IndexError):
      self.assertEqual(t[400.], 0)

    scores.append(('#ac Lab10', 'getitem excep', 1))
  def test_getitem3(self):
    t = TimeSeries([1.5, 2.5, 3.5, 7.0], [0.1, 0.2, 0.3, 0.4])
    # test float with a bit of tolerenace, this should work!
    self.assertEqual(t[7.0 + 10**(-15)], 0.4)   
    self.assertEqual(t[7.0 - 10**(-15)], 0.4)   
    scores.append(('#ac Lab10', 'getitem get adv', 5))

  def test_setitem1(self):
    t = TimeSeries([1.5, 2.5, 3.5, 7.0], [0.1, 0.2, 0.3, 0.4])

    t[1.5] = -0.9
    self.assertEqual(t[1.5], -0.9)
    t[3.5] = 0.0
    self.assertEqual(t.__getitem__(3.5), 0.0)
    scores.append(('#ac Lab10', 'setitem base', 1))

  def test_setitem2(self):
    t = TimeSeries([1.5, 2.5, 3.5, 7.0], [0.1, 0.2, 0.3, 0.4])
    with self.assertRaises(IndexError):
      t[-1] = 0.0

    with self.assertRaises(IndexError):
      t[400.0] = 10.0
    scores.append(('#ac Lab10', 'setitem excep', 1))

  def test_setitem3(self):
    t = TimeSeries([1.5, 2.5, 3.5, 7.0], [0.1, 0.2, 0.3, 0.4])
    # test float with a bit of tolerenace, this should work!
    # try/except as no assertNotRaises(...) exists...s
    try:
      t[7.0 + 10**(-15)] = 0.8
      self.assertEqual(t[7.0 + 10**(-15)], 0.8)
      t[7.0 - 10**(-15)] = 0.9
      self.assertEqual(t[7.0 - 10**(-15)], 0.9)  
    except:
      # indicate that this failed
      self.assertTrue(False)
    scores.append( ('#ac Lab10', 'setitem adv', 5))
 

  def test_str1(self):
    for stype in (str,repr):
      # Check short strings are handled
      s = stype(TimeSeries([1,2,3], [4, 5, 6]))
      self.assertNotEqual(s,'')
      self.assertTrue(len(s)<1000)
      # Check long strings are abbreviated
      s = stype(TimeSeries(list(range(0,100000)), list(range(0,100000))))
      self.assertNotEqual(s,'')
      self.assertTrue(len(s)<1000)

    scores.append( ('#ac Lab10', 'str base', 1))

  def test_str2(self):
      # We're not super mean here. If they've done *any* abbreviation, we're happy.
    # Make sure they actually tried something different, though.
    x = TimeSeries(list(range(0,100000)), list(range(0,100000)))
    self.assertNotEqual(str(x), repr(x))
    scores.append( ('#ac Lab10', 'str long', 1))

  def test_str3(self):
    x = TimeSeries(list(range(0,100000)), list(range(0,100000)))
    # check that hamming distance is larger than 6!
    # there should be some difference showing they understood
    # str / repr difference
    min_length = min(len(str(x)), len(repr(x)))
    diff_length = abs(len(str(x)) - len(repr(x)))
    strstr = str(x)
    reprstr = repr(x)
    self.assertGreater(distance.hamming(strstr[:min_length], reprstr[:min_length]) + diff_length, 6)
    scores.append( ('#ac Lab10', 'str != repr', 1))  

  def test_contains1(self):
    t = TimeSeries([0.1, 0.2, 0.3, 0.4], [1, 2, 3, 4])

    self.assertTrue(0.2 in t)
    self.assertTrue(t.__contains__(0.1))
    self.assertFalse(42 in t)
    self.assertFalse(t.__contains__(-10))
    scores.append( ('#ac Lab10', 'test contains', 1))  


  def test_contains2(self):
    t = TimeSeries([0.1, 0.2, 0.3, 0.4], [1, 2, 3, 4])

    with self.assertRaises(TypeError):
      'Hello World!' in t
    scores.append( ('#ac Lab10', 'test contains', 1))  

  def test_iter(self):
    vals = [1, 2, 3, 4]
    t = TimeSeries([0.1, 0.2, 0.3, 0.4], vals)

    pos = 0
    for v in t:
      self.assertEqual(v, vals[pos])
      pos+=1
    scores.append( ('#ac Lab10', 'test iter', 2))  

  def test_properties(self):
    times = [0.1, 0.2, 0.3, 0.4]
    vals = [1, 2, 3, 4]
    t = TimeSeries(times, vals)

    self.assertEqual(list(t.times()), times)
    self.assertEqual(list(t.values()), vals)
    self.assertEqual(list(t.items()), [(0.1, 1), (0.2, 2), (0.3, 3), (0.4, 4)])
    scores.append( ('#ac Lab10', 'test properties', 1))  

class TestTSInterpolation(unittest.TestCase):
  def testInterpolation1(self):
    a = TimeSeries([0,5,10], [1,2,3])
    b = TimeSeries([2.5,7.5], [100, -100])
    # Simple cases as given
    ares = a.interpolate([1])
    self.assertEqual(ares.values()[0], 1.2)
    self.assertEqual(ares.times()[0], 1)
    ares = a.interpolate(b.times())
    self.assertEqual(list(ares.values()), [1.5, 2.5])
    self.assertEqual(list(ares.times()), [2.5,7.5])
    scores.append( ('#ar Lab10', 'test interpol base', 3)) 
  def testInterpolation2(self):
    a = TimeSeries([0,5,10], [1,2,3])
    b = TimeSeries([2.5,7.5], [100, -100])
    # Boundary conditions
    ares = a.interpolate([-100, 100])
    self.assertEqual(list(ares.values()), [1, 3])
    self.assertEqual(list(ares.times()), [-100, 100])
    scores.append( ('#ar Lab10', 'test interpol boundary', 3)) 
  def testInterpolation3(self):
    a = TimeSeries([0,5,10], [1,2,3])
    b = TimeSeries([2.5,7.5], [100, -100])
    # empty case
    ares = a.interpolate([])
    self.assertEqual(list(ares.values()), [])
    self.assertEqual(list(ares.times()), [])
    scores.append( ('#ar Lab10', 'test interpol empty', 1)) 

class TestTSLaziness(unittest.TestCase):
  def testLazy1(self):
    x = TimeSeries([1,2,3,4],[1,4,9,16]) 

    self.assertEqual(str(x), str(x.lazy.eval()))
    scores.append( ('#lz Lab10', 'test lazy base', 3))    

  def testCheckLength(self):

    @lazy
    def check_length(a, b):
      return len(a) == len(b)

    thunk = check_length(TimeSeries(range(0, 4), range(1, 5)), TimeSeries(range(0, 4), range(1, 5)))
    self.assertEqual(thunk.eval(), True)
    scores.append( ('#lz Lab10', 'test lazy base', 1)) 

  def testLazy2(self):
    # check recursive lazy operations
    @lazy
    def ladd(a, b):
      return a + b

    @lazy
    def lequal(a, b):
      return a == b
    @lazy 
    def check_length2(a, b, c):
      return lequal(ladd(len(a), len(b)), ladd(len(b), len(c))).eval()

    thunk2 = check_length2(TimeSeries(range(0, 4), range(1, 5)), \
         TimeSeries(range(0, 4), range(1, 5)), \
         TimeSeries(range(5, 9), range(2, 6)))
    self.assertEqual(thunk2.eval(), True)

    scores.append( ('#lz Lab10', 'test lazy recursive', 3)) 

# Lab11 tests...
class TestTSMean(unittest.TestCase):

  def testMean1(self):
    t = TimeSeries([1], [-10])
    self.assertEqual(t.mean(), -10)
    scores.append( ('#ar Lab11', 'mean base', 1))
  def testMean2(self):

    t = TimeSeries([1, 2], [1, 2])
    self.assertEqual(t.mean(), 1.5)
    scores.append( ('#ar Lab11', 'mean base2', 1))

  def testMean3(self):
    t = TimeSeries([1, 2, 3, 4], [1, 2, 3, 4])
    # self.assertEqual(t.mean(), np.array([1, 2, 3, 4]).mean())
    self.assertEqual(t.mean(), np.array([1, 2, 3, 4]).mean())
    scores.append( ('#ar Lab11', 'mean gen', 1))

  def testMean4(self):
    # assert edge cases...
    with self.assertRaises(Exception):
      t = TimeSeries([],[])
      t.mean()
    scores.append( ('#ar Lab11', 'mean excep', 2))


# Lab12 tests..
class TestTSIterators(unittest.TestCase):

  def testIteratators1(self):

    time_vals = [1, 2, 3, 4]
    vals = [0.1, 0.2, 0.3, 0.4]
    t = TimeSeries(time_vals, vals)

    # iterate over times
    pos = 0
    for time in t.itertimes():
      self.assertEqual(time, time_vals[pos])
      pos += 1
    scores.append( ('#ac Lab12', 'itertimes', 1))

  def testIteratators2(self):

    time_vals = [1, 2, 3, 4]
    vals = [0.1, 0.2, 0.3, 0.4]
    t = TimeSeries(time_vals, vals)

    # iterate over values
    pos = 0
    for val in t.itervalues():
      self.assertEqual(val, vals[pos])
      pos += 1
    scores.append( ('#ac Lab12', 'itervals', 1))

  def testIteratators3(self):

    time_vals = [1, 2, 3, 4]
    vals = [0.1, 0.2, 0.3, 0.4]
    t = TimeSeries(time_vals, vals)
    # iterate over items
    pos = 0
    for item in t.iteritems():
      self.assertEqual(item, (time_vals[pos], vals[pos]))
      pos += 1
    scores.append( ('#ac Lab12', 'itertimes', 1))

# Lab 15 tests...
class TestTSUnaryyOperators(unittest.TestCase):

  def testOps1(self):
    t_a = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
    self.assertTrue(+t_a == t_a)
    scores.append( ('#ar Lab15', 'unary+', 1))

  def testOps2(self):
    t_a = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
    #t_b = TimeSeries([1, 2, 3, 4], np.array([-0.1, -0.2, -0.3, -0.4]))
    t_b = TimeSeries([1, 2, 3, 4], [-0.1, -0.2, -0.3, -0.4])
    self.assertTrue(-t_a == t_b)
    scores.append( ('#ar Lab15', 'unary-', 1))

  def testOps3(self):
    ts_a = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
    self.assertTrue(bool(ts_a))
    scores.append(('#ar Lab15', 'bool', 1))

  def testOps4(self):
    t_a = TimeSeries([1, 2], [20., -9.])
    self.assertEqual(abs(t_a), list(np.sqrt([20. * 20. + 9 * 9])))
    scores.append(('#ar Lab15', 'abs', 1))

  def testOps5(self):
    with self.assertRaises(Exception):
      abs(TimeSeries([], []))
    scores.append( ('#ar Lab15', 'abs empty', 2))

class TestTSBinaryOperators(unittest.TestCase):

  def testEq1(self):
    t_a = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
    # ats = ArrayTimeSeries
    # t_b = TimeSeries([1, 2, 3, 4], np.array([0.1, 0.2, 0.3, 0.4]))
    t_c = TimeSeries([1, 2, 3, 4], [0.5, 0.2, 0.9, 0.4])

    # self.assertEqual(t_a, t_b)
    self.assertNotEqual(t_a, t_c)
    scores.append(('#ac Lab15', 'eq base', 1))

  def testEq2(self):
    t_a = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
    # t_b = TimeSeries([1, 2, 3, 4], np.array([0.1, 0.2, 0.3, 0.4]))
    t_c = TimeSeries([1, 2, 3, 4], [0.5, 0.2, 0.9, 0.4])
    t_d = TimeSeries([-10, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
    t_e = TimeSeries([1, 2, 3], [0.5, 0.2, 0.9])
    t_f = TimeSeries([], [])
    with self.assertRaises(ValueError):
      t_a == t_d
    with self.assertRaises(ValueError):
      t_e == t_d
    with self.assertRaises(ValueError):
      t_e == t_f
    with self.assertRaises(ValueError):
      t_a == t_f
    with self.assertRaises(TypeError):
      t_a == 4

    scores.append( ('#ac Lab15', 'eq value err', 2))

  def testEq3(self):
    t_a = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
    with self.assertRaises(NotImplementedError):
      t_a == [1, 2, 3, 4]
    with self.assertRaises(NotImplementedError):
      t_a == np.array([1, 2, 3, 4])
    scores.append( ('#ac Lab15', 'eq not impl err', 1))

  def testSub1(self):
    t_a = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
    #t_b = TimeSeries([1, 2, 3, 4], np.array([0.1, 0.2, 0.3, 0.4]))
    t_b = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
    t_c = TimeSeries([1, 2, 3, 4], [0.0, 0.0, 0.0, 0.0])
    t_d = TimeSeries([1, 2, 3, 4], [-0.9, -0.8, -0.7, -0.6])
    t_e = TimeSeries([1, 2, 3], [0.5, 0.2, 0.9])
    t_f = TimeSeries([], [])

    self.assertEqual(t_a - t_b, t_c)

    scores.append(('#ar Lab15', 'sub base', 1))


    # to avoid errors be here maybe a bit more generous...
    # i.e. allow besides TypeErrors also NotImplemented
    # here separate into individual test cases!
  def testSub2(self):
    t_a = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
    with self.assertRaises(TypeError):
      t_a - 'Hello'

  def test_multiplication_with_valid_length_timeseries(self):
    ts_a = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
    ts_b = TimeSeries([1, 2, 3, 4], [2.0, 3.0, 3.0, 2.0])
    ts_c = TimeSeries([1, 2, 3, 4], [0.2, 0.6, 0.9, 0.8])

    self.assertEqual(ts_a * ts_b, ts_c)
    scores.append(('#ar Lab15', 'mul base', 1))

    # to avoid errors be here maybe a bit more generous...
    # i.e. allow besides TypeErrors also NotImplemented
    # here separate into individual test cases!
  def testMul2(self):
    t_a = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
    with self.assertRaises(TypeError):
      t_a * 'Hello'

    scores.append( ('#ar Lab15', 'mul adv', 3))

  def testMul3(self):
    t_a = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
    with self.assertRaises(NotImplementedError):
      t_a * [1, 2, 3, 4]
    with self.assertRaises(NotImplementedError):
      t_a * np.array([1, 2, 3, 4])

    scores.append( ('#ar Lab15', 'mul not impl', 1))

  def testMul4(self):
    t_a = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
    t_d = TimeSeries([1, 2, 3, 4], [0.2, 0.4, 0.6, 0.8])

    val = 2
    val = int(val)

    self.assertEqual(t_a * val, t_d)
    scores.append(('#ar Lab15', 'mul + int val', 2))

  def testMul6(self):
    t_a = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
    t_d = TimeSeries([1, 2, 3, 4], [0.2, 0.4, 0.6, 0.8])

    val = 2
    val = float(val)
    self.assertEqual(t_a * val, t_d)
    scores.append(('#ar Lab15', 'mul + float val', 1))

  def testMul7(self):
    t_a = TimeSeries([1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4])
    t_e = TimeSeries([1, 2, 3], [0.5, 0.2, 0.9])
    t_f = TimeSeries([], [])

    with self.assertRaises(ValueError):
      t_a * t_e
    with self.assertRaises(ValueError):
      t_a * t_f

    scores.append( ('#ar Lab15', 'mul + val err', 2))


class TestTimeSeriesDocs(unittest.TestCase):

    def test_all_required_methods_have_docstrings(self):
        """ Make sure that all the required methods are well documented """
        DOCSTRING_LENGTH = 5
        REQUIRED_DOCSTRINGS = [ '__init__', '__str__', 'items', '__contains__',
                                '__iter__', '__eq__', '__add__', '__sub__', '__mul__',
                                'itertimes', 'itervalues', 'iteritems', '__abs__', '__bool__']
        ts = TimeSeries([1, 2, 3], [1,2,3])
        for method in REQUIRED_DOCSTRINGS:
            try:
                if len(getattr(ts, method, '').__doc__.strip()) > DOCSTRING_LENGTH:
                    scores.append( ('#doc General', 'item docstrings: ' + method, 1))
            except AttributeError:
                scores.append( ('#doc General', 'item docstrings: ' + method, 0))
                continue
            except Exception as e:
                logging.exception(e)
                scores.append( ('#doc General', 'item docstrings: ' + method, 0))

    def test_class_has_docstring(self):
        ts = TimeSeries([1, 2, 3], [1,2,3])
        self.assertIsNotNone(ts.__doc__)
        self.assertTrue(len(ts.__doc__ )>10 )
        scores.append(('#doc General', 'class docstrings', 3))