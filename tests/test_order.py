import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from turnorder.order import Order  # noqa: E402


class OrderTest(unittest.TestCase):
    def test_faster_goes_first(self):
        book = Order()
        book.add("slow", 10)
        book.add("fast", 90)
        self.assertEqual([name for name, _ in book.resolve("r1")], ["fast", "slow"])

    def test_other_unit_still_moves(self):
        book = Order()
        book.add("a", 100)
        book.add("b", 90)
        book.stun("b")
        self.assertIn("a", [name for name, _ in book.resolve("r1")])

    def test_scanned_starts_at_zero(self):
        self.assertEqual(Order().scanned, 0)


if __name__ == "__main__":
    unittest.main()
