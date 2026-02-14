import unittest

from date_utils import parse_shiller_date


class TestProcess(unittest.TestCase):
    def test_parse_shiller_date_handles_january_and_october(self):
        self.assertEqual(parse_shiller_date(2021.01), "2021-01-01")
        self.assertEqual(parse_shiller_date(2021.1), "2021-10-01")


if __name__ == "__main__":
    unittest.main()
