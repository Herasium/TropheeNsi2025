import time
from math import *
import timeit

def test_primes():
    sieve_limit = 1000000
    start = time.time()
    sieve = [True] * (sieve_limit + 1)
    sieve[0] = sieve[1] = False
    for current in range(2, int(sieve_limit ** 0.5) + 1):
        if sieve[current]:
            sieve[current*current :: current] = [False] * len(sieve[current*current :: current])
    end = time.time()
    return end - start

def test_pi():
    iterations = 10000000 
    start = time.time()
    pi_over_4 = 0.0
    for i in range(iterations):
        denominator = 2 * i + 1
        if i % 2 == 0:
            pi_over_4 += 1.0 / denominator
        else:
            pi_over_4 -= 1.0 / denominator
    end = time.time()
    return end - start

def test_matrix():
    size = 50
    start = time.time()

    a = [[1.0 for _ in range(size)] for _ in range(size)]
    b = [[1.0 for _ in range(size)] for _ in range(size)]
    result = [[0.0 for _ in range(size)] for _ in range(size)]
    
    for i in range(size):
        for k in range(size):
            aik = a[i][k]
            for j in range(size):
                result[i][j] += aik * b[k][j]
    end = time.time()
    return end - start

def benchmark():
    time_primes = test_primes()
    time_pi = test_pi()
    time_matrix = test_matrix()
    bench()

    total_time = time_primes + time_pi + time_matrix
    score = 10 / total_time  
    return score


def bench():
    product = 1.0
    for counter in range(1, 1000, 1):
        for dex in list(range(1, 360, 1)):
            angle = radians(dex)
            product *= sin(angle)**2 + cos(angle)**2
    return product



if __name__ == "__main__":

    print(f"\nCPU Score: {benchmark():.1f}")

#PC Du lycée (salle nsi): 6.9 ; 30fps
#PC CDI : 3.1 ; 20fps
#PC Windows: 11.5