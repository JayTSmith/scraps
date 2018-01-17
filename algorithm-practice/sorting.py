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
    length = len(_list)
    for i in range(length - 1):
        max_element = None
        cutoff_point = length - i
        active_list = _list[:cutoff_point]

        for j in range(cutoff_point):
            if max_element is None or active_list[j] > active_list[max_element]:
                max_element = j

        swap(_list, max_element, cutoff_point - 1)
    return _list
