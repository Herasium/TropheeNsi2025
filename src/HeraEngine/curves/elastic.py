import numpy as np

def elastic_interpolation(A, B, t):
    return A + (B - A) * (1 - np.exp(-6 * t) * np.cos(3 * np.pi * t))