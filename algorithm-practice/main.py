import cProfile
import os
import sys
import timeit

sys.path.append(os.path.join(os.getcwd(), 'algor_data'))
from algor_data import sorting, data
from data import UNSORTED_NUMBERS

if __name__ == '__main__':
    prof = cProfile.Profile()
    prof.enable()
    sorting.bubble_sort(list(UNSORTED_NUMBERS))
    prof.disable()
    prof.print_stats()

    # Sort Results when Number =
    # Bubble Sort Time:
    # Insertion Sort Time:
    # Merge Sort Time:

    # Sort Results when Number = 100
    # Bubble Sort Time:512.2189687800128
    # Insertion Sort Time:154.79481413506437
    # Merge Sort Time:10.762874175910838

    # Sort Results when Number = 10
    # Bubble Sort Time:51.66355023405049
    # Insertion Sort Time:15.585685932077467
    # Merge Sort Time:1.0821677109925076

    # Sort Results when Number = 1
    # Bubble Sort Time:5.228721752995625
    # Insertion Sort Time:1.597086961963214
    # Merge Sort Time:0.11947531893383712
