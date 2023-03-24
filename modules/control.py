import copy
import numpy as np
from operator import itemgetter
from modules import genetic

# variables:
genetic.fundamental = 130.813  # Fundamental Frequency of marimba Bar 130.8 == C3
marimba_length, marimba_width_avr, marimba_height = 440.4, 68.58, 28.96
num_of_parameters = 4       # free (x,y) koordinates
population_folder = 4       # folder is called 'population{population_folder}'
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
                             mutation_probability, mutate_range_x, mutate_range_y]

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

        # allow members of the population to breed based on their relative score;
        # if their score is higher they're more likely to breed
        for i in range(0, number_of_couples):
            parent_exception = -1       # -> no existing parent has negative index
            parent_1 = genetic.pick_mate(scores, parent_exception)
            parent_2 = genetic.pick_mate(scores, parent_1)
            child_1, child_2 = genetic.crossover(population[parent_1],
                                                 population[parent_2])     # TODO must be two different individuals (solved?)
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

        # make list of FEM calculated Eigenmodes/ Frequencies of the current population and scores
        print(f'pre generation {generation}')
        new_frequencies = genetic.calculate_frequencies(new_population)     # this is the big FEM analysis that takes all the time
        print(f'post generation {generation}')
        new_scores = genetic.score_population(new_frequencies)

        # make matrix and file:
        matrix_generation = [[round(new_scores[i], 2), new_population[i],
                              itemgetter(0, 1, 2)(new_frequencies[i])] for i in range(population_size)]
        matrix_generation_sorted = sorted(matrix_generation, key=lambda l: l[0])
        genetic.write_file_generation(matrix_generation_sorted, population_folder, wood_type, result_file_name, population_properties)


def old_code():
    # parameters
    population_size = 20
    number_of_generations = 2
    number_of_couples = 8
    number_of_parents_to_keep = 0   # the best parent is always kept
    mutation_probability = 0.1
    mutate_range_x, mutate_range_y = 10, 3

    # final lists
    all_members, all_members_generation = [], []    # a big list of all values of all members of all populations
    all_scores, all_scores_generation = [], []      # 1. blank, 2. separated in generations
    all_frequencies, all_frequencies_generation = [], []

    # create the starting population
    #population = genetic.make_first_population(population_size, marimba_length, marimba_width_avr, marimba_height, num_of_parameters)
    population = genetic.read_file(population_size)

    last_score = 10000000

    for generation in range(0, number_of_generations):
        new_population = []

        if generation > 0:
            population = genetic.read_file(population_size)

        # make list of FEM calculated Eigenmodes/ Frequencies of the current population
        frequencies = genetic.calculate_frequencies(population)

        # evaluate the fitness of the current population
        scores = genetic.score_population(frequencies)
        # print(f'Scores of Generation {i}:{scores}')

        best_values = population[np.argmin(scores)]
        best_object = population.index(best_values)
        best_score = scores[best_object]

        if best_score != last_score:
            print(f'Generation {generation}: Best so far is a score of {best_score}... The values are: {best_values}')

        if generation == 0:
            all_members.clear()    # if the GA starts, the list starts empty
            all_scores.clear()
            all_frequencies.clear()

        all_scores_generation.clear(), all_members_generation.clear(), all_frequencies_generation.clear()

        # allow members of the population to breed based on their relative score;
        # i.e., if their score is higher they're more likely to breed
        for i in range(0, number_of_couples):
            new_1, new_2 = genetic.crossover(population[genetic.pick_mate(scores)],
                                             population[genetic.pick_mate(scores)])
            new_population.append(new_1)
            new_population.append(new_2)

        # mutate
        for i in range(0, len(new_population)):
            new_population[i] = genetic.mutate(new_population[i], mutation_probability, mutate_range_x, mutate_range_y, marimba_height, num_of_parameters)

        # keep members of previous generation
        new_population += [best_values]  # Adds the best member from previous generation to list
        for i in range(0, number_of_parents_to_keep):
            keeper = genetic.pick_mate(scores)
            new_population += [population[keeper]]  # Adds some previous members to list (chosen by pick_mate())

        # add new random members
        while len(new_population) < population_size:
            new_population += [genetic.create_new_member(marimba_length, marimba_width_avr, marimba_height, num_of_parameters)]

        # replace the old population with a real copy
        population = copy.deepcopy(new_population)

        # Make lists of all members, all scores and all frequencies of all generations
        all_members.extend(population)
        all_members_generation.extend(population)
        all_scores.extend(scores)
        all_scores_generation.extend(scores)
        all_frequencies.extend(frequencies)
        all_frequencies_generation.extend(frequencies)

        matrix_generation = [[round(all_scores_generation[i], 2), all_members_generation[i], itemgetter(0, 3, 9)(all_frequencies_generation[i])] for i in range(len(all_scores_generation))]
        matrix_generation_sorted = sorted(matrix_generation, key=lambda l: l[0])
        genetic.write_file_generation(matrix_generation_sorted)

        last_score = best_score

        # print(f'Generation {i} finished successful!')

    matrix = [[round(all_scores[i], 2), all_members[i], itemgetter(0, 3, 9)(all_frequencies[i])] for i in range(len(all_scores))]
    matrix_sorted = sorted(matrix, key=lambda l: l[0])

    # genetic.write_file_sorted(matrix_sorted)

    # genetic.build_best_bar(matrix_sorted)

