# -*- coding: utf-8 -*-
#
"""

# Unit Test script

This is a standalone script which tests the Super Simple Stock Market engine
"""

import unittest
import datetime
import engine

class SuperSimple(unittest.TestCase):

    def test_main_data(self):
        JOE = {'Type': 'Common', 'Par_Value': 250, 'Stock_Symbol': 'JOE', 'Fixed_Dividend': '', 'Last_Dividend': 13}
        self.assertEqual(engine.main_data('JOE'), JOE)
        self.assertRaises(ValueError, engine.main_data, 'NONEXISTANTSTOCK')

    def test_dividend_yield_common_type(self):
        self.assertEqual(engine.calculate_dividend_yield('POP', 149), 5.37)
        self.assertEqual(engine.calculate_dividend_yield('JOE', 0.01), 130000)
        self.assertEqual(engine.calculate_dividend_yield('POP', 1), 800.0)
        self.assertRaises(ValueError, engine.calculate_dividend_yield, 'ALE', -1)

    def test_dividend_yield_preferred_type(self):
        self.assertEqual(engine.calculate_dividend_yield('GIN', 43), 4.65)
        self.assertEqual(engine.calculate_dividend_yield('GIN', 0.01), 20000.0)
        self.assertEqual(engine.calculate_dividend_yield('GIN', 1), 200.0)
        self.assertRaises(ValueError, engine.calculate_dividend_yield, 'GIN', -1)

    def test_p_to_e_ratio(self):
        self.assertEqual(engine.p_to_e_ratio('TEA', 0.01), 0.0)
        self.assertEqual(engine.p_to_e_ratio('ALE', 100), 4.35)
        self.assertEqual(engine.p_to_e_ratio('ALE', 1), 0.04)
        self.assertEqual(engine.p_to_e_ratio('ALE', 0.01), 0.00)
        self.assertRaises(ValueError, engine.p_to_e_ratio, 'GIN', -1)

    def test_trade_record(self):
        trade = engine.trade_record('ALE', 100, 'SELL', 15)
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M")
        self.assertIn('ALE', trade)
        self.assertIn(str(100), trade)
        self.assertIn('SELL', trade)
        self.assertIn(str(15), trade)
        self.assertIn(timestamp, trade)
        self.assertNotIn('JOE',trade)


    def test_volume_weighted_stock_price(self):
        pass

    def test_gbce_all_share_index(self):
        pass


if __name__ == '__main__':
    unittest.main()
