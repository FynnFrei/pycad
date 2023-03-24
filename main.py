#!/usr/bin/env python
import time
import sys
import os
from modules import control, genetic

if __name__ == "__main__":

    repeat = True
    fem_full = True
    best_of_file = False
    build_single_bar = False

    startTime = time.time()

    if fem_full:
        control.test_code()
    if best_of_file:
        genetic.write_best_of_file(30, control.population_folder, control.wood_type, 30, control.result_file_name)
    if build_single_bar:
        genetic.build_single_bar(save_bar=True)
    # TODO fix: Illegal storage access...
    # <Exception> Illegal storage access! Please save your work under a new file name and restart the application!
    # Recompute failed! Please check report view.
    endTime = time.time()
    elapsed_time = endTime - startTime
    print(f'Program needed {elapsed_time} seconds.')

    if fem_full and repeat:
        os.execv(sys.executable, ['python'] + sys.argv)
