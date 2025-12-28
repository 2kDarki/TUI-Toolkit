from tuikit import logictools
import unittest

class TestLogicTools(unittest.TestCase):
    def test_any_in(self):
        any_in = logictools.any_in
        self.assertTrue(any_in(1, 2, 3, eq=[3, 4, 5]))
        self.assertFalse(any_in(6, 7, eq=[1, 2, 3]))
        self.assertTrue(any_in([1, 2], eq=[2, 3]))
        self.assertFalse(any_in([6, 7], eq=[1, 2]))
        self.assertTrue(any_in(3, eq=[3, 4]))
        self.assertFalse(any_in(5, eq=[1, 2]))

    def test_any_eq(self):
        any_eq = logictools.any_eq
        self.assertTrue(any_eq(2, 3, 4, eq=3))
        self.assertFalse(any_eq(1, 2, eq=5))
        self.assertTrue(any_eq([3], eq=3))
        self.assertFalse(any_eq([4], eq=5))
        self.assertTrue(any_eq(5, eq=5))
        self.assertFalse(any_eq(5, eq=4))

    def test_all_in(self):
        all_in = logictools.all_in
        self.assertTrue(all_in(1, 2, eq=[1, 2, 3]))
        self.assertFalse(all_in(1, 4, eq=[1, 2, 3]))
        self.assertTrue(all_in([2, 3], eq=[1, 2, 3]))
        self.assertFalse(all_in([2, 4], eq=[1, 2, 3]))
        self.assertTrue(all_in(3, eq=[1, 2, 3]))
        self.assertFalse(all_in(4, eq=[1, 2, 3]))

    def test_all_eq(self):
        all_eq = logictools.all_eq
        self.assertTrue(all_eq(5, 5, 5, eq=5))
        self.assertFalse(all_eq(5, 6, eq=5))
        self.assertTrue(all_eq([7, 7], eq=7))
        self.assertFalse(all_eq([7, 8], eq=7))
        self.assertTrue(all_eq(9, eq=9))
        self.assertFalse(all_eq(9, eq=10))
        
    def test_shave(self):
        shave = logictools.shave
        self.assertEqual(shave(75, 60), (15, 1))
        self.assertEqual(shave(121, 60), (1, 2))
        self.assertEqual(shave(59, 60), (59, 0))
        self.assertEqual(shave(-10, 60), (1, 0))

    def test_variance(self):
        variance = logictools.variance
        self.assertEqual(variance(100, 100), 0)
        self.assertEqual(variance(150, 100), 50)
        self.assertEqual(variance(0, 100), -100)
        self.assertEqual(variance(100, 0), 100)
        self.assertEqual(variance(0, 0), 0)
        with self.assertRaises(TypeError):
            variance("a", 100)
        with self.assertRaises(TypeError):
            variance(100, "b")

    def test_number_padding(self):
        pad_num = logictools.number_padding
        self.assertEqual(pad_num(5), "  5")
        self.assertEqual(pad_num(50, pad=4), "  50")
        self.assertEqual(pad_num(1234, pad=2), "1234")

    def test_format_order(self):
        fmt_order = logictools.format_order
        self.assertEqual(fmt_order("7", deno=3), "007")
        self.assertEqual(fmt_order("15",form="x"),"15")
        self.assertEqual(fmt_order("5",form="x"), "x5")
        with self.assertRaises(TypeError):
            fmt_order("5", deno="2")
        with self.assertRaises(TypeError):
            fmt_order("5", form=0)