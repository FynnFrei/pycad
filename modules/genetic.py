import copy
import os
import random
import numpy as np
import re
from modules import marimbaClass
from datetime import datetime

fundamental = 0  # Declare fundamental variable


def create_new_member(marimba_length, marimba_width_avr, marimba_height, num_of_parameters):

    num_of_params = num_of_parameters + 2       # adds groundLength parameter 2 times
    '''marimba_width = round(random.uniform(0.8 * marimba_width_avr, 1.2 * marimba_width_avr), 1)'''
    marimba_width = marimba_width_avr
    ground_length = round(random.uniform(10, (1 / num_of_params) * marimba_length), 2)

    new_member = [marimba_length, marimba_width, marimba_height, ground_length]

    for i in range(1, num_of_params - 1):
        new_x = round(random.uniform(((num_of_params - (i + 1)) / num_of_params) * marimba_length, ((num_of_params - i) / num_of_params) * marimba_length), 2)
        new_y = round(random.uniform(marimba_height / 2, marimba_height - 6), 2)     # bar should be minimum 6mm thick
        new_member.append(new_x)
        new_member.append(new_y)

    return new_member


def make_first_population(population_size, marimba_length, marimba_width_avr, marimba_height, num_of_parameters):
    population_value_list = []  # 2D List of all individual VALUES/VARIABLES
    num_of_params = num_of_parameters + 2       # adds groundLength parameter 2 times -> easier for the following lines
    for i in range(population_size):
        '''marimba_width = round(random.uniform(0.8 * marimba_width_avr, 1.2 * marimba_width_avr), 1)'''
        marimba_width = marimba_width_avr
        ground_length = round(random.uniform(10, (1 / num_of_params) * marimba_length), 2)

        new_member = [marimba_length, marimba_width, marimba_height, ground_length]

        for j in range(1, num_of_params - 1):
            new_x = round(random.uniform(((num_of_params - (j + 1)) / num_of_params) * marimba_length,
                                         ((num_of_params - j) / num_of_params) * marimba_length), 2)
            new_y = round(random.uniform(marimba_height / 2, marimba_height - 6), 2)  # bar should be minimum 6mm thick
            new_member.append(new_x)
            new_member.append(new_y)

        population_value_list.append(new_member)

    return population_value_list


# Test simulation of the marimba build and FEM analysis, less calculation time
def calculate_frequencies_test(population_value_list):
    frequency_list = []  # 2D List of all Eigenmodes of all individuals in population
    #marimbaClass.open_freecad()

    for i in range(len(population_value_list)):
        marimba_object = marimbaClass.Marimba(*population_value_list[i])    # TODO FreeCADGui can only open 62 docs (see TODO in marimbaClass)
        #marimba_object.marimba_sketch()
        marimbaClass.close_doc()
        frequencies = [random.randint(500, 1000), random.randint(1000, 1500), random.randint(1500, 2000),
                       random.randint(1800, 2300), random.randint(2300, 2600), random.randint(2600, 3000),
                       random.randint(3000, 3500), random.randint(3500, 4000), random.randint(4000, 4500),
                       random.randint(4500, 5500)]
        frequency_list.append(frequencies)

    #marimbaClass.close_freecad()
    return frequency_list


def calculate_frequencies(population_value_list):
    frequency_list = []

    #marimbaClass.open_freecad()

    for i in range(len(population_value_list)):
        marimba_object = marimbaClass.Marimba(*population_value_list[i])
        marimba_object.marimba_sketch()
        marimba_object.marimba_extrude()
        # marimba_object.box_part()
        marimba_object.marimba_analysis()
        marimbaClass.marimba_femrun()
        frequencies = marimba_object.read_eigenmodes()  # List of Eigenmodes of individual
        frequency_list.append(frequencies)
        marimbaClass.close_doc()

    #marimbaClass.close_freecad()

    return frequency_list


# Function to calculate fitness values for all individuals
def score_population(frequency_list):
    scores_list = []  # 1D List of all fitness values of all individuals in population
    for index, value in enumerate(frequency_list):
        score = (abs(pow(frequency_list[index][0] - fundamental, 1.5)) * 10) + abs(
            frequency_list[index][1] - (4 * fundamental)) + abs(frequency_list[index][2] - (10 * fundamental))
        scores_list.append(score)       # TODO find the best formula (exponents and multiplicators)

    return scores_list


def pick_mate(scores_list, parent_exception):
    # took parts from https://github.com/gmichaelson/GA_in_python/blob/master/GA%20example.ipynb
    scores_array = np.array(scores_list)
    temp = scores_array.argsort()  # Sorts indices from best to worst
    ranks = np.empty_like(temp)
    ranks[temp] = np.arange(len(scores_array))  # Gives each index a rank from 0 (best) to number-1 (worst)
    fitness = [len(ranks) - x for x in
               ranks]  # Gives each index a fitness value from 1 (worst) to number (best) -> linear

    for i in range(len(fitness)):  # Changes fitness score from linear to exponential
        fitness[i] = pow(fitness[i], 1.5)   # TODO find the best exponent

    add_scores = copy.deepcopy(fitness)

    for i in range(1, len(add_scores)):
        add_scores[i] = fitness[i] + add_scores[i - 1]  # Add up all fitness values

    probs = [i / add_scores[-1] for i in add_scores]  # The higher the fitness, the higher the probability

    rand = random.random()

    for i in range(0, len(probs)):
        if rand < probs[i] and i != parent_exception:  # The higher the fitness, the higher the chance that condition returns this index
            # print('Random Value:', rand, ' Chosen mate:', i, ' Mates fitness:', fitness[i], ' Mates score:',  scores_list[i], ' Mates rank:', ranks[i])
            return i


def crossover(a, b):
    sample = random.sample(a, 1)
    cut = np.random.choice(np.where(np.isin(a, sample))[0])

    new_a1 = copy.deepcopy(a[0:cut])
    new_a2 = copy.deepcopy(b[cut:])

    new_b1 = copy.deepcopy(b[0:cut])
    new_b2 = copy.deepcopy(a[cut:])

    new_a = list(np.append(new_a1, new_a2))
    new_b = list(np.append(new_b1, new_b2))

    return new_a, new_b


def mutate(child, probability, mutate_range_x, mutate_range_y, marimba_height, num_of_parameters):
    for i in range(4, (2 * num_of_parameters) + 4, 2):  # for all x (even) values of marimba bar
        if random.random() < probability and child[i + 1] != child[i] != child[i - 1]:  # constraints
            child[i] = round(random.uniform(child[i] - mutate_range_x, child[i] + mutate_range_x), 2)

    for i in range(5, (2 * num_of_parameters) + 5, 2):  # for all y (odd) values of marimba bar
        if random.random() < probability and marimba_height - mutate_range_y > child[i] > 0:  # constraints
            child[i] = round(random.uniform(child[i] - mutate_range_y, child[i] + mutate_range_y), 2)
            while child[i] == (child[i-1] or child[i+1]):     # this is to prevent error because two (x,y) points are equal
                child[i] -= round(random.uniform(0, mutate_range_y), 2)

    if random.random() < probability:       # mutates base length (x-value)
        child[3] = round(random.uniform(child[3] - mutate_range_x, child[3] + mutate_range_x), 2)

    return child


def write_file_generation(matrix, population_folder, wood_type, result_file_name, population_properties):
    # save all the results in a .txt file
    numbering = 0
    date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    while os.path.exists(fr"marimba_objects/population_{wood_type}_{population_folder}/{result_file_name}{numbering}.txt"):
        numbering += 1
    with open(f'marimba_objects/population_{wood_type}_{population_folder}/{result_file_name}{numbering}.txt', 'w') as f:
        for line in matrix:
            f.write(f"{line}\n")

        # write all population properties at the end of file
        f.write(f"\nPopulation size: {population_properties[0]}"
                f"\nNumber of couples: {population_properties[1]}"
                f"\nNumber of kept parents: {population_properties[2]}"
                f"\nBest parent kept: {population_properties[3]}"
                f"\nMutation Probability: {population_properties[4]}"
                f"\nMutation range (x, y): {population_properties[5]}, {population_properties[6]}"
                f"\n\nWritten time: {date_and_time}")

        print(f'{result_file_name}{numbering} written!')


def write_best_of_file(num_of_individuals, population_folder, wood_type, population_size, result_file_name):
    # makes a list of the best individuals from all former files
    numbering = 0
    all_population, all_scores = [], []
    while os.path.exists(fr"marimba_objects/population_{wood_type}_{population_folder}/{result_file_name}{numbering}.txt"):
        numbering += 1

    if numbering == 0:  # if no readable file exists, return false
        return False

    for index in range(numbering):
        with open(f'marimba_objects/population_{wood_type}_{population_folder}/{result_file_name}{index}.txt', 'r') as file:
            head = [next(file) for i in range(population_size)]  # all file content in a list
            print(head)
            for j in range(len(head)):
                member = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", head[j])  # extracts all floats from string
                member = list(filter(None, member))
                member = [float(x) for x in member]
                values = member[1:-3]  # make a list of all member (population[j]) values
                score = member[0]  # save the score value

                all_population.append(values)
                all_scores.append(score)

    matrix_generation = [[all_scores[i], all_population[i]] for i in range(len(all_scores))]
    matrix_generation_sorted = sorted(matrix_generation, key=lambda l: l[0])

    matrix_best_of = matrix_generation_sorted[:num_of_individuals]

    with open(f'marimba_objects/population_{wood_type}_{population_folder}/result_file_best_of(0-{numbering - 1}).txt', 'w') as f:
        for line in matrix_best_of:
            f.write(f"{line}\n")
        print('result_file_best_of written!')

    return matrix_best_of


def read_file(population_size, population_folder, wood_type, result_file_name):
    numbering = 0
    population, scores = [], []
    while os.path.exists(fr"marimba_objects/population_{wood_type}_{population_folder}/{result_file_name}{numbering}.txt"):
        numbering += 1

    if numbering == 0:      # if no readable file exists, return false
        return False

    with open(f'marimba_objects/population_{wood_type}_{population_folder}/{result_file_name}{numbering - 1}.txt', 'r') as file:
        head = [next(file) for i in range(population_size)]      # all file content in a list
        for j in range(len(head)):
            member = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", head[j])  # extracts all floats from string
            member = list(filter(None, member))
            member = [float(x) for x in member]
            values = member[1:-3]   # make a list of all member (population[j]) values
            score = member[0]     # save the score value

            population.append(values)
            scores.append(score)
    return population, scores


def build_best_bar(matrix_sorted):
    bar = marimbaClass.Marimba(*matrix_sorted[0][1])
    bar.marimba_sketch()
    bar.marimba_extrude()
    bar.marimba_analysis()
    bar.recompute()

    numbering = 0
    while os.path.exists(fr"marimba_objects/Best_Bar{numbering}.FCStd"):
        numbering += 1

    bar.save(fr"marimba_objects/Best_Bar{numbering}.FCStd")


def build_single_bar(*, save_bar: bool = False):        # a function to test specific shapes of single bars
    # values = create_new_member(450, 30, 60, 10)
    # bar = marimbaClass.Marimba(*values)
    bar = marimbaClass.Marimba(440.4, 68.58, 28.96, 25.29, 296.03, 21.75, 222.34, 21.99, 191.75, 22.68, 86.07, 22.85)
    bar.marimba_sketch()
    bar.marimba_extrude()
    bar.marimba_analysis()
    #marimbaClass.marimba_femrun()
    #frequencies = bar.read_eigenmodes()
    #print(frequencies)

    if save_bar:
        bar.recompute()

        numbering = 0
        while os.path.exists(fr"marimba_objects/Single_Bar{numbering}.FCStd"):
            numbering += 1

        bar.save(fr"marimba_objects/Single_Bar{numbering}.FCStd")

