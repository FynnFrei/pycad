import copy
import math
import random
import numpy as np
from modules import marimbaClass

fundamental = 0  # Declare fundamental variable
population_list = []  # 1D List af all individual objects -> currently not active
population_value_list = []  # 2D List of all individual VALUES/VARIABLES
frequency_list = []  # 2D List of all Eigenmodes of all individuals
scores_list = []    # 1D List of all score values of all individuals in one generation


# Test version of make_parents, less calculation time
def make_population_test(population_members):
    for i in range(population_members):
        marimbaLength, marimbaWidth, marimbaHeight = 440.5, 68.6, 29.0
        groundLength = random.uniform(10, marimbaLength / 10)
        x2 = round(random.uniform(0.8 * marimbaLength, 0.9 * marimbaLength), 2)  # Rounds on 2 digits
        x3 = round(random.uniform(0.7 * marimbaLength, 0.8 * marimbaLength), 2)
        x4 = round(random.uniform(0.6 * marimbaLength, 0.7 * marimbaLength), 2)
        x5 = round(random.uniform(0.5 * marimbaLength, 0.6 * marimbaLength), 2)
        x6 = round(random.uniform(0.4 * marimbaLength, 0.5 * marimbaLength), 2)
        x7 = round(random.uniform(0.3 * marimbaLength, 0.4 * marimbaLength), 2)
        x8 = round(random.uniform(0.2 * marimbaLength, 0.3 * marimbaLength), 2)
        x9 = round(random.uniform(0.1 * marimbaLength, 0.2 * marimbaLength), 2)
        y2 = round(random.uniform(0, 0.8 * marimbaHeight), 2)
        y3 = round(random.uniform(0, 0.8 * marimbaHeight), 2)
        y4 = round(random.uniform(0, 0.8 * marimbaHeight), 2)
        y5 = round(random.uniform(0, 0.8 * marimbaHeight), 2)
        y6 = round(random.uniform(0, 0.8 * marimbaHeight), 2)
        y7 = round(random.uniform(0, 0.8 * marimbaHeight), 2)
        y8 = round(random.uniform(0, 0.8 * marimbaHeight), 2)
        y9 = round(random.uniform(0, 0.8 * marimbaHeight), 2)

        population_value_list.append(
            [marimbaLength, marimbaWidth, marimbaHeight, groundLength, x2, x3, x4, x5, x6, x7, x8,
             x9, y2, y3,
             y4, y5, y6, y7, y8, y9])
        frequencies = [random.randint(500, 1000), random.randint(1000, 1500), random.randint(1500, 2000), random.randint(2000, 2500), random.randint(2500, 3000), random.randint(3000, 3500)]
        frequency_list.append(frequencies)

    print('\n!!!ALL TEST MEMBERS PRODUCED!!!\n')


def make_population(population_members):
    for i in range(population_members):
        marimbaLength, marimbaWidth, marimbaHeight = 440.5, 68.6, 29.0
        groundLength = random.uniform(10, marimbaLength / 10)
        x2 = round(random.uniform(0.8 * marimbaLength, 0.9 * marimbaLength), 2)  # Rounds on 2 digits
        x3 = round(random.uniform(0.7 * marimbaLength, 0.8 * marimbaLength), 2)
        x4 = round(random.uniform(0.6 * marimbaLength, 0.7 * marimbaLength), 2)
        x5 = round(random.uniform(0.5 * marimbaLength, 0.6 * marimbaLength), 2)
        x6 = round(random.uniform(0.4 * marimbaLength, 0.5 * marimbaLength), 2)
        x7 = round(random.uniform(0.3 * marimbaLength, 0.4 * marimbaLength), 2)
        x8 = round(random.uniform(0.2 * marimbaLength, 0.3 * marimbaLength), 2)
        x9 = round(random.uniform(0.1 * marimbaLength, 0.2 * marimbaLength), 2)
        y2 = round(random.uniform(0, 0.8 * marimbaHeight), 2)
        y3 = round(random.uniform(0, 0.8 * marimbaHeight), 2)
        y4 = round(random.uniform(0, 0.8 * marimbaHeight), 2)
        y5 = round(random.uniform(0, 0.8 * marimbaHeight), 2)
        y6 = round(random.uniform(0, 0.8 * marimbaHeight), 2)
        y7 = round(random.uniform(0, 0.8 * marimbaHeight), 2)
        y8 = round(random.uniform(0, 0.8 * marimbaHeight), 2)
        y9 = round(random.uniform(0, 0.8 * marimbaHeight), 2)

        population_value_list.append(
            [marimbaLength, marimbaWidth, marimbaHeight, groundLength, x2, x3, x4, x5, x6, x7, x8,
             x9, y2, y3,
             y4, y5, y6, y7, y8, y9])
        '''population_list.append(
            marimbaClass.Marimba(marimbaLength, marimbaWidth, marimbaHeight, groundLength, x2, x3, x4, x5, x6, x7, x8,
                                 x9, y2, y3,
                                 y4, y5, y6, y7, y8, y9))'''
        print(population_value_list[i])
        marimba_object = marimbaClass.Marimba(marimbaLength, marimbaWidth, marimbaHeight, groundLength, x2, x3, x4, x5,
                                              x6, x7, x8,
                                              x9, y2, y3,
                                              y4, y5, y6, y7, y8, y9)
        marimba_object.marimba_sketch()
        marimba_object.marimba_extrude()
        marimba_object.box_part()
        marimba_object.marimba_analysis()
        marimbaClass.marimba_femrun()
        frequencies = marimba_object.read_eigenmodes()  # List of Eigenmodes of individual
        frequency_list.append(frequencies)

        # get file numbering
        '''numbering = 0
        while os.path.exists(fr"marimba_objects/Figure{numbering}.FCStd"):
            numbering += 1

        population_list[i].recompute()
        population_list[i].save(fr"marimba_objects/Figure{numbering}.FCStd")'''

    print('\n!!!ALL MEMBERS PRODUCED!!!\n')


# Function to calculate fitness values for all individuals
def score_population():
    for index, value in enumerate(frequency_list):
        score = abs(frequency_list[index][0] - fundamental)  # TODO real fitness function (modes 1, 2, 5)
        scores_list.append(score)


def pick_mate():
    # took parts from https://github.com/gmichaelson/GA_in_python/blob/master/GA%20example.ipynb
    scores_array = np.array(scores_list)
    temp = scores_array.argsort()  # Sorts indices from best to worst
    ranks = np.empty_like(temp)
    ranks[temp] = np.arange(len(scores_array))  # Gives each index a rank from 0 (best) to number-1 (worst)
    fitness = [len(ranks) - x for x in
               ranks]  # Gives each index a fitness value from 1 (worst) to number (best) -> linear

    for i in range(len(fitness)):  # Changes fitness score from linear to exponential
        fitness[i] = pow(fitness[i], 1.5)

    add_scores = copy.deepcopy(fitness)

    for i in range(1, len(add_scores)):
        add_scores[i] = fitness[i] + add_scores[i - 1]  # Add up all fitness values

    probs = [i / add_scores[-1] for i in add_scores]  # The higher the fitness, the higher the probability
    '''print('scores_array: ', scores_array)
    print('temp: ', temp)
    print('ranks: ', ranks)
    print('fitness:', fitness)
    print('probs: ', probs)'''

    rand = random.random()

    for i in range(0, len(probs)):
        if rand < probs[i]:  # The higher the fitness, the higher the chance that condition returns this index
            print('Random Value:', rand, ' Chosen mate:', i, ' Mates fitness:', fitness[i], ' Mates score:',  scores_list[i], ' Mates rank:', ranks[i])
            return i


def crossover(a, b):
    print('Parent a: ', a, '\nParent b: ', b)
    sample = random.sample(a, 1)

    cut = np.random.choice(np.where(np.isin(a, sample))[0])

    new_a1 = copy.deepcopy(a[0:cut])
    new_a2 = copy.deepcopy(b[cut:])

    new_b1 = copy.deepcopy(b[0:cut])
    new_b2 = copy.deepcopy(a[cut:])

    new_a = np.append(new_a1, new_a2)
    new_b = np.append(new_b1, new_b2)
    print('cut: ', cut)

    return new_a, new_b


'''
def mutate():


def create_new_member():


def create_next_generation():


def main():
'''
