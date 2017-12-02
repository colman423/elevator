import os
import pygame
import time
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
def elevatorMoveTo(elevator,floor):
    if elevator.rect.center[1]-5 > maxFloor*eachFloorSize-floor*eachFloorSize:
        elevator.velocity.y = -4
        if elevator.rect.center[1] <= maxFloor*eachFloorSize-floor*eachFloorSize:
            elevator.currentFloor = floor
            elevator.velocity.y = 0
    elif elevator.rect.center[1]-5 < maxFloor*eachFloorSize-floor*eachFloorSize:
        elevator.velocity.y = 4
        if elevator.rect.center[1] >= maxFloor*eachFloorSize-floor*eachFloorSize:
            elevator.currentFloor = floor
            elevator.velocity.y = 0
    else:
        elevator.velocity.y = 0
    return 0

def create_person():  # create a person ui
    
    images = load_images()  # Make sure to provide the relative or full path to the images directory.
    player = AnimatedSprite(position=(100, 10+(len(playerX))%maxFloor*eachFloorSize), images=images)
    playerX.append(player)
    player.velocity.x = 1
    return 0


def person_entering(person):  # let waiting person walk into elevator
    
    person.velocity.x = 1
    if person.rect.center[0] > elevatorPosition:
        person.velocity.x = 0
        person.InTheElevator = True
        return True
    return False

def person_leaving(person):  # let arrived person leave the window
    person.velocity.x = -1
    person.velocity.y = 0
    person.InTheElevator = False
    return True


class AnimatedSprite(pygame.sprite.Sprite):
    
    def __init__(self, position, images):
        """
        Animated sprite object.

        Args:
            position: x, y coordinate on the screen to place the AnimatedSprite.
            images: Images to use in the animation.
        """
        super(AnimatedSprite, self).__init__()
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

#    def update_frame_dependent(self):
#        """
#        Updates the image of Sprite every 6 frame (approximately every 0.1 second if frame rate is 60).
#        """
#        if self.velocity.x > 0:  # Use the right images if sprite is moving right.
#            self.images = self.images_right
#        elif self.velocity.x < 0:
#            self.images = self.images_left
#
#        self.current_frame += 1
#        if self.current_frame >= self.animation_frames:
#            self.current_frame = 0
#            self.index = (self.index + 1) % len(self.images)
#            self.image = self.images[self.index]
#
#        self.rect.move_ip(*self.velocity)

    def update(self, dt):
        """This is the method that's being called when 'all_sprites.update(dt)' is called."""
        # Switch between the two update methods by commenting/uncommenting.
        self.update_time_dependent(dt)
        # self.update_frame_dependent()


def main():
    ElevatorImages.append(pygame.image.load("elevator.png"))
    Elevator = AnimatedSprite(position=(500, eachFloorSize*(maxFloor-1)), images=ElevatorImages)
    create_person()
    create_person()
    create_person()
    create_person()
    create_person()
    create_person()
    count = 0
    
    running = True
    while running:
        
        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop.
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        create_person()
#                    if event.key == pygame.K_UP:
#                        Elevator.velocity.y = -3
#                    if event.key == pygame.K_DOWN:
#                        Elevator.velocity.y = 3
#                if event.type == pygame.KEYUP:
#                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
#                        Elevator.velocity.y = 0
        if count < len(playerX):
            if playerX[count].rect.center[0] > stopPosition:
                playerX[count].velocity.x = 0
                count += 1
        #for test
        elevatorMoveTo(Elevator,10)
        if len(peopleInElevator) == 0:
            
            if person_entering(playerX[0]):
                peopleInElevator.append(playerX[0])
        if playerX[0].InTheElevator and Elevator.currentFloor == 10:
            elevatorMoveTo(Elevator,1)
            peopleInElevator[0].velocity.y = Elevator.velocity.y
        if Elevator.currentFloor == 1:
            person_leaving(playerX[0])
        ######################

        all_sprites = pygame.sprite.Group(playerX) # Creates a sprite group and adds 'player' to it.
        all_sprites.update(dt)  # Calls the 'update' method on all sprites in the list (currently just the player).
        elevator_sprites = pygame.sprite.Group(Elevator)
        elevator_sprites.update(dt)
        
        screen.fill(BACKGROUND_COLOR)
        all_sprites.draw(screen)
        elevator_sprites.draw(screen)
        pygame.display.update()



if __name__ == '__main__':
    main()

