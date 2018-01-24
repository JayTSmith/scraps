from . import data
from random import randint


def shuffle(_list):
    for element in _list:
        _list.append(_list.pop(randint(0, len(_list) - 1)))
    return _list


def swap(_list, i1, i2):
    """
    Swaps the elements at the two indices specified.
    :param _list: The list that contains both elements.
    :param i1: The index of the first element to be swapped.
    :param i2: The index of the second element to be swapped.
    :return: Nothing.
    """
    _list[i1], _list[i2] = _list[i2], _list[i1]


def bogo_sort(_list):
    """
    An implementation of bogo-sort according to the bland definition of it.

    DO NOT EVER USE THIS ALGORITHM!!!
    Estimated time for sorting 10000 numbers: 9 X 10^35652 years

    :param _list: The list to be sorted.
    :return: The sorted list.
    """
    is_sorted = True
    for i in range(len(_list) - 1):
        if _list[i] > _list[i + 1]:
            is_sorted = False

    while not is_sorted:
        shuffle(_list)
        is_sorted = True
        for i in range(len(_list) - 1):
            if _list[i] > _list[i + 1]:
                is_sorted = False
                break

    return _list

def bubble_sort(_list):
    """
    An implementation of bubble sort according to the bland definition of it.
    :param _list: The list to be sorted
    :return: The sorted list.
    """
    for i in range(len(_list), 0, -1):
        max_element = 0
        active_list = _list[:i]

        for j in range(i):
            max_element = j if active_list[j] > active_list[max_element] else max_element

        swap(_list, max_element, i - 1)
    return _list


def insertion_sort(_list):
    """
    An implementation of insertion sort according to the bland definition of it.
    :param _list: The list to be sorted
    :return: The sorted list
    """
    final_list = [_list[0]]
    for i, i_ele in enumerate(_list[1:]):
        insert_index = len(final_list)
        # Scan if the index needs to be changed.
        for j in range(len(final_list)):
            if i_ele < final_list[j]:
                insert_index = j
                break
        final_list.insert(insert_index, i_ele)

    return final_list


def merge_sort(_list):
    """
    An implementation of merge sort according to the bland definition of it.
    :param _list: The list to be sorted
    :return: The sorted list
    """
    if len(_list) < 2:
        return _list

    left = merge_sort(_list[0:len(_list) // 2])
    right = merge_sort(_list[len(_list) // 2:len(_list)])
    left_idx, right_idx = 0, 0

    final = []
    while left_idx < len(left) or right_idx < len(right):
        left_ele = left[left_idx] if left_idx < len(left) else float('-inf')
        right_ele = right[right_idx] if right_idx < len(right) else float('-inf')

        if left_ele == float('-inf'):
            right_idx += 1
            final.append(right_ele)
            continue

        if right_ele == float('-inf'):
            left_idx += 1
            final.append(left_ele)
            continue

        if left_ele < right_ele:
            left_idx += 1
            final.append(left_ele)
            continue
        right_idx += 1
        final.append(right_ele)

    return final