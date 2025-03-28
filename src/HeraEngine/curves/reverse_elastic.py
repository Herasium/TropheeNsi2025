import numpy as np

def reverse_elastic_interpolation(B, A, t):
    t = max(0,1-t)
    return A + (B - A) * (1 - np.exp(-6 * t) * np.cos(3 * np.pi * t))