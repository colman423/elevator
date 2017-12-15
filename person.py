import threading
import time
import random
import STATE
import GUI
from CONST import *
from elevator import Elevator

# floor_lock = [threading.Lock()] * FLOOR   # not useful, this will point all element to same lock
floor_lock = list()  # create a list of thread lock for every floor

global elevator
def main():

    for i in range(0, FLOOR):  # initial locks at every floor
        _lock = threading.Lock()
        _lock.acquire()
        floor_lock.append(_lock)


    global elevator
    elevator = Elevator()
    # elevator = Elevator(floor_lock)
    elevator.start()

    RandomAccessFloor().start()  # start random access floors
    RandomCreatePeople(100).start()  # start creating people


class Person(threading.Thread):  # inherit thread
    state = None
    init_at = -1
    init_to = -1
    init_at_lock = None
    init_to_lock = None
    GUI_person = None

    def __init__(self, name, init_at, init_at_lock, init_to, init_to_lock):
        super(Person, self).__init__(name=name)
        self.init_at = init_at  # floor where he call elevator
        self.init_to = init_to  # floor where he want to arrive
        self.init_at_lock = init_at_lock  # get the lock at the floor where he call elevator
        self.init_to_lock = init_to_lock  # get the lock at the floor where he want to arrive
        self.GUI_person = GUI.create_person(init_at)  # get the person ui

    def start(self):
        self.call_elevator()  # call the elevator
        super().start()

    def run(self):
        while True:  # run and run and run

            if self.state == STATE.WAITING:  # if this person is waiting elevator
                print("{0} is waiting elevator at floor {1}".format(self.name, self.init_at))
                self.init_at_lock.acquire()  # waiting the elevator to release that floor's lock
                self.state = STATE.ENTERING  # after lock released, switch state into entering elevator

            elif self.state == STATE.ENTERING:  # if this person is walking enter elevator
                print("{0} is entering elevator".format(self.name))
                enter_completed = GUI.person_entering(self.GUI_person)  # maybe some GUI represent here
                if enter_completed:
                    self.state = STATE.TRANSPORTING
                    self.init_at_lock.release()  # release lock resource to other people

            elif self.state == STATE.TRANSPORTING:  # if this person is taking elevator
                print("{0} is taking elevator to floor {1}".format(self.name, self.init_to))
                self.init_to_lock.acquire()  # waiting the elevator to release that floor's lock
                self.state = STATE.LEAVING  # after lock released, switch state into leaving elevator
                self.init_to_lock.release()  # release lock resource to other people

            elif self.state == STATE.LEAVING:  # if this person is leaving elevator
                print("{0} is leaving elevator".format(self.name))
                leave_complete = GUI.person_leaving(self.GUI_person)  # maybe some GUI represent here
                if leave_complete:
                    return
                    # del self  # will this line work??

            else:
                print("{0} has bug QQ".format(self.name))

            time.sleep(0.1)  # set person frame

    def call_elevator(self):  # not complete
        print("{0} call_elevator, from {1} to {2}".format(self.name, self.init_at, self.init_to))
        self.state = STATE.WAITING  # called elevator, now's state is waiting elevator
        elevator.set_new_passenger(self.init_at, self.init_to)
        # todo: some elevator function there


class RandomCreatePeople(threading.Thread):
    prob = 0

    def __init__(self, prob):
        self.prob = prob
        super(RandomCreatePeople, self).__init__()

    def run(self):
        i = 0  # no. of the person
        while True:
            p = random.randrange(0, 100)  # should change a way later
            if p < self.prob:
                name = "person-" + str(i)
                at = random.randrange(0, FLOOR)  # random assign a floor
                to = random.randrange(0, FLOOR)  # random assign a floor
                Person(name, at, floor_lock[at], to, floor_lock[to]).start()
                i += 1
            time.sleep(2)


class RandomAccessFloor(threading.Thread):
    # no elevator class now, but for demo, this function let elevator random stop at random floor
    def __init__(self):
        super(RandomAccessFloor, self).__init__()

    def run(self):
        while True:
            f = random.randrange(0, FLOOR)
            print("elevator open at floor {0}".format(f))
            for l in floor_lock:
                if not l.locked():
                    l.acquire()
            floor_lock[f].release()
            time.sleep(2)
