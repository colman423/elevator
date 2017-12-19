import os
import pygame
import time
import STATE
class AnimatedSprite(pygame.sprite.Sprite):
    
    def __init__(self, position, images, floor):
        """
            Animated sprite object.
            
            Args:
            position: x, y coordinate on the screen to place the AnimatedSprite.
            images: Images to use in the animation.
            """
        super(AnimatedSprite, self).__init__()
        
        
        
        self.state = STATE.CREATION
        self.floor = floor
        self.isMoving = True
        self.currentFloor = 0
        self.InTheElevator = False
        size = (16, 16)  # This should match the size of the images.
        posirionX = position[0]
        positionY = position[1]
        self.rect = pygame.Rect(position, size)
        self.images = images
        self.images_right = images
        self.images_left = [pygame.transform.flip(image, True, False) for image in images]  # Flipping every image.
        self.index = 0
        self.image = images[self.index]  # 'image' is the current image of the animation.
        
        self.velocity = pygame.math.Vector2(0, 0)
        
        self.animation_time = 0.3
        self.current_time = 0
        
        self.animation_frames = 6
        self.current_frame = 0
    
    
    def update_time_dependent(self, dt):
        """
            Updates the image of Sprite approximately every 0.3 second.
            
            Args:
            dt: Time elapsed between each frame.
            """
        if self.velocity.x > 0:  # Use the right images if sprite is moving right.
            self.images = self.images_right
        elif self.velocity.x < 0:
            self.images = self.images_left
        
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
        
        self.rect.move_ip(*self.velocity)
    
    def update(self, dt):
        """This is the method that's being called when 'all_sprites.update(dt)' is called."""
        self.update_time_dependent(dt)



class ElevatorMove(object):  # represents the bird, not the game
    def __init__(self):
        """ The constructor of the class """
        self.image = pygame.image.load("elevator.png")
        # the bird's position
        self.x = 500
        self.y = 0
    def ElevatorMoveToFloor(floor):
        self.y = (720-15)-floor*70
    

    def draw(self, surface):
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))



pygame.init()

SIZE = WIDTH, HEIGHT = 720, 720
BACKGROUND_COLOR = pygame.Color('white')
FPS = 30
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
playerX = []
ElevatorImages = []
stopPosition = 450
elevatorPosition = stopPosition + 70
maxFloor = 10
eachFloorSize = 70
peopleInElevator = []
NumberOfPersonOnFloor = [0 for x in range(maxFloor+1)]
elevatorVelocity = 30
elevatorFloor = 0

#create elevator
ElevatorImages.append(pygame.image.load("elevator.png"))
Elevator = AnimatedSprite(position=(500, eachFloorSize*(maxFloor-1)), images=ElevatorImages, floor = 1)
Elevator.font = pygame.font.SysFont("Arial", 12)


elevator1 = ElevatorMove()


def load_images():
    """
    Loads all images in directory. The directory must only contain images.

    Args:
        path: The relative or absolute path to the directory to load images from.

    Returns:
        List of images.
    """
    images = []
    
    images.append(pygame.image.load("walk1.png"))
    images.append(pygame.image.load("walk2.png"))
    return images

def quit_program():
    os._exit(1)

# ----- functions for thread -----
def elevatorStop():
    Elevator.velocity.y = 0
    return 0
def elevatorMoveTo(floor):

    elevator1.y = (720-30)-floor*70

#    if Elevator.rect.center[1]-15 > 720 or Elevator.rect.center[1]-15 < 0:
#        Elevator.rect.center[1] = 0
#    elevatorFloor = floor
#    Elevator.textsurf = Elevator.font.render(str(elevatorFloor), 1, pygame.Color('red'))
#    Elevator.images[0].blit(Elevator.textsurf, [10, -3])
#    print("elevator at {} floor at  {}".format(Elevator.rect.center[1],(maxFloor-floor)*eachFloorSize))
#    if Elevator.rect.center[1]-15 > (maxFloor-floor)*eachFloorSize:
#        Elevator.velocity.y = -elevatorVelocity
#        if Elevator.rect.center[1] <= (maxFloor-floor)*eachFloorSize:
#            Elevator.currentFloor = floor
#            elevatorStop()
#            return True
#    elif Elevator.rect.center[1]-15 < (maxFloor-floor)*eachFloorSize:
#        Elevator.velocity.y = elevatorVelocity
#        if Elevator.rect.center[1] >= (maxFloor-floor)*eachFloorSize:
#            Elevator.currentFloor = floor
#            elevatorStop()
#            return True
#    else:
#        Elevator.velocity.y = 0
#    return False

def create_person(floor):  # create a person ui
    
    NumberOfPersonOnFloor[floor] += 1 #count the number of person in each floor
    images = load_images()  # Make sure to provide the relative or full path to the images directory.
    player = AnimatedSprite(position=(100, HEIGHT-(10+floor*eachFloorSize)), images=images, floor = floor)
    
    #add font on person's head
    player.font = pygame.font.SysFont("Arial", 12)
    player.textsurf = player.font.render("test", 1, pygame.Color('red'))
    player.images[0].blit(player.textsurf, [10, -3])
    player.images[1].blit(player.textsurf, [10, -3])
    playerX.append(player)
    player.velocity.x = 1
    return player


def person_entering(person):  # let waiting person walk into elevator
    person.velocity.x = 1
    if person.rect.center[0] > elevatorPosition:
        person.velocity.x = 0
        person.InTheElevator = True
        person.state = STATE.TRANSPORTING
        NumberOfPersonOnFloor[person.floor] -= 1
        return True
    return False

def person_leaving(person):  # let arrived person leave the window
    person.state = STATE.LEAVING
    person.velocity.x = -1
    person.velocity.y = 0
    person.InTheElevator = False
    return True

# -----end thread function-----

# -----start utility function-----
def floorToScreenHeight(floor):
    return HEIGHT-floor*48

# -----end utility function -----

def main():
    
#    #for test
#    create_person(10)
#    create_person(9)
#    create_person(8)
#    create_person(7)
#    create_person(6)
#    create_person(5)
#    create_person(4)
#    create_person(3)
#    create_person(2)
#    create_person(1)
    count = 0
    
    
    
    running = True
    while running:
        
        FloorText=pygame.font.SysFont("comicsansms",30)
        for i in range(1,maxFloor+1):
            text1=FloorText.render("{}F".format(i),True,(30,255,30))
            pygame.draw.line(screen,pygame.Color('black'),(0,HEIGHT-28-eachFloorSize*i),(500,HEIGHT-28-eachFloorSize*i),3)
            screen.blit(text1,(50,HEIGHT-15-eachFloorSize*i))
        pygame.draw.line(screen,pygame.Color('black'),(0,697),(500,697),3)
        pygame.draw.line(screen,pygame.Color('black'),(465,0),(465,1000),3)
        
        elevator1.draw(screen)
        
        pygame.display.flip()

        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop.
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit_program()
            else:
                #for test
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        create_person(10)
                    if event.key == pygame.K_z:
                        create_person(9)
#                    if event.key == pygame.K_UP:
#                        Elevator.velocity.y = -3
#                    if event.key == pygame.K_DOWN:
#                        Elevator.velocity.y = 3
#                if event.type == pygame.KEYUP:
#                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
#                        Elevator.velocity.y = 0
        #calculate the person stop point
        
        if count < len(playerX):
            if playerX[count].rect.center[0] > stopPosition - NumberOfPersonOnFloor[playerX[count].floor]*20:
                playerX[count].velocity.x = 0
                playerX[count].state = STATE.WAITING
                count += 1
#        #for test

#        if len(peopleInElevator) == 0:
#            if person_entering(playerX[0]):
#                peopleInElevator.append(playerX[0])
#        if playerX[0].InTheElevator and Elevator.currentFloor == 10:
#            elevatorMoveTo(1)
#            peopleInElevator[0].velocity.y = Elevator.velocity.y
#        if Elevator.currentFloor == 1:
#            person_leaving(playerX[0])
#        ######################

        #draw all sprites
        all_sprites = pygame.sprite.Group(playerX) # Creates a sprite group and adds 'player' to it.
        all_sprites.update(dt)  # Calls the 'update' method on all sprites in the list (currently just the player).
#        elevator_sprites = pygame.sprite.Group(Elevator)
#        elevator_sprites.update(dt)

        screen.fill(BACKGROUND_COLOR)
        all_sprites.draw(screen)
#        elevator_sprites.draw(screen)
        pygame.display.update()




if __name__ == '__main__':
    main()

