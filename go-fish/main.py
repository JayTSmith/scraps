"""
The executable test script for fish_lib.

Author: Justin Smith
Date: 1/23/18
"""
from fish_lib import game


def main():
    """
    Executed when the script is ran as an executable script.
    :return: The fish_lib.BaseGame object created for testing.
    """
    fish = game.BasicGoFish(player_count=6)
    fish.do_full_round()

    line_sep_char = '#'

    win_string = '{1} Winners: {0}'.format(', '.join(['Player ' + p.name for p in fish.winner]),
                                           line_sep_char)
    sep = line_sep_char * len(win_string)
    print('\n{0}\n{1}\n{0}'.format(sep, win_string))
    return fish


def prof_main():
    from cProfile import Profile

    prof = Profile()
    prof.enable()
    fish = game.BasicGoFish(player_count=2)
    fish.do_full_round()
    prof.disable()

    line_sep_char = '#'

    win_string = '{1} Winners: {0}'.format(', '.join(['Player ' + p.name for p in fish.winner]),
                                           line_sep_char)
    sep = line_sep_char * len(win_string)
    print('\n{0}\n{1}\n{0}'.format(sep, win_string))

    prof.print_stats()
    return fish


if __name__ == '__main__':
    # Used if the script is used in an interactive environment
    prof_main()
