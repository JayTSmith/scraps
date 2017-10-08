#!/usr/bin/env python3
# File Name: computer_talk.py
# Author: Justin Smith
# Date: 9/11/2017
# Purpose: To attempt to properly implement an event-queue style of processing.
########################################

###########################
# Core Section Begin
###########################

import weakref

from enum import Enum
from random import randint, choice


class Utility(object):
    @staticmethod
    def rand_pop(l):
        return l.pop(randint(0, len(l)-1))


class EventObject(object):
    def __init__(self):
        self._listeners = set()

    """Code is commented in this class because it is of a different paradigm - 
    EventListeners rather than a centralized listener."""

    # @property
    # def listeners(self):
    #     return self._listeners
    #
    # def attach_listeners(self, *listeners):
    #     for listener in listeners[0]:
    #         if isinstance(listener, EventObject):
    #             self._listeners.add(weakref.ref(listener))
    #
    # def clean_listeners(self):
    #     for listener in self._listeners:
    #         if not listener():
    #             self._listeners.remove(listener)
    #
    # def remove_listeners(self, *listeners):
    #     for listener in listeners:
    #         for ref in weakref.getweakrefs(listener):
    #             if ref in self._listeners:
    #                 self._listeners.remove(ref)

    def handle_event(self, event):
        print('{} handled {} from {}.'.format(str(self), event, event.source))

    # def notify_all(self, event=None):
    #     for listener in self._listeners:
    #         listener().handle_event(event)

###########################
# Core Section End
#
# Event Section Begin
###########################


class Signal(Enum):
    START = 'START'
    IDLE = 'IDLE'
    CON_END = 'CON_END'
    END = 'END'


class Converse(Enum):
    START = 'CON_START'
    GENERIC = 'GENERIC'
    JOKE = 'JOKE'
    QUESTION = 'QUESTION'
    APOLOGY = 'APOLOGY'
    DEPARTURE = 'DEPARTURE'


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


class Room(EventObject):
    base_converse_chance = 85
    
    def __init__(self):
        super(EventObject, self).__init__()
        self.avail_people = []
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
        # Because of the fact that it is the argument, we must get the list from the arg.
        self.people = list(people)
        self.last_talker = None
        # If it is already marked for CON_END.
        self.marked = False

        for person in self.people:
            person.conversation = self

    def handle_event(self, event):
        super(Conversation, self).handle_event(event=event)

        if isinstance(event, Event):
            try:
                if event.type == Converse.START:
                    for peep in self.people:
                        self.room.event_queue.append(Event(self, peep, _type=Converse.START))
                elif event.type == Converse.GENERIC:
                    if self.last_talker is not None:
                        target = self.last_talker
                    else:
                        target = choice([person for person in self.people if person != event.source])
                    self.last_talker = event.source
                    self.room.event_queue.append(Event(event.source, target, _type=event.type))
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

    def handle_event(self, event):
        super(Person, self).handle_event(event=event)

        if isinstance(event, Event):
            try:
                if event.type == Converse.START:
                    self.conversation.room.event_queue.append(Event(self, self.conversation,
                                                                    _type=Converse.GENERIC, value=self))
                elif event.type == Converse.GENERIC:
                    self.conversation.room.event_queue.append(Event(self, self.conversation,
                                                                    _type=Converse.DEPARTURE, value=self))
            except AttributeError:
                # Look at Conversation
                pass

    def __str__(self):
        return '{}({})'.format(self.name, str(self.conversation))
        
###########################
# Program Section End
#
# Testing Section Beginning
###########################


def main():
    test_room = Room()
    idle = Event(None, test_room, _type=Signal.IDLE)
    peeps = [Person() for x in range(6)]
    test_room.add_people(*peeps)

    idle.fire()
    return test_room


if __name__ == '__main__':
    room = main()
    room.handle_queue()
    print(list(map(str, room.avail_people)))
###########################
# Testing Section End
###########################
