import threading
import time
from collections import defaultdict

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
        self.toFloor = atFloor
        time.sleep(0.1) # moving time
        print("Elevator move from {} to {}".format(self.fromFloor, self.toFloor))

        self.passenger_num += len(self.waiting_list[atFloor])
        self.waiting_num -= len(self.waiting_list[atFloor])
        print("{} people enter elevator".format(len(self.waiting_list[atFloor])))   

        self.toTransport += self.waiting_list[atFloor]
        self.waiting_list[atFloor] = []
        print("{} people in the elevator".format(self.passenger_num))
        print('toTransport: ', self.toTransport)
        
    def transport(self):
        self.fromFloor = self.toFloor
        self.toFloor = self.toTransport.pop() #  need to implement a exiting prioirtiy to choose which floor the elevator should go to
        time.sleep(0.1)
        print("Elevator move from {} to {}".format(self.fromFloor, self.toFloor))
        
        leave_num = len([desitnation for desitnation in self.toTransport if desitnation == self.toFloor]) + 1 # the pop one
        self.passenger_num -= leave_num # reduce the same desitnation people num
        self.toTransport = [desitnation for desitnation in self.toTransport if desitnation != self.toFloor]
        print("{} people exits".format(leave_num))
        print('toTransport: ', self.toTransport)
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
    while True:
        atFloor, toFloor = random.randrange(0, 10), random.randrange(0, 10)
        print()
        print('passenger:', atFloor, toFloor)
        newPassenger = threading.Thread(target=elevator.set_new_passenger, args=(atFloor, toFloor, ))
        newPassenger.start()
        time.sleep(0.05)