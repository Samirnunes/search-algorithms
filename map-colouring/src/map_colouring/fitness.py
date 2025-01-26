import numpy as np

MIN_FITNESS = 0

def fitness(array: np.ndarray):
    fitness = MIN_FITNESS
    for i in range(array.shape[0]):
        color = array[i][i]
        for j in range(array.shape[1]):
            if array[i][j] == color and j != i:
                fitness += 1
    return fitness
                