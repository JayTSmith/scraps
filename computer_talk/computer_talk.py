#!/usr/bin/env python3
# File Name: computer_talk.py
# Author: Justin Smith
# Date: 9/11/2017
# Purpose: To attempt to properly implement an event-queue style of processing.
########################################

###########################
# Core Section Begin
###########################
from enum import Enum
from random import randint, choice


class Utility(object):
    @staticmethod
    def rand_pop(l):
        return l.pop(randint(0, len(l) - 1))

    @staticmethod
    def get_values(enum):
        return [x for x in enum]

    @staticmethod
    def match_length(l, le, replace=None):
        """Extends or shrinks the list in order to make it a specified length
        l: list to modify
        le: length to match
        replace: element to use for extension"""
        if len(l) > le:
            return l[:le]
        if len(l) < le:
            return l + [None] * (le - len(l))
        return l

    @staticmethod
    def random_weighted(elements, weights):
        l_weights = Utility.match_length(weights, len(elements), 0)

        endpoint = sum(l_weights)
        index = randint(0, endpoint - 1)

        # Sum of the weights for the stepper
        running_total = 0

        for i in range(len(elements)):
            running_total += l_weights[i]
            if index < running_total:
                return elements[i]
        return None


class EventObject(object):
    """This class signifies that it is made to respond to Event objects. It has a generic print statement by default."""

    def handle_event(self, event):
        print('{} handled {} from {}.'.format(str(self), event, event.source))


###########################
# Core Section End
#
# Event Section Begin
###########################


class Signal(Enum):
    START = 'START'
    IDLE = 'IDLE'
    DEPARTURE = 'DEPARTURE'
    CON_END = 'CON_END'
    END = 'END'


class Converse(Enum):
    START = 'CON_START'
    GENERIC = 'GENERIC'
    JOKE = 'JOKE'
    QUESTION = 'QUESTION'
    APOLOGY = 'APOLOGY'
    DEPARTURE = 'DEPARTURE'


class PersonalityTraits(Enum):
    NO_FILTER = 'NO_FILTER'
    INTROVERT = 'INTROVERT'
    EXTROVERT = 'EXTROVERT'
    TALKATIVE = 'TALKATIVE'
    LISTENS = 'GOOD_LISTENER'
    NOSY = 'NOSY'
    CARING = 'CARING'
    IMMATURE = 'IMMATURE'
    DEPRESSED = 'DEPRESSED'
    BASIC = 'BASIC'
    HIPSTER = 'HIPSTER'


class MessageTraits(Enum):
    SERIOUS = 'SERIOUS'
    SAD = 'SAD'
    JOKE = 'JOKE'
    # Dark as in dark humor
    DARK = 'DARK'
    # Jab is like a roast
    JAB = 'JAB'
    # Culture = Reference
    CULTURE = 'CULTURE'
    SILENCE = 'SILENCE'


class Event(object):
    def __init__(self, source, target, _type=None, value=None):
        self.source = source
        self.target = target
        self.type = _type
        self.value = value
        self.available = True

    def consume(self):
        if self.available:
            self.available = False

    def fire(self):
        if isinstance(self.target, EventObject):
            self.target.handle_event(self)
        else:
            print('I have no target! {}'.format(str(self)))

    def __bool__(self):
        return self.available

    def __str__(self):
        return str(self.type)


###########################
# Event Section End
#
# Program Section Begin
###########################

class Building(EventObject):
    def __init__(self):
        super(Building, self).__init__()
        self.rooms = []
        self.people = []

    def move_to_room(self, person=None):
        """Moves a person to another room."""
        chosen = person
        if person is None:
            chosen = choice(self.people)

        new_room = choice(self.rooms)
        while chosen in new_room.avail_people:
            new_room = choice(self.rooms)

        new_room.avail_people.append(chosen)

        return

    def handle_event(self, event):
        super(Building, self).handle_event(event=event)

        if isinstance(event, Event) and event.available:
            if event.type == Signal.IDLE:
                for r in self.rooms:
                    idle = Event(self, r, _type=Signal.IDLE, value=None)
                    idle.fire()

    def resolve_queues(self):
        for room in self.rooms:
            room.handle_queue()


class Room(EventObject):
    base_converse_chance = 85

    def __init__(self, building=None):
        super(EventObject, self).__init__()
        self.avail_people = []
        self.building = building if isinstance(building, Building) else None
        self.conversations = set()
        self.event_queue = []

    def add_people(self, *people):
        for person in people:
            if person.name == 'NONAME-PERSON':
                person.name = 'Person-{}'.format(len(self.avail_people))
            self.avail_people.append(person)

    def create_new_con(self):
        if len(self.avail_people) >= 2:
            peeps = [Utility.rand_pop(self.avail_people), Utility.rand_pop(self.avail_people)]
            while randint(0, 1) and self.avail_people:
                peeps.append(Utility.rand_pop(self.avail_people))
            return Conversation(self, *peeps, name=self.new_con_name())
        else:
            return None

    def new_con_name(self):
        return 'Conversation-{}'.format(len(self.conversations))

    def handle_event(self, event):
        super(Room, self).handle_event(event=event)

        if isinstance(event, Event) and event:
            if event.type == Signal.IDLE:
                # self.notify_all(IdleEvent)

                # Conversation Section
                converse_attempts = randint(1, 6)
                print('Going to try and start {} Conversations!'.format(converse_attempts))
                while converse_attempts and len(self.avail_people) > 1:
                    if randint(1, 100) <= Room.base_converse_chance:
                        new_con = self.create_new_con()
                        if new_con:
                            self.conversations.add(new_con)
                            self.event_queue.append(Event(self, new_con, _type=Converse.START))
                    converse_attempts -= 1
                print('Now have {} Conversations.'.format(len(self.conversations)))

                for converse in self.conversations:
                    self.event_queue.append(Event(self, converse, _type=Signal.IDLE))
            elif event.type == Signal.CON_END:
                if event.source in self.conversations:
                    self.conversations.remove(event.source)
                    for person in event.source.people:
                        person.conversation = None
                        self.avail_people.append(person)
            elif event.type == Signal.DEPARTURE:
                if event.source in self.avail_people and self.building is not None:
                    print('Moving {} to another room!'.format(event.source))
                    self.avail_people.remove(event.source)
                    self.building.move_to_room(person=event.source)

    def handle_queue(self):
        while self.event_queue:
            self.event_queue.pop(0).fire()

    def __str__(self):
        return 'Room(Conversations:{} People:{})'.format(len(self.conversations), len(self.avail_people))


class Conversation(EventObject):
    def __init__(self, room, *people, **kwargs):
        super(Conversation, self).__init__()
        if not isinstance(room, Room):
            raise TypeError('Argument supplied was wrong type! Required: Room')
        self.name = kwargs.get('name', 'NONAME-CON')

        self.room = room
        self.people = list(people)
        self.last_talker = None
        # If it is already marked for CON_END.
        self.marked = False

        for person in self.people:
            person.conversation = self

    def handle_event(self, event):
        super(Conversation, self).handle_event(event=event)

        if isinstance(event, Event) and event.available:
            try:
                if event.type == Converse.START:
                    for peep in self.people:
                        self.room.event_queue.append(Event(self, peep, _type=Converse.START))
                elif event.type == Converse.GENERIC:
                    # Gets whoever talked last, they will get hit with the next event.
                    if self.last_talker is not None:
                        target = self.last_talker
                    else:
                        target = choice([person for person in self.people if person != event.source])
                    self.last_talker = event.source

                    # The Conversation acts a hub for the people within. It's up to the people to play it safe.
                    for peep in self.people:
                        if peep != self.last_talker:
                            self.room.event_queue.append(Event(event.source, peep, _type=event.type,
                                                               value=(target, event.value[1])))
                elif event.type == Converse.DEPARTURE:
                    if event.source in self.people and event.source.conversation == self:
                        self.people.remove(event.source)
                        event.source.conversation = None
                        self.room.avail_people.append(event.source)
                    if len(self.people) < 2 and not self.marked:
                        self.room.event_queue.append(Event(self, self.room, _type=Signal.CON_END))
                        self.marked = True

            except AttributeError as e:
                # Means more than likely, this wasn't an event that Conversation was made to handle.
                print(e)

    def __str__(self):
        return self.name


class Person(EventObject):
    def __init__(self, **kwargs):
        super(EventObject, self).__init__()
        self.name = kwargs.get('name', 'NONAME-PERSON')
        self.conversation = None

        self.traits = None
        self.weight_map = dict()

        self.build_traits()
        self.generate_weight_map()

    def build_traits(self):
        assigned_traits = set()
        possible_traits = Utility.get_values(PersonalityTraits)
        num_of_traits = randint(0, len(possible_traits) - 1)

        for i in range(num_of_traits):
            assigned_traits.add(choice(possible_traits))
        self.traits = tuple(assigned_traits)

    def generate_weight_map(self):
        for t in MessageTraits:
            self.weight_map[t] = 1

        if PersonalityTraits.BASIC in self.traits:
            self.weight_map[MessageTraits.CULTURE] += 3
        if PersonalityTraits.NO_FILTER in self.traits:
            self.weight_map[MessageTraits.SERIOUS] += 1
            self.weight_map[MessageTraits.SAD] += 1
            self.weight_map[MessageTraits.JOKE] += 2
            self.weight_map[MessageTraits.DARK] += 2
        if PersonalityTraits.CARING in self.traits:
            self.weight_map[MessageTraits.SERIOUS] += 3
        if PersonalityTraits.EXTROVERT in self.traits:
            self.weight_map[MessageTraits.SILENCE] -= 4
        if PersonalityTraits.INTROVERT in self.traits:
            self.weight_map[MessageTraits.SILENCE] += 4
        if PersonalityTraits.HIPSTER in self.traits:
            self.weight_map[MessageTraits.CULTURE] -= 3
        if PersonalityTraits.TALKATIVE in self.traits:
            self.weight_map[MessageTraits.SILENCE] += 1
        if PersonalityTraits.DEPRESSED in self.traits:
            self.weight_map[MessageTraits.SAD] += 2

    def generate_message_trait(self):
        traits = list(self.weight_map.keys())
        weights = list(self.weight_map.values())

        return Utility.random_weighted(traits, weights)

    def handle_event(self, event):
        super(Person, self).handle_event(event=event)

        if isinstance(event, Event) and event.available:
            try:
                if event.type == Converse.START:
                    self.conversation.room.event_queue.append(Event(self, self.conversation,
                                                                    _type=Converse.GENERIC,
                                                                    value=(self, self.generate_message_trait())))
                # May need to be put into a separate method.
                elif event.type == Converse.GENERIC and event.value[0] == self:
                    self.conversation.room.event_queue.append(Event(self, self.conversation,
                                                                    _type=Converse.DEPARTURE, value=self))

                    # Rolls to see if they are going to leave the room.
                    if randint(0, 1):
                        self.conversation.room.event_queue.append(Event(self, self.conversation.room,
                                                                        _type=Signal.DEPARTURE, value=self))
            except AttributeError:
                # Look at Conversation
                pass

    def __str__(self):
        return '{}({})'.format(self.name, str(self.conversation))

###########################
# Program Section End
###########################
