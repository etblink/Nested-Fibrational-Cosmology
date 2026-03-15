"""
Toy Universe U12 Simulator
NFC Computational Verification Module
"""

import numpy as np
from itertools import product

class ToyU12Simulator:
    """
    Simulates the U12 toy universe with defect-mediated evolution.

    Parameters:
    -----------
    gamma : float
        Gap threshold separating sub-gap from super-gap defects
    lambda_param : float
        Decay parameter for weighted frequencies
    """

    def __init__(self, gamma=2, lambda_param=0.5):
        self.sites = ['a', 'b', 'c', 'd']
        self.gamma = gamma
        self.lambda_param = lambda_param

        # Relations: (source_set, target_set, type)
        self.relations = {
            'b1': ({'a'}, {'b'}, 'backbone'),
            'b2': ({'b'}, {'c'}, 'backbone'),
            'b3': ({'c'}, {'d'}, 'backbone'),
            'h0': ({'a'}, {'d'}, 'halo'),
            'h1': ({'a'}, {'d'}, 'halo'),
            'd1': ({'b'}, {'b'}, 'defect_sub'),
            'd2': ({'c'}, {'c'}, 'defect_super'),
            'w': ({'d'}, {'d'}, 'witness')
        }

        self.defect_weights = {'d1': 1, 'd2': 1, 'd2_d1': 2}

    def compute_defect_functional(self, path):
        """Compute D(path) = sum of defect weights"""
        return sum(self.defect_weights.get(step, 0) for step in path)

    def compute_k_eff(self, defect_budget):
        """Effective witness depth given defect budget"""
        k_max = 2
        c = 1.0
        return k_max * max(0, 1 - c * defect_budget / (self.gamma ** 2))

# Verification tests
def test_theorems():
    """Verify NFC theorems computationally"""
    sim = ToyU12Simulator()

    # Theorem: k_eff decreases monotonically with D
    D_vals = np.linspace(0, 10, 100)
    k_vals = [sim.compute_k_eff(D) for D in D_vals]
    assert all(k_vals[i] >= k_vals[i+1] for i in range(len(k_vals)-1)),         "k_eff not monotonically decreasing"

    # Theorem: k_eff = 0 for D >= gamma^2
    assert sim.compute_k_eff(4) == 0, "k_eff should be 0 at threshold"

    print("✅ All computational theorem verifications passed")

if __name__ == "__main__":
    test_theorems()
