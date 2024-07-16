import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 128)
WALL_COLOR = (0, 0, 255)
PACMAN_COLOR = (255, 255, 0)
PELLET_COLOR = (255, 255, 255)
POWER_PELLET_COLOR = (255, 165, 0)
GHOST_COLOR = (255, 0, 0)
CELL_SIZE = 20
PACMAN_RADIUS = CELL_SIZE // 2
PACMAN_SPEED = 3
GHOST_SPEED = 2

def load_maze(filename):
    maze = []
    pellets = []
    power_pellets = []
    with open(filename, 'r') as f:
        for y, line in enumerate(f):
            row = list(line.strip())
            maze.append(row)
            for x, char in enumerate(row):
                if char == '.':
                    pellets.append((x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2))
                elif char == 'o':
                    power_pellets.append((x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2))
    return maze, pellets, power_pellets

maze, pellets, power_pellets = load_maze('maze.txt')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

def draw_maze(screen, maze):
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            if char == '#':
                pygame.draw.rect(screen, WALL_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_pellets(screen, pellets, color=PELLET_COLOR):
    for pellet in pellets:
        pygame.draw.circle(screen, color, pellet, 2)

def draw_pacman(screen, x, y):
    pygame.draw.circle(screen, PACMAN_COLOR, (x, y), PACMAN_RADIUS)

    mouth_rect = pygame.Rect(x - PACMAN_RADIUS, y - PACMAN_RADIUS, PACMAN_RADIUS * 2, PACMAN_RADIUS * 2)
    if mouth_open:
        pygame.draw.arc(screen, BACKGROUND_COLOR, mouth_rect, mouth_start_angle, mouth_end_angle, 0)

def draw_ghosts(screen, ghosts):
    for ghost in ghosts:
        pygame.draw.circle(screen, GHOST_COLOR, (ghost['x'], ghost['y']), PACMAN_RADIUS)

pacman_x = CELL_SIZE * 1.5
pacman_y = CELL_SIZE * 1.5
movement_x = 0
movement_y = 0

mouth_open = False
mouth_animation_speed = 0.1
mouth_start_angle = 0
mouth_end_angle = 0

score = 0

ghosts = [
    {'x': SCREEN_WIDTH - CELL_SIZE * 2.5, 'y': SCREEN_HEIGHT - CELL_SIZE * 2.5, 'dx': -1, 'dy': 0, 'state': 'chase'},
    {'x': SCREEN_WIDTH - CELL_SIZE * 2.5, 'y': CELL_SIZE * 2.5, 'dx': 1, 'dy': 0, 'state': 'scatter'}
]

ghost_scatter_time = 0
scatter_duration = 5000
ghosts_scattered = False

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    pacman_x += movement_x
    pacman_y += movement_y

    cell_x = int(pacman_x / CELL_SIZE)
    cell_y = int(pacman_y / CELL_SIZE)
    if maze[cell_y][cell_x] == '#':
        pacman_x -= movement_x
        pacman_y -= movement_y

    elif maze[cell_y][cell_x] == '.':
        maze[cell_y][cell_x] = ' '
        score += 10

    elif maze[cell_y][cell_x] == 'o':
        maze[cell_y][cell_x] = ' '
        score += 50

        for ghost in ghosts:
            ghost['state'] = 'frightened'
        ghost_scatter_time = pygame.time.get_ticks()
        ghosts_scattered = True

    screen.fill(BACKGROUND_COLOR)

    draw_maze(screen, maze)

    draw_pellets(screen, pellets, PELLET_COLOR)
    draw_pellets(screen, power_pellets, POWER_PELLET_COLOR)

    draw_pacman(screen, int(pacman_x), int(pacman_y))

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

    for ghost in ghosts:
        if ghost['state'] == 'chase':

            if pacman_x < ghost['x']:
                ghost['dx'] = -GHOST_SPEED
            elif pacman_x > ghost['x']:
                ghost['dx'] = GHOST_SPEED
            if pacman_y < ghost['y']:
                ghost['dy'] = -GHOST_SPEED
            elif pacman_y > ghost['y']:
                ghost['dy'] = GHOST_SPEED
        elif ghost['state'] == 'scatter':

            if random.randint(0, 1) == 0:
                ghost['dx'] = -GHOST_SPEED if random.randint(0, 1) == 0 else GHOST_SPEED
                ghost['dy'] = 0
            else:
                ghost['dx'] = 0
                ghost['dy'] = -GHOST_SPEED if random.randint(0, 1) == 0 else GHOST_SPEED
        elif ghost['state'] == 'frightened':

            if pacman_x < ghost['x']:
                ghost['dx'] = GHOST_SPEED
            elif pacman_x > ghost['x']:
                ghost['dx'] = -GHOST_SPEED
            if pacman_y < ghost['y']:
                ghost['dy'] = GHOST_SPEED
            elif pacman_y > ghost['y']:
                ghost['dy'] = -GHOST_SPEED

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    for ghost in ghosts:
        ghost['x'] += ghost['dx']
        ghost['y'] += ghost['dy']

    if ghosts_scattered:
        current_time = pygame.time.get_ticks()
        if current_time - ghost_scatter_time >= scatter_duration:
            ghosts_scattered = False

    draw_ghosts(screen, ghosts)

    pygame.display.flip()

pygame.quit()
sys.exit()