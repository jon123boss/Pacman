import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
BACKGROUND_COLOR = (0, 0, 128)  # Dark Blue
WALL_COLOR = (0, 0, 255)  # Blue
PACMAN_COLOR = (255, 255, 0)  # Yellow
CELL_SIZE = 20
PACMAN_RADIUS = CELL_SIZE // 2
PACMAN_SPEED = 3

# Load the maze from file
def load_maze(filename):
    maze = []
    with open(filename, 'r') as f:
        for line in f:
            row = list(line.strip())
            maze.append(row)
    return maze

maze = load_maze('maze.txt')

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

# Function to draw the maze
def draw_maze(screen, maze):
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == '#':
                pygame.draw.rect(screen, WALL_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Function to draw Pac-Man
def draw_pacman(screen, x, y):
    pygame.draw.circle(screen, PACMAN_COLOR, (x, y), PACMAN_RADIUS)
    # Draw mouth
    mouth_rect = pygame.Rect(x - PACMAN_RADIUS, y - PACMAN_RADIUS, PACMAN_RADIUS * 2, PACMAN_RADIUS * 2)
    if mouth_open:
        pygame.draw.arc(screen, BACKGROUND_COLOR, mouth_rect, mouth_start_angle, mouth_end_angle, 0)

# Initial Pac-Man position
pacman_x = CELL_SIZE * 1.5
pacman_y = CELL_SIZE * 1.5

# Pac-Man movement variables
movement_x = 0
movement_y = 0
mouth_open = False
mouth_animation_speed = 0.1
mouth_start_angle = 0
mouth_end_angle = 0

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        movement_x = -PACMAN_SPEED
        movement_y = 0
    elif keys[pygame.K_RIGHT]:
        movement_x = PACMAN_SPEED
        movement_y = 0
    elif keys[pygame.K_UP]:
        movement_x = 0
        movement_y = -PACMAN_SPEED
    elif keys[pygame.K_DOWN]:
        movement_x = 0
        movement_y = PACMAN_SPEED

    # Check collision with walls
    next_x = pacman_x + movement_x
    next_y = pacman_y + movement_y
    cell_x = int(next_x / CELL_SIZE)
    cell_y = int(next_y / CELL_SIZE)
    if maze[cell_y][cell_x] != '#':
        pacman_x = next_x
        pacman_y = next_y

    # Fill the background
    screen.fill(BACKGROUND_COLOR)

    # Draw the maze
    draw_maze(screen, maze)

    # Draw Pac-Man
    draw_pacman(screen, int(pacman_x), int(pacman_y))

    # Update mouth animation
    if mouth_open:
        mouth_end_angle += mouth_animation_speed
        if mouth_end_angle > 2.0:
            mouth_end_angle = 2.0
    else:
        mouth_start_angle += mouth_animation_speed
        if mouth_start_angle > 2.0:
            mouth_start_angle = 2.0

    if mouth_start_angle >= 1.0:
        mouth_open = True
    if mouth_start_angle >= 2.0:
        mouth_open = False
        mouth_start_angle = 0
        mouth_end_angle = 0

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
