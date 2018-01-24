from fish_lib import game

if __name__ == '__main__':
    fish = game.BasicGoFish(player_count=4)
    fish.do_full_round()
    print('Winners: {}'.format(', '.join(['Player ' + p.name for p in fish.winner])))
