#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2008-2022
#  National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________

import pyomo.common.unittest as unittest
import pytest

from pyomo.contrib.mpc.data.find_nearest_index import (
    find_nearest_index,
    find_nearest_interval_index,
)


class TestFindNearestIndex(unittest.TestCase):

    def test_two_points(self):
        array = [0, 5]

        i = find_nearest_index(array, 1)
        self.assertEqual(i, 0)
        i = find_nearest_index(array, 1, tolerance=0.5)
        self.assertEqual(i, None)

        i = find_nearest_index(array, -0.01, tolerance=0.1)
        self.assertEqual(i, 0)
        i = find_nearest_index(array, -0.01, tolerance=0.001)
        self.assertEqual(i, None)

        i = find_nearest_index(array, 6, tolerance=2)
        self.assertEqual(i, 1)
        i = find_nearest_index(array, 6, tolerance=1)
        self.assertEqual(i, 1)

        # This test relies on the behavior for tiebreaks
        i = find_nearest_index(array, 2.5)
        self.assertEqual(i, 0)

    def test_array_with_floats(self):
        array = []
        for i in range(5):
            i0 = float(i)
            i1 = round((i + 0.15) * 1e4)/1e4
            i2 = round((i + 0.64) * 1e4)/1e4
            array.extend([i, i1, i2])
        array.append(5.0)

        i = find_nearest_index(array, 1.01, tolerance=0.1)
        self.assertEqual(i, 3)
        i = find_nearest_index(array, 1.01, tolerance=0.001)
        self.assertEqual(i, None)

        i = find_nearest_index(array, 3.5)
        self.assertEqual(i, 11)
        i = find_nearest_index(array, 3.5, tolerance=0.1)
        self.assertEqual(i, None)

        i = find_nearest_index(array, -1)
        self.assertEqual(i, 0)
        i = find_nearest_index(array, -1, tolerance=1)
        self.assertEqual(i, 0)

        i = find_nearest_index(array, 5.5)
        self.assertEqual(i, 15)
        i = find_nearest_index(array, 5.5, tolerance=0.49)
        self.assertEqual(i, None)

        i = find_nearest_index(array, 2.64, tolerance=1e-8)
        self.assertEqual(i, 8)
        i = find_nearest_index(array, 2.64, tolerance=0)
        self.assertEqual(i, 8)

        i = find_nearest_index(array, 5, tolerance=0)
        self.assertEqual(i, 15)

        i = find_nearest_index(array, 0, tolerance=0)
        self.assertEqual(i, 0)


class TestFindNearestIntervalIndex(unittest.TestCase):

    def test_find_interval(self):
        intervals = [(0.0, 0.1), (0.1, 0.5), (0.7, 1.0)]
        target = 0.05
        idx = find_nearest_interval_index(intervals, target)
        self.assertEqual(idx, 0)

        target = 0.1
        idx = find_nearest_interval_index(intervals, target)
        # TODO: Need some logic to break ties in this case.
        self.assertEqual(idx, 0)

        target = 0.55
        idx = find_nearest_interval_index(intervals, target)
        self.assertEqual(idx, 1)


if __name__ == "__main__":
    unittest.main()
