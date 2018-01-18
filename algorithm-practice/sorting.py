from .algor_data import data
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


def bubble_sort(_list):
    """
    An implementation of bubble sort according to the bland definition of it.
    :param _list: The list to be sorted
    :return: The sorted list.
    """
    for i in range(len(_list) - 1):
        max_element = None
        active_list = _list[:len(_list) - i]

        for j in range(len(active_list)):
            if max_element is None or active_list[j] > active_list[max_element]:
                max_element = j

        swap(_list, max_element, len(active_list) - 1)
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
