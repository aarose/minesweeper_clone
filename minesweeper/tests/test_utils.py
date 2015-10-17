import unittest

from minesweeper.grids.utils import (
    InvalidMineAmount,
    Matrix,
    MineMap,
    )


class TestMatrixMethods(unittest.TestCase):

    def test_init_only_width(self):
        """ Should create an NxN matrix. """
        N = 3
        new_matrix = Matrix(N)
        # Height/rows
        self.assertEqual(N, len(new_matrix))
        self.assertEqual(N, new_matrix.height)
        # Width/columns
        self.assertEqual(N, len(new_matrix[0]))
        self.assertEqual(N, new_matrix.width)

    def test_init_width_and_height(self):
        """ Should create a NxM matrix. """
        N = 3
        M = 5
        new_matrix = Matrix(N, M)
        # Height/rows
        self.assertEqual(N, len(new_matrix))
        self.assertEqual(N, new_matrix.height)
        # Width/columns
        self.assertEqual(M, len(new_matrix[0]))
        self.assertEqual(M, new_matrix.width)

    def test_init_with_value(self):
        """ Should create a matrix with a different init value than default."""
        init_value = 'bananas'
        matrix = Matrix(2, init_value=init_value)
        self.assertEqual(init_value, matrix[0][0])

    def test_call(self):
        """ Should be callable, and return the element located at x and y. """
        matrix = Matrix(2)
        element_value = 'blue'
        x = 0
        y = 1
        matrix[x][y] = element_value
        self.assertEqual(element_value, matrix(x, y))

    def test_init_no_width(self):
        """ Should create an empty Matrix (list with one empty list). """
        matrix = Matrix(0)
        self.assertEqual([], matrix)
        self.assertNotEqual([[], ], matrix)

    def test_adjacent_indices(self):
        """ Should return the list of indices, with none out of range. """
        # Index is not at either edge
        index = 1
        expected = [index-1, index, index+1]
        limit = index+1
        self.assertListEqual(expected, Matrix._adjacent_indices(index, limit))

        # Index == limit
        index = limit
        expected = [index-1, index]
        self.assertListEqual(expected, Matrix._adjacent_indices(index, limit))

        # Index == 0 (first)
        index = 0
        expected = [index, index+1]
        self.assertListEqual(expected, Matrix._adjacent_indices(index, limit))


class TestMineMapMethods(unittest.TestCase):

    def test_init(self):
        """ Should create a MineMap. """
        mines, size = 1, 5
        minemap = MineMap(mines, size)
        self.assertTrue(minemap)

    def test_exceed_mine_limit(self):
        """ Should raise InvalidMineAmount if too many mines we requested. """
        size = 5  # 5x5 matrix
        mines = size*size
        self.assertRaises(InvalidMineAmount, MineMap, mines, size)

    def test_rand_coords(self):
        """ Should return coodinates that are within the limits. """
        mines, size = 1, 2
        minemap = MineMap(mines, size)
        (x, y) = minemap._random_coord()
        self.assertLess(x, minemap.height)
        self.assertLess(y, minemap.width)


if __name__ == '__main__':
    unittest.main()
