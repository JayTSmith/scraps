import unittest

from .computer_talk import *


class TestComputerTalk(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_room_creation(self):
        peeps = [Person() for x in range(6)]

        room = Room()
        room.add_people(*peeps)

        self.assertSequenceEqual(peeps, room.avail_people)

    def test_room_cycle(self):
        room = Room()
        room.add_people(Person(), Person(), Person(), Person(), Person(), Person())

        idle = Event(None, room, _type=Signal.IDLE, value=None)
        idle.fire()

        room.handle_queue()

        self.assertEqual(6, len(room.avail_people))

    def test_building_cycle(self):
        b = Building()
        for i in range(4):
            b.rooms.append(Room())
            b.rooms[i].add_people(Person(), Person(), Person(), Person(), Person())

        b_idle = Event(None, b, _type=Signal.IDLE, value=None)
        b_idle.fire()

        b.resolve_queues()
        self.assertEqual(20, sum([len(room.avail_people) for room in b.rooms]), "UH-OH WE MESSED IT!")
