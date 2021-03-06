from .context import nanopq

import unittest

import numpy as np


class TestSuite(unittest.TestCase):
    def setUp(self):
        np.random.seed(123)

    def test_property(self):
        opq = nanopq.OPQ(M=4, Ks=256)
        self.assertEqual(
            (opq.M, opq.Ks, opq.verbose, opq.code_dtype),
            (opq.pq.M, opq.pq.Ks, opq.pq.verbose, opq.pq.code_dtype))

    def test_fit(self):
        N, D, M, Ks = 100, 12, 4, 10
        X = np.random.random((N, D)).astype(np.float32)
        opq = nanopq.OPQ(M=M, Ks=Ks)
        opq.fit(X)
        self.assertEqual(opq.Ds, D / M)
        self.assertEqual(opq.codewords.shape, (M, Ks, D / M))
        self.assertEqual(opq.R.shape, (D, D))

    def test_rotate(self):
        N, D, M, Ks = 100, 12, 4, 10
        X = np.random.random((N, D)).astype(np.float32)
        opq = nanopq.OPQ(M=M, Ks=Ks)
        opq.fit(X)
        rotated_vec = opq.rotate(X[0])
        rotated_vecs = opq.rotate(X[:3])
        self.assertEqual(rotated_vec.shape, (D, ))
        self.assertEqual(rotated_vecs.shape, (3, D))

        # Because R is a rotation matrix (R^t * R = I), R^t should be R^(-1)
        self.assertAlmostEqual(np.linalg.norm(opq.R.T - np.linalg.inv(opq.R)), 0.0, places=3)


if __name__ == '__main__':
    unittest.main()
