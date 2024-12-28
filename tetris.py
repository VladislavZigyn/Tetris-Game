import pygame
import random

# Initialization Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
COLORS = [
    (0, 255, 255),  # Blue
    (0, 0, 255),    # Blue
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (128, 0, 128),  # Violet
    (255, 0, 0)     # Red
]

# Description of figures
SHAPES = [
    [  # Stick
        [[1, 1, 1, 1]],
        [[1], [1], [1], [1]]
    ],
    [  # Square
        [[1, 1], [1, 1]]
    ],
    [  # T-shaped
        [[0, 1, 0], [1, 1, 1]],
        [[1, 0], [1, 1], [1, 0]],
        [[1, 1, 1], [0, 1, 0]],
        [[0, 1], [1, 1], [0, 1]]
    ],
    [  # L-shaped
        [[1, 0, 0], [1, 1, 1]],
        [[1, 1], [1, 0], [1, 0]],
        [[1, 1, 1], [0, 0, 1]],
        [[0, 1], [0, 1], [1, 1]]
    ],
    [  # Reverse L
        [[0, 0, 1], [1, 1, 1]],
        [[1, 0], [1, 0], [1, 1]],
        [[1, 1, 1], [1, 0, 0]],
        [[1, 1], [0, 1], [0, 1]]
    ]
]

# Figure class
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
        self.rotation = 0

    def rotate(self):
        """Changes the current rotation of the figure"""
        self.rotation = (self.rotation + 1) % len(self.shape)

    def current_shape(self):
        """Returns the current shape matrix"""
        return self.shape[self.rotation]

# Creating a grid
def create_grid():
    return [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Drawing a grid
def draw_grid(surface, grid):
    surface.fill(BLACK)
    for y, row in enumerate(grid):
        for x, color in enumerate(row):
            pygame.draw.rect(surface, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    for x in range(GRID_WIDTH):
        pygame.draw.line(surface, GRAY, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, SCREEN_HEIGHT))
    for y in range(GRID_HEIGHT):
        pygame.draw.line(surface, GRAY, (0, y * BLOCK_SIZE), (SCREEN_WIDTH, y * BLOCK_SIZE))

# Checking the admissibility of the figure's position
def valid_space(piece, grid):
    shape = piece.current_shape()
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:  # Если в клетке есть блок
                new_x = piece.x + x
                new_y = piece.y + y
                if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                    return False
                if new_y >= 0 and grid[new_y][new_x] != BLACK:
                    return False
    return True

# Locking a figure in a grid
def lock_piece(piece, grid):
    shape = piece.current_shape()
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid[piece.y + y][piece.x + x] = piece.color

# Clearing filled lines
def clear_lines(grid):
    lines_cleared = 0
    for y in range(GRID_HEIGHT - 1, -1, -1):
        if all(grid[y][x] != BLACK for x in range(GRID_WIDTH)):
            del grid[y]
            grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
            lines_cleared += 1
    return lines_cleared

# The main game loop
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    grid = create_grid()
    current_piece = Piece(GRID_WIDTH // 2 - 1, 0, random.choice(SHAPES))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        current_piece.rotate()  # We cancel the rotation if it is not allowed

        # Fall of the figure
        current_piece.y += 1
        if not valid_space(current_piece, grid):
            current_piece.y -= 1
            lock_piece(current_piece, grid)
            current_piece = Piece(GRID_WIDTH // 2 - 1, 0, random.choice(SHAPES))
            if not valid_space(current_piece, grid):
                print("Game Over")
                running = False

        # Cleaning the lines
        clear_lines(grid)

        # Drawing
        draw_grid(screen, grid)
        shape = current_piece.current_shape()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        current_piece.color,
                        ((current_piece.x + x) * BLOCK_SIZE, (current_piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    )

        pygame.display.flip()
        clock.tick(5)

if __name__ == "__main__":
    main()