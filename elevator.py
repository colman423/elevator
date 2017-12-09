import threading
import time
from collections import defaultdict, OrderedDict

class Elevator(threading.Thread):
    def __init__(self):
        super().__init__(name="elevator")
        self.toPass = []
        self.waiting_list = defaultdict(list)
        self.waiting_num = 0
        # self.lock = threading.Lock()
        self.passenger_num = 0
        self.active = False
        self.fromFloor = 0
        self.toFloor = 0

    def take_passenger(self, atFloor):
        self.toFloor = atFloor
        self.passenger_num += 1
        print("Elevator move from {} to {} ({} peoples in elevator)".format(self.fromFloor, self.toFloor, self.passenger_num))

    def transport(self, toFloor):
        self.fromFloor = self.toFloor
        self.toFloor = toFloor
        self.passenger_num -= 1
        print("Elevator move from {} to {} ({} peoples in elevator)".format(self.fromFloor, self.toFloor, self.passenger_num))
        print("DEACTIVE")
        self.fromFloor = self.toFloor
        self.active = False

    def set_new_passenger(self, atFloor, toFloor):
        if atFloor == toFloor:
            return
        self.waiting_list[atFloor].append((atFloor, toFloor))
        self.waiting_num += 1

    def get_passenger_from_waiting(self):
        if self.active == False:
            print("ACTIVE")
            self.active = True
            # print(self.waiting_list.items())
            # print(sorted(self.waiting_list.items(), key= lambda t: len(t[1])))
            # print(sorted(self.waiting_list.items(), key= lambda t: len(t[1])).pop()[0])
            floor = sorted(self.waiting_list.items(), key= lambda t: len(t[1])).pop()[0]
            atFloor, toFloor = self.waiting_list[floor].pop()
            self.waiting_num -= 1
            self.take_passenger(atFloor)
            self.transport(toFloor)      

    def run(self):
        while True:
            time.sleep(0.1)
            if len(self.toPass) == 0 and self.waiting_num != 0:
                self.get_passenger_from_waiting()


                
if __name__ == "__main__":
    elevator =  Elevator()
    elevator.start()
    import random
    # for i in range(10):
    while True:
        atFloor, toFloor = random.randrange(0, 10), random.randrange(0, 10)
        print()
        print('passenger:', atFloor, toFloor)
        newPassenger = threading.Thread(target=elevator.set_new_passenger, args=(atFloor, toFloor, ))
        newPassenger.start()
        time.sleep(3)