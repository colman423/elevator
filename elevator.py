import threading
import time
from collections import defaultdict, OrderedDict

class Elevator(threading.Thread):
    def __init__(self):
        super().__init__(name="elevator")
        self.toTransport = []
        self.waiting_list = defaultdict(list)
        self.waiting_num = 0
        self.passenger_num = 0
        self.active = False
        self.fromFloor = 0
        self.toFloor = 0

    def take_passenger(self, atFloor):
        time.sleep(0.1)
        self.toFloor = atFloor
        self.passenger_num += len(self.waiting_list[atFloor])
        self.waiting_num -= len(self.waiting_list[atFloor])
        print("Elevator move from {} to {} ({} peoples in elevator)".format(self.fromFloor, self.toFloor, self.passenger_num))
        print("{} people enter elevator".format(len(self.waiting_list[atFloor])))   
        self.toTransport += self.waiting_list[atFloor]
        self.waiting_list[atFloor] = []
        print('toTransport: ', self.toTransport)
        
    def transport(self):
        time.sleep(0.1)
        self.fromFloor = self.toFloor
        self.toFloor = self.toTransport.pop() #  need to implement a exiting prioirtiy to choose which floor the elevator should go to
        self.passenger_num -= 1 # reduce the same desitnation people num
        print("Elevator move from {} to {} ({} peoples in elevator)".format(self.fromFloor, self.toFloor, self.passenger_num))
        print("{} people exits".format('xxx'))
        self.fromFloor = self.toFloor
        if self.waiting_list[self.fromFloor] != []:
            self.waiting_num -= len(self.waiting_list[self.fromFloor])
            self.passenger_num += len(self.waiting_list[self.fromFloor])
            print("{} people enter elevator".format(len(self.waiting_list[self.fromFloor])))   
            self.toTransport += self.waiting_list[self.fromFloor]
            self.waiting_list[self.fromFloor] = []
            print('toTransport: ', self.toTransport)
        if len(self.toTransport) == 0:
            print("DEACTIVE")
            self.active = False

    def set_new_passenger(self, atFloor, toFloor):
        if atFloor == toFloor:
            return
        self.waiting_list[atFloor].append(toFloor)
        self.waiting_num += 1
        print('waiting_list:', self.waiting_list)

    def get_passenger_from_waiting(self):
        if self.active == False:
            print("ACTIVE")
            self.active = True
            # print(self.waiting_list.items())
            # print(sorted(self.waiting_list.items(), key= lambda t: len(t[1])))
            # print(sorted(self.waiting_list.items(), key= lambda t: len(t[1])).pop()[0])
            floor = sorted(self.waiting_list.items(), key= lambda t: len(t[1])).pop()[0]
            # need to implement a waiting prioirtiy to choose which floor the elevator should go to
            # now we take the floor the most people waiting
            self.take_passenger(floor)

    def run(self):
        while True:
            if len(self.toTransport) != 0:
                self.transport()
            elif len(self.toTransport) == 0 and self.waiting_num != 0:
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
        time.sleep(0.05)