#!/usr/bin/env python3
# File Name: ai_game.py
# Author: Justin Smith
# Date: 11/6/2017
# Purpose: Develop a closed minded AI that can play this game.
import random
import sys

from io import StringIO


class AI(object):

    def __init__(self):
        self._input = StringIO()
        self._output = StringIO()
        self.org_out = None
        self.org_in = None
        self.options = {'A': 0, 'B': 0, 'C': 1, 'D': 0, 'E': 0, 'Q': 0}

    def _reset_weights(self):
        for opt in self.options:
            self.options[opt] = 0
        # Naturally, we want to be moving.
        self.options['C'] = 1

    def _process_input(self):
        self._input.seek(0)
        true_in = self._input.read()
        print(true_in, file=self.org_out)
        self._reset_in()
        return true_in

    def _reset_in(self):
        self._input = StringIO()
        sys.stdout = self._input

    def hook(self):
        self.org_in = sys.stdin
        sys.stdin = self._output

        self.org_out = sys.stdout
        sys.stdout = self._input

    def restore(self):
        if self.org_in and self.org_out:
            sys.stdin = self.org_in
            sys.stdout = self.org_out

            self.org_in = self.org_out = None
        else:
            print('We haven\'t hooked into the input and output yet.')

    def consider_options(self):
        true_in = self._process_input()
        # Native Distance check
        if 'The natives are getting close!' in true_in:
            print('Danger on the horizon!', file=self.org_out)
            self.options['C'] += 1
        if 'The natives are getting really close!' in true_in:
            print('Danger close!', file=self.org_out)
            self.options['C'] += 1

        # Camel check
        if 'Your camel is getting tired' in true_in:
            print('Camel thirsty!', file=self.org_out)
            self.options['D'] += 5

        # Thirst check
        if 'You are thirsty' in true_in:
            print('Person thirsty!', file=self.org_out)
            self.options['A'] += 5

        # Oasis check
        if 'You found the oasis' in true_in:
            print('Oasis found!', file=self.org_out)
            self.options['A'] = 0
            self.options['D'] = 0

        return sorted(self.options.items(), key=lambda k: k[1], reverse=True)[0][0]

    def get_choice(self):
        choice = self.consider_options()
        print(choice, file=self.org_out)
        self._reset_weights()
        return choice

    def get_weights(self):
        pass


ai_instance = AI()


def get_input(prompt=None):
    global ai_instance

    if sys.stdin == ai_instance._output:
        return ai_instance.get_choice()
    else:
        return input(prompt)

# This script comes from Steven Thompson (https://github.com/Sthomp123/program-arcade-games)


""" This is a game about making your way across the desert on a stolen camel while trying to outrun the natives"""

OASIS_CHECK = 5

# These variables are the base mechanics of the game.
total_miles_traveled = 0
thirst = 0
camel_tiredness = 0
drinks_in_canteen = 3
native_location = -20


def main():
    global thirst, camel_tiredness, drinks_in_canteen
    print("Welcome to Camel!")
    print("You have stolen a camel to make your way across the great Mobi desert.")
    print("The natives want their camel back and are chasing you down!\nSurvive your desert trek and out run the natives.")

    # This is what keeps the game going. If it gets set to true, then the game ends.
    done = False

    def check_camel():
        global camel_tiredness

        lost = False
        if 5 <= camel_tiredness <= 8:
            print("Your camel is getting tired.")
        if camel_tiredness > 8:
            print("Your camel is dead.")
            lost = True
        return lost

    def check_native():
        global native_location

        lost = False
        if native_location >= 0:
            print('The natives have caught you.')
            lost = True
        elif -2 <= native_location <= -10:
            print('The natives are getting really close!')
        elif -10 <= native_location <= -15:
            print('The natives are getting close!')
        return lost

    def check_oasis():
        global OASIS_CHECK, camel_tiredness, thirst, drinks_in_canteen

        if random.randint(1, 20) == OASIS_CHECK:
            print("You found the oasis")
            thirst = 0
            camel_tiredness = 0
            drinks_in_canteen = 4

    def check_thirst():
        global thirst

        lost = False
        if 4 <= thirst <= 6:
            print("You are thirsty.")
        if thirst > 6:
            print("You died of thirst!")
            lost = True
        return lost

    def check_travel():
        global total_miles_traveled

        if total_miles_traveled >= 200:
            print('You have won! Good job.')
        return total_miles_traveled >= 200

    def move_native(player_miles):
        global native_location

        native_location += (random.randint(7, 14) - player_miles)

    def travel(miles):
        global total_miles_traveled, thirst, camel_tiredness, native_location
        total_miles_traveled += miles
        move_native(miles)

    while not done:
        # these are possible choices for your character
        print("A. Drink from your canteen.")
        print("B. Ahead moderate speed.")
        print("C. Ahead full speed.")
        print("D. Stop for the night.")
        print("E. Status check.")
        print("Q. Quit.")
        # this line allows you to select a choice from above.
        user_choice = get_input("Your choice? ")
        # If you select Q then the game ends.
        if user_choice.upper() == "Q":
            break

        # If You select E then it will show you all the necessary stats to get you across the desert safely
        elif user_choice.upper() == "E":
            print("Miles Traveled:", total_miles_traveled)
            print("Drinks in canteen:", drinks_in_canteen)
            print("The natives are", native_location * (-1), "miles behind you.")
            print("Camel tiredness:", camel_tiredness)
            print("Thirst", thirst)

        # If you select D then the tiredness of your camel is reset and the natives move in closer on your location
        elif user_choice.upper() == "D":
            camel_tiredness = 0
            print("The camel is happy")
            move_native(0)
            done = check_native()

        # If you select C then you will move a random integer between 10 and 20 forward and there is also a 1 in 20 chance of finding an oasis
        elif user_choice.upper() == "C":
            miles_traveled = random.randint(10, 20)
            travel(miles_traveled)
            print("You traveled", miles_traveled, "miles")
            thirst += 2
            camel_tiredness += 2
            done = check_native() or check_thirst() or check_camel() or check_travel()
            check_oasis()

        # If you select B then you will move forward a random integer between 5 and 12. This also has a 1 in 20 chance of finding an oasis
        elif user_choice.upper() == "B":
            miles_traveled = random.randint(5, 12)
            travel(miles_traveled)
            print("You traveled", miles_traveled, "miles.")
            thirst += 1
            camel_tiredness += 1
            done = check_native() or check_thirst() or check_camel() or check_travel()
            check_oasis()

        # if you select A then you will take a drink from your canteen
        elif user_choice.upper() == "A":
            if drinks_in_canteen > 0:
                drinks_in_canteen = drinks_in_canteen - 1
                thirst = 0
                print("You have", drinks_in_canteen, "drinks left.")
            else:
                print("You're out of water")


if __name__ == '__main__':
    ai_instance.hook()
    main()
    ai_instance.restore()
    if total_miles_traveled >= 200:
        print('We probably won!')
    else:
        print('You dead.')
