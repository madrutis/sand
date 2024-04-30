# Example file showing a circle moving on screen
import pygame
import numpy as np

# pygame setup
pygame.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
running = True
dt = 0

spacing = 20
radius = 3
num_rows = screen.get_height() // spacing
num_cols = screen.get_width() // spacing
color = 0
# grid = np.random.choice([1, 0],(num_rows, num_cols), p=[0.4, 0.6])
grid = np.zeros((num_rows, num_cols))


def draw_grid():
    cols = screen.get_width()
    rows = screen.get_height()
    for i in range(0, cols, spacing):
        pygame.draw.line(screen, "white", (i, 0), (i, rows))
    for i in range(0, rows, spacing):
        pygame.draw.line(screen, "white", (0, i), (cols, i))

def draw_rectangles(grid):
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] != 0:
                color = pygame.Color(0, 0, 0)
                color.hsva = (grid[i, j], 100, 100, 100)
                pygame.draw.rect(screen, color, (j * spacing, i * spacing, spacing, spacing))

def handle_click():
    global radius, color
    pos = pygame.mouse.get_pos()
    yloc = pos[1] // spacing
    xloc = pos[0] // spacing
    color = (color + 1) % 360
    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            if x**2 + y**2 <= radius**2:
                grid[yloc + y, xloc + x] = color

def update_grid(grid):
    new_grid = np.zeros((screen.get_height() // spacing, screen.get_width() // spacing))
    new_grid[num_rows - 1, :] = grid[num_rows - 1, :]
    for row in range(num_rows - 1):
        for col in range(num_cols):
            # check to see if there is sand below
            direction = np.random.choice([-1, 1])
            if grid[row, col] != 0:
                new_grid[row, col] = 0
                if grid[row + 1, col] == 0:
                    new_grid[row + 1, col] = grid[row, col]
                elif grid[row + 1, (col + direction) % num_cols] == 0:
                    new_grid[row + 1, (col + direction) % num_cols] = grid[row, col]
                elif grid[row + 1, (col - direction) % num_cols] == 0:
                    new_grid[row + 1, (col - direction) % num_cols] = grid[row, col]
                else:
                    new_grid[row, col] = grid[row, col]
                

    return new_grid


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_click()
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:  # Left mouse button is pressed
        handle_click()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    draw_grid()
    grid = update_grid(grid)
    draw_rectangles(grid)



    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()



