#!/usr/bin/env python3
# Prog In
# Justin Smith
# November 3, 2017

"""Attempts to load input from a file into a python script."""

import sys

from io import StringIO

FILE_IN = './user_input.txt'
STDIN = sys.stdin


def sideload_in():
    """Changes the standard input to the file specified in FILE_IN"""
    global FILE_IN

    sys.stdin = StringIO(read_contents(FILE_IN))


def restore_in():
    """Changes the standard input back to its default value"""
    global STDIN

    sys.stdin = STDIN


def read_contents(path):
    """Returns the contents of a file from a path
    :param path the path of file
    :return the content of the file found from the path param."""
    with open(path, 'r') as file:
        return file.read()


def test():
    """Testing method for the script's main intent."""
    sideload_in()
    # Because it is loaded in from a file, it does not go to a newline automatically.
    file_in = input('Say something:\n')
    restore_in()
    usr_in = input('Now you say something: ')
    print('Usr_in\'s value:', usr_in)
    print('File_in\'s value:', file_in)


if __name__ == '__main__':
    test()
