from fish_lib import game

if __name__ == '__main__':
    fish = game.BasicGoFish(player_count=6)
    fish.do_full_round()

    line_sep_char = '#'

    win_string = '{1} Winners: {0}'.format(', '.join(['Player ' + p.name for p in fish.winner]),
                                           line_sep_char)
    sep = line_sep_char * len(win_string)
    print('\n{0}\n{1}\n{0}'.format(sep, win_string))
