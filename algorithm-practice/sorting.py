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
