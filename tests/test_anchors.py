import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from turnorder.order import Order  # noqa: E402


class AnchorTest(unittest.TestCase):
    """打印题面里引用的现状值。"""

    def test_length_only(self):
        book = Order()
        book.add("b", 100)
        book.add("a", 100)
        print("first=%s" % book.resolve("r1")[0][0])
        self.assertTrue(True)

    def test_stun_anchor(self):
        book = Order()
        book.add("a", 100)
        book.add("b", 90)
        book.stun("b")
        order = book.resolve("r1")
        print("len=%d skip=%d" % (len(order), sum(1 for _, skip in order if skip)))
        self.assertTrue(True)

    def test_dup_anchor(self):
        book = Order()
        book.add("a", 100)
        book.add("b", 90)
        first = book.resolve("r1")
        book.set_speed("a", 10)
        second = book.resolve("r1")
        print("same=%s" % (first == second))
        self.assertTrue(True)

    def test_work_anchor(self):
        book = Order()
        for index in range(3000):
            book.add("u-%d" % index, index)
        for index in range(3000):
            book.resolve("r-%d" % index)
        print("scanned=%d" % book.scanned)
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
