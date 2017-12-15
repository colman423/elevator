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
        self.lock = threading.Lock()
        self.lock.acquire()

    def transport_passenger_when_moving(self):
        if self.fromFloor > self.toFloor:
            for i in range(self.fromFloor, self.toFloor, -1):
                self.lock.release()
                self.lock.acquire()                
                print('Elevator arrive at {}'.format(i))
                if self.waiting_list[i] != []:
                    self.toTransport += self.waiting_list[i]
                    self.passenger_num += len(self.waiting_list[i])
                    self.waiting_num -= len(self.waiting_list[i])
                    print("{} people enter elevator".format(len(self.waiting_list[i])))   
                    print('In elevator(to transport): ', self.toTransport)
                    self.waiting_list[i] = []
                leave_num = len([desitnation for desitnation in self.toTransport if desitnation == i])
                if leave_num:
                    self.passenger_num -= leave_num # reduce the same desitnation people num
                    self.toTransport = [desitnation for desitnation in self.toTransport if desitnation != i]
                    print("{} people exits".format(leave_num))
                    print('In elevator(to transport): ', self.toTransport)
        elif self.fromFloor < self.toFloor:
            for i in range(self.fromFloor, self.toFloor):
                self.lock.release()
                self.lock.acquire()     
                print('Elevator arrive at {}'.format(i))
                if self.waiting_list[i] != []:
                    self.toTransport += self.waiting_list[i]
                    self.passenger_num += len(self.waiting_list[i])
                    self.waiting_num -= len(self.waiting_list[i])
                    print("{} people enter elevator".format(len(self.waiting_list[i])))   
                    print('In elevator(to transport): ', self.toTransport)
                    self.waiting_list[i] = []
                leave_num = len([desitnation for desitnation in self.toTransport if desitnation == i]) 
                if leave_num:
                    self.passenger_num -= leave_num # reduce the same desitnation people num
                    self.toTransport = [desitnation for desitnation in self.toTransport if desitnation != i]
                    print("{} people exits".format(leave_num))
                    print('In elevator(to transport): ', self.toTransport)

    def take_passenger(self, atFloor):
        self.toFloor = atFloor
        time.sleep(0.1) # moving time
        print("Elevator move from {} to {}...".format(self.fromFloor, self.toFloor))

        self.transport_passenger_when_moving()
        self.lock.release()
        self.lock.acquire()     
        print('Elevator arrive at {}'.format(self.toFloor))
        self.passenger_num += len(self.waiting_list[atFloor])
        self.waiting_num -= len(self.waiting_list[atFloor])
        print("{} people enter elevator".format(len(self.waiting_list[atFloor])))   

        self.toTransport += self.waiting_list[atFloor]
        self.waiting_list[atFloor] = []
        print("{} people in the elevator".format(self.passenger_num))
        print('In elevator(to transport): ', self.toTransport)
        
    def transport(self):
        self.fromFloor = self.toFloor
        floor = sorted(self.toTransport, key= lambda t: self.toTransport.count(t)).pop()
        self.toFloor = floor 
        # need to implement a exiting prioirtiy to choose which floor the elevator should go to
        # now we take the floor the most people are going to
        time.sleep(0.1)
        print("Elevator move from {} to {}...".format(self.fromFloor, self.toFloor))

        self.transport_passenger_when_moving()
        self.lock.release()
        self.lock.acquire()            
        print('Elevator arrive at {}'.format(self.toFloor))
        leave_num = len([desitnation for desitnation in self.toTransport if desitnation == self.toFloor])
        self.passenger_num -= leave_num # reduce the same desitnation people num
        self.toTransport = [desitnation for desitnation in self.toTransport if desitnation != self.toFloor]
        print("{} people exits".format(leave_num))
        print('In elevator(to transport): ', self.toTransport)
        self.fromFloor = self.toFloor

        if self.waiting_list[self.fromFloor] != []:
            self.waiting_num -= len(self.waiting_list[self.fromFloor])
            self.passenger_num += len(self.waiting_list[self.fromFloor])
            print("{} people enter elevator".format(len(self.waiting_list[self.fromFloor])))   
            self.toTransport += self.waiting_list[self.fromFloor]
            self.waiting_list[self.fromFloor] = []
            print('In elevator(to transport): ', self.toTransport)
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
        time.sleep(0.001)