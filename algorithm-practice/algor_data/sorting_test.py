from . import data
from .sorting import bubble_sort, insertion_sort, merge_sort

import unittest


class SortingTestCase(unittest.TestCase):
    def setUp(self):
        self.work_set = list(data.UNSORTED_NUMBERS)
        self.sorted_data = sorted(data.UNSORTED_NUMBERS)

    def test_merge_sort(self):
        self.assertEqual(merge_sort(self.work_set), self.sorted_data)

    def test_bubble_sort(self):
        self.assertEqual(bubble_sort(self.work_set), self.sorted_data)

    def test_insertion_sort(self):
        self.assertEqual(insertion_sort(self.work_set), self.sorted_data)

    def tearDown(self):
        del self.work_set
        del self.sorted_data


if __name__ == '__main__':
    unittest.main()
