import pygame

# Use 2D vectors
vector = pygame.math.Vector2

# Initialize pygame
pygame.init()

# Set display surface to something divisible by tile size (32x32). Our surface is 30 tiles wide by 20 tiles high
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Making a tile map!")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()


# Define Classes
class Tile(pygame.sprite.Sprite):
    """A class to read and create individual tiles and place them in the display"""

    def __init__(self, x, y, tile_type, main_group, sub_group=""):
        super().__init__()
        # Load in the correct image and add it to the correct sub group
        if tile_type == 1:
            self.image = pygame.image.load("dirt.png")
        elif tile_type == 2:
            self.image = pygame.image.load("grass.png")
            sub_group.add(self)
        elif tile_type == 3:
            self.image = pygame.image.load("water.png")
            sub_group.add(self)

        # Add every tile to the main tile group
        main_group.add(self)

        # Get rect of the image and position it in the grid
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Player(pygame.sprite.Sprite):
    """A Player class the user can control"""

    def __init__(self, x, y, grass_tiles, water_tiles):
        super().__init__()
        self.image = pygame.image.load("knight.png")
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        self.starting_x = x
        self.starting_y = y
        self.grass_tiles = grass_tiles
        self.water_tiles = water_tiles

        # Kinematics vectors (first value is x, second value is y)
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

        # Kinematic constants
        self.HORIZONTAL_ACCELERATION = 2
        self.HORIZONTAL_FRICTION = 0.15
        self.VERTICAL_ACCELERATION = 0.5  # Gravity
        self.VERTICAL_JUMP_SPEED = 15  # Determines how high we can jump

    def update(self):
        self.move()
        self.check_collisions()

    def move(self):
        # Set the acceleration vector to (0,0) so there is initially no acceleration
        # If there are no key presses then horizontal acceleration should be 0, gravity will always be present
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        # If the user is pressing a left or right key, set the x-component of the acceleration vector to a non-zero value
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
        if keys[pygame.K_RIGHT]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION

        # Calculate new kinematics values
        self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + .5 * self.acceleration

        # Update rect based on kinematics calculations and add wrap around motion
        if self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = 0
        self.rect.bottomleft = self.position

    def check_collisions(self):
        # Check for collisions with grass tiles
        collided_platforms = pygame.sprite.spritecollide(self, self.grass_tiles, False)
        if collided_platforms:
            # Only move to the platform if the player is falling down
            if self.velocity.y > 0:
                self.position.y = collided_platforms[0].rect.top + 1
                self.velocity.y = 0

        # Check for collisions with water tiles
        if pygame.sprite.spritecollide(self, self.water_tiles, False):
            self.position = (self.starting_x, self.starting_y)
            self.velocity = vector(0, 0)

    def jump(self):
        # Only jump if on a grass tile
        if pygame.sprite.spritecollide(self, self.grass_tiles, False):
            self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED


# Create sprite groups
main_tile_group = pygame.sprite.Group()
grass_tile_group = pygame.sprite.Group()
water_tile_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

# Create the tile map: 0 -> no tile, 1 -> dirt, 2 -> grass, 3 -> water, 4 -> player
# 20 rows and 30 columns
tile_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1],
]

# Create individual tile objects from the tile map
# Loop through the 20 lists in the tile map (i moves us down the map)
for i in range(len(tile_map)):
    # Loop through the 30 elements in a given list (j moves us across the map)
    for j in range(len(tile_map[i])):
        if tile_map[i][j] == 1:
            Tile(j * 32, i * 32, 1, main_tile_group)
        elif tile_map[i][j] == 2:
            Tile(j * 32, i * 32, 2, main_tile_group, grass_tile_group)
        elif tile_map[i][j] == 3:
            Tile(j * 32, i * 32, 3, main_tile_group, water_tile_group)
        elif tile_map[i][j] == 4:
            player = Player(j * 32, i * 32 + 32, grass_tile_group, water_tile_group)
            player_group.add(player)

# Load in a background image
background_image = pygame.image.load("background.png")
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

# The main game loop
running = True
while running:
    # Check to see if the user has quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # Blit the background
    display_surface.blit(background_image, background_rect)

    # Draw tiles
    main_tile_group.draw(display_surface)

    # Update and draw sprites
    player_group.update()
    player_group.draw(display_surface)

    # Update the display and tick the clock
    pygame.display.update()
    clock.tick(FPS)

# End the game
pygame.quit()
