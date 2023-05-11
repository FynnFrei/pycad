import copy
import numpy as np
from operator import itemgetter
from modules import genetic

# parameters:
genetic.fundamental = 130.8  # Fundamental Frequency of marimba Bar 130.8 == C3
marimba_length, marimba_width_avr, marimba_height = 440, 69, 29    # 440.4, 68.58, 28.96
num_of_parameters = 6       # free (x,y) koordinates
population_folder = 5       # folder is called 'population{population_folder}'
wood_type = 'Chestnut'
result_file_name = f'result_file_{wood_type}_{population_folder}_generation'


def test_code():
    # parameters
    population_size = 30
    number_of_generations = 2
    number_of_couples = 13      # each couple has 2 children
    number_of_parents_to_keep = 0
    keep_best_parent = True
    mutation_probability = 0.3
    mutate_range_x, mutate_range_y = 5, 0.5
    population_properties = [population_size, number_of_couples, number_of_parents_to_keep, keep_best_parent,
                             mutation_probability, mutate_range_x, mutate_range_y, num_of_parameters,
                             marimba_length, marimba_width_avr, marimba_height, genetic.fundamental]

    if not genetic.read_file(population_size, population_folder, wood_type, result_file_name):
        # create the starting population
        population = genetic.make_first_population(population_size, marimba_length, marimba_width_avr, marimba_height, num_of_parameters)
        frequencies = genetic.calculate_frequencies(population)     # this is the big FEM analysis that takes all the time
        scores = genetic.score_population(frequencies)
        matrix_generation = [[round(scores[i], 2), population[i],
                              itemgetter(0, 1, 2)(frequencies[i])] for i in range(population_size)]
        matrix_generation_sorted = sorted(matrix_generation, key=lambda l: l[0])
        genetic.write_file_generation(matrix_generation_sorted, population_folder, wood_type, result_file_name, population_properties)
        print('Generation 0 is ready!')
    else:
        print('Generation file already exists!')

    for generation in range(0, number_of_generations):
        new_population = []

        population, scores = genetic.read_file(population_size, population_folder, wood_type, result_file_name)

        # allow members of the population to breed based on their relative score/rank;
        # if their score is higher they're more likely to breed
        for i in range(0, number_of_couples):
            parent_exception = -1       # -> no existing parent has negative index
            parent_1 = genetic.pick_mate(scores, parent_exception)
            parent_2 = genetic.pick_mate(scores, parent_1)
            child_1, child_2 = genetic.crossover(population[parent_1],
                                                 population[parent_2])
            new_population.append(child_1)
            new_population.append(child_2)

        # keep members of previous generation
        if keep_best_parent:
            new_population += [population[0]]  # Adds the best member from previous generation to list
        for i in range(0, number_of_parents_to_keep):
            parent_exception = 0    # best parent is exception
            keeper = genetic.pick_mate(scores, parent_exception)
            new_population += [population[keeper]]  # Adds some previous members to list (chosen by pick_mate())

        # mutate
        for i in range(0, len(new_population)):
            new_population[i] = genetic.mutate(new_population[i], mutation_probability, mutate_range_x,
                                               mutate_range_y, marimba_height, num_of_parameters)

        # add new random members
        while len(new_population) < population_size:
            new_population += [
                genetic.create_new_member(marimba_length, marimba_width_avr, marimba_height, num_of_parameters)]

        # make list of FEM calculated Eigenmodes/Frequencies of the current population and scores
        print(f'pre generation {generation}')
        new_frequencies = genetic.calculate_frequencies(new_population)     # this is the big FEM analysis that takes all the time
        print(f'post generation {generation}')
        new_scores = genetic.score_population(new_frequencies)

        # make matrix and file:
        matrix_generation = [[round(new_scores[i], 2), new_population[i],
                              itemgetter(0, 1, 2)(new_frequencies[i])] for i in range(population_size)]
        matrix_generation_sorted = sorted(matrix_generation, key=lambda l: l[0])
        genetic.write_file_generation(matrix_generation_sorted, population_folder, wood_type, result_file_name, population_properties)
