#!/usr/bin/env python
import time
import sys
import os
from modules import control, genetic

if __name__ == "__main__":

    # startTime = time.time()

    control.test_code()
    # genetic.build_single_bar(save_bar=True)
    # genetic.write_best_of_file(30, control.population_folder, control.wood_type, 30, control.result_file_name)

    os.execv(__file__, sys.argv)
    # endTime = time.time()
    # elapsed_time = endTime - startTime
    # print(f'Program needed {elapsed_time} seconds.')