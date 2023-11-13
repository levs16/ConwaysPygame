# Imports
import pygame
import sys

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
CELL_SIZE = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Init screen
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Conway\'s Game of Life')
clock = pygame.time.Clock()

# Create grid function
def create_grid():
    rows = SCREEN_HEIGHT // CELL_SIZE
    cols = SCREEN_WIDTH // CELL_SIZE
    grid = []

    for i in range(rows):
        grid.append([])
        for j in range(cols):
            grid[i].append(0)

    return grid

# Draw grid function
def draw_grid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            x = j * CELL_SIZE
            y = i * CELL_SIZE

            # Draw a rectangle for the cell
            if grid[i][j] == 0:
                # If the cell is dead, fill it with black
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))
            else:
                # If the cell is alive, fill it with white
                pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))

            # Draw a gray border around the cell
            pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)

    # Draw a gray border around the grid
    pygame.draw.rect(screen, GRAY, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 1)

# Define a function to update the grid according to the rules of the game
def update_grid(grid):
    # Create a copy of the grid to store the new state
    new_grid = create_grid()

    # Loop through the rows and columns of the grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            # Get the number of alive neighbors of the cell
            neighbors = 0
            for k in range(-1, 2):
                for l in range(-1, 2):
                    # Skip the cell itself
                    if k == 0 and l == 0:
                        continue

                    # Check if the neighbor cell is within the grid boundaries
                    row = i + k
                    col = j + l
                    if row >= 0 and row < len(grid) and col >= 0 and col < len(grid[i]):
                        # Add the value of the neighbor cell to the count
                        neighbors += grid[row][col]

            # Apply the rules of the game to the cell
            if grid[i][j] == 1:
                # If the cell is alive, it stays alive if it has 2 or 3 neighbors, otherwise it dies
                if neighbors == 2 or neighbors == 3:
                    new_grid[i][j] = 1
                else:
                    new_grid[i][j] = 0
            else:
                # If the cell is dead, it becomes alive if it has exactly 3 neighbors, otherwise it stays dead
                if neighbors == 3:
                    new_grid[i][j] = 1
                else:
                    new_grid[i][j] = 0

    # Return the new grid
    return new_grid

# Grid drawing
def draw_on_grid(grid):
    # Get the position and the state of the mouse
    x, y = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()
    i = y // CELL_SIZE
    j = x // CELL_SIZE

    # Check if the left mouse button is pressed
    if pressed[0] and grid[i][j] == 0:
        grid[i][j] = 1
    elif pressed[2] and grid[i][j] == 1:
        grid[i][j] = 0
# Create a grid of cells
grid = create_grid()

# Set a flag to control the simulation
running = True

# Main loop
while True:
    # Handle events
    for event in pygame.event.get():
        # Quit the program if the user closes the window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Toggle the simulation if the user presses the space bar
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = not running

    # Draw on the grid by holding down the mouse button
    draw_on_grid(grid)

    # Update the grid if the simulation is running
    if running:
        grid = update_grid(grid)

    # Draw the grid on the screen
    draw_grid(grid)

    # Update the display
    pygame.display.flip()

    # Lock to 60fps
    clock.tick(60)
