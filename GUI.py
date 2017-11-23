import os
import pygame
import time
pygame.init()

SIZE = WIDTH, HEIGHT = 720, 480
BACKGROUND_COLOR = pygame.Color('white')
FPS = 5

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
playerX = []

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

def create_person():  # create a person ui
    
    images = load_images()  # Make sure to provide the relative or full path to the images directory.
    player = AnimatedSprite(position=(100, 100+len(playerX)*100), images=images)
    playerX.append(player)
    
    return 0


def person_entering(person):  # let waiting person walk into elevator
    # todo
    return True


def person_leaving(person):  # let arrived person leave the window
    # todo
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

        size = (32, 32)  # This should match the size of the images.

        self.rect = pygame.Rect(position, size)
        self.images = images
        self.images_right = images
        self.images_left = [pygame.transform.flip(image, True, False) for image in images]  # Flipping every image.
        self.index = 0
        self.image = images[self.index]  # 'image' is the current image of the animation.

        self.velocity = pygame.math.Vector2(0, 0)

        self.animation_time = 0.1
        self.current_time = 0

        self.animation_frames = 6
        self.current_frame = 0

    def update_time_dependent(self, dt):
        """
        Updates the image of Sprite approximately every 0.1 second.

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

    def update_frame_dependent(self):
        """
        Updates the image of Sprite every 6 frame (approximately every 0.1 second if frame rate is 60).
        """
        if self.velocity.x > 0:  # Use the right images if sprite is moving right.
            self.images = self.images_right
        elif self.velocity.x < 0:
            self.images = self.images_left

        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

        self.rect.move_ip(*self.velocity)

    def update(self, dt):
        """This is the method that's being called when 'all_sprites.update(dt)' is called."""
        # Switch between the two update methods by commenting/uncommenting.
        self.update_time_dependent(dt)
        # self.update_frame_dependent()


def main():
    create_person()
    all_sprites = pygame.sprite.Group(playerX)  # Creates a sprite group and adds 'player' to it.
    
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
                        all_sprites = pygame.sprite.Group(playerX)
                for i in range(0,len(playerX)):
                    playerX[i].velocity.x = 5
    
        all_sprites.update(dt)  # Calls the 'update' method on all sprites in the list (currently just the player).
        
        screen.fill(BACKGROUND_COLOR)
        all_sprites.draw(screen)
        pygame.display.update()
#time.sleep(5)
#create_person()
#    images = load_images()  # Make sure to provide the relative or full path to the images directory.
#    player = AnimatedSprite(position=(100, 100), images=images)
#    all_sprites = pygame.sprite.Group(player)  # Creates a sprite group and adds 'player' to it.
#
#    running = True
#    while running:
#
#        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop.
#
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                running = False
#            else:
#                player.velocity.x = 4
#
#        all_sprites.update(dt)  # Calls the 'update' method on all sprites in the list (currently just the player).
#
#        screen.fill(BACKGROUND_COLOR)
#        all_sprites.draw(screen)
#        pygame.display.update()


if __name__ == '__main__':
    main()

