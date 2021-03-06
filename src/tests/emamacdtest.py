"""Unit test for EmaMacd.py

"""

__author__ = "Sander Smits (jhmsmits@xs4all.nl)"
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2006/07/04 20:54:20 $"
__copyright__ = "Copyright (c) 2006 Sander Smits"
__license__ = "Python"

from ta.Ema import *
import unittest

inputValues = [(datetime.datetime(2006, 5, 1), 12.34, 12.56, 12.11, 12.20, 2010912),
             (datetime.datetime(2006, 5, 2), 12.24, 12.48, 12.20, 12.20, 8791029),
                (datetime.datetime(2006, 5, 2), 12.24, 12.48, 12.20, 12.21, 8791029),
                (datetime.datetime(2006, 5, 2), 12.24, 12.48, 12.20, 12.22, 8791029),
             (datetime.datetime(2006, 5, 3), 12.18, 12.20, 11.88, 12.16, 5434255),
             (datetime.datetime(2006, 5, 4), 12.24, 12.68, 12.24, 12.36, 8734251),
                (datetime.datetime(2006, 5, 4), 12.34, 12.78, 12.20, 12.38, 6534253),
             (datetime.datetime(2006, 5, 5), 12.30, 12.88, 12.28, 12.57, 3637262),
             (datetime.datetime(2006, 5, 8), 12.34, 12.56, 12.11, 12.20, 2010912),
             (datetime.datetime(2006, 5, 9), 12.24, 12.48, 12.20, 12.22, 8791029),
             (datetime.datetime(2006, 5, 10), 12.18, 12.20, 11.88, 12.16, 5434255),
             (datetime.datetime(2006, 5, 11), 12.24, 12.68, 12.24, 12.38, 8734251),
             (datetime.datetime(2006, 5, 12), 12.30, 12.88, 12.28, 12.57, 3637262),
             (datetime.datetime(2006, 5, 15), 12.34, 12.56, 12.11, 12.20, 2010912),
             (datetime.datetime(2006, 5, 16), 12.24, 12.48, 12.20, 12.22, 8791029),
             (datetime.datetime(2006, 5, 17), 12.18, 12.20, 11.88, 12.16, 5434255),
             (datetime.datetime(2006, 5, 18), 12.24, 12.68, 12.24, 12.38, 8734251),
             (datetime.datetime(2006, 5, 19), 12.30, 12.88, 12.28, 12.57, 3637262),
          ]

class BadInitializationInput(unittest.TestCase):
    def testNoneParameter(self):
        """ initializing should fail with None parameter """
        self.assertRaises(IndicatorError, EmaMacd, None)
        
    def testTupleParameter(self):
        """ initializing should fail with tuple parameter """
        self.assertRaises(IndicatorError, EmaMacd, (4, ))
        
    def testStringParameter(self):
        """ initializing should fail with str parameter """
        self.assertRaises(IndicatorError, EmaMacd, '4')
        
    def testNegativeIntParameter(self):
        """ initializing should fail with negative int parameter """
        self.assertRaises(IndicatorError, EmaMacd, -1)
        
    def testEmptyParameter(self):
        """ initializing should raise TypeError with empty parameter """
        self.assertRaises(TypeError, EmaMacd)

class AppendBadInput(unittest.TestCase):
    def testInteger(self):
        """append should fail with integer input"""
        s = EmaMacd(4)
        self.assertRaises(NotTupleError, s.append, 4000)
        
    def testString(self):
        """append should fail with string input"""
        s = EmaMacd(4)
        self.assertRaises(NotTupleError, s.append, "dummy")
        
    def testFloat(self):
        """append should fail with float input"""
        s = EmaMacd(4)
        self.assertRaises(NotTupleError, s.append, 12.432)
        
    def testFloatVolume(self):
        """append should fail with float value for volume"""
        s = EmaMacd(4)
        c = (datetime.datetime(2006, 5, 19), 12.34, 12.56, 12.11, 12.20, 2010912.25)
        self.assertRaises(InvalidCandleStickError, s.append, c)
     
    def testStringOpen(self):
        """append should fail with string value for open"""
        s = EmaMacd(4)
        c = (datetime.datetime(2006, 5, 19), "dummy", 12.56, 12.11, 12.20, 2010912)
        self.assertRaises(InvalidCandleStickError, s.append, c)
    
    def testNoneOpen(self):
        """append should fail with None value for open"""
        s = EmaMacd(4)
        c = (datetime.datetime(2006, 5, 19), None, 12.56, 12.11, 12.20, 2010912)
        self.assertRaises(InvalidCandleStickError, s.append, c)
        
    def testTupleTooLarge(self):
        """append should fail with tuple that has a length bigger than 6"""
        s = EmaMacd(4)
        c = (datetime.datetime(2006, 5, 19), None, 12.56, 12.11, 12.20, 2010912, 1425)
        self.assertRaises(InvalidCandleStickError, s.append, c)
        
    def testTupleTooSmall(self):
        """append should fail with tuple that has a length smaller than 6"""
        s = EmaMacd(4)
        c = (datetime.datetime(2006, 5, 19), None, 12.56, 12.11, 12.20)
        self.assertRaises(InvalidCandleStickError, s.append, c)
        
    def testOlderDateTime(self):
        """append should fail with candle input that has an older datetime than the most recently processed candle """
        s = EmaMacd(4)
        testInput = inputValues[:8]
        for c in testInput:
            s.append(c)
        self.assertRaises(InvalidDateTimeError, s.append, inputValues[4])
        
    def testIntegerDateTime(self):
        """append should fail with candle input that does not have a datetime as first element """
        s = EmaMacd(4)
        c = (1562516271, 12.34, 12.56, 12.11, 12.20, 2010912)
        self.assertRaises(InvalidDateTimeError, s.append, c)
        
    def testHighLowMixUp(self):
        """append should fail with high lower than low"""
        s = EmaMacd(4)
        c = (datetime.datetime(2006, 5, 19), 12.34, 12.11, 12.56, 12.20, 2010912)
        self.assertRaises(InvalidCandleStickError, s.append, c)
        
    def testOpenHigherThanHigh(self):
        """append should fail with open higher than high"""
        s = EmaMacd(4)
        c = (datetime.datetime(2006, 5, 19), 12.60, 12.56, 12.11, 12.20, 2010912)
        self.assertRaises(InvalidCandleStickError, s.append, c)
    
    def testCloseLowerThanLow(self):
        """append should fail with close lower than low"""
        s = EmaMacd(4)
        c = (datetime.datetime(2006, 5, 19), 12.60, 12.56, 12.11, 12.09, 2010912)
        self.assertRaises(InvalidCandleStickError, s.append, c)
        
class KnownValues(unittest.TestCase):
    def testOutputKnownValues(self):
        """EmaMacd calculation should give known result with known input
           results are rounded by str representation of floats
        """
        s = EmaMacd(4)
        knownvalues = [None, None, None, 12.24, 12.372, 12.3032, 12.26992, 12.225952]
        for c in inputValues[:11]:
            s.append(c)
        for i in range(len(s.output)):
            self.assertEqual(str(s.output[i]), str(knownvalues[i]))
            