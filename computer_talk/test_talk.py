from .computer_talk import *
import unittest


class TestComputerTalk(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_room_creation(self):
        peeps = [Person() for x in range(6)]

        room = Room()
        room.add_people(*peeps)

        self.assertSequenceEqual(peeps, room.avail_people)

    def test_room_cycle(self):
        peeps = [Person() for x in range(6)]

        room = Room()
        room.add_people(*peeps)

        idle = Event(None, room, _type=Signal.IDLE, value=None)
        idle.fire()

        room.handle_queue()

        self.assertCountEqual(peeps, room.avail_people)