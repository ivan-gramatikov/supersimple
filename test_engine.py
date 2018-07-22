# -*- coding: utf-8 -*-
#
"""

# Unit Test script

This is a standalone script which tests the Super Simple Stock Market engine
"""

import unittest
import engine

class TestDividend(unittest.TestCase):

    def test_dividend_yield_proper(self):
        self.assertEqual(engine.calculate_dividend_yield('POP', 149), 5.37)
        self.assertEqual(engine.calculate_dividend_yield('JOE', 0.01), 130000)
        self.assertRaises(ValueError, engine.calculate_dividend_yield, 'ALE', -1)


    def test_dividend_yield_common(self):
        self.assertEqual(engine.calculate_dividend_yield('POP', 149), 5.37)





# class Test


if __name__ == '__main__':
    unittest.main()
