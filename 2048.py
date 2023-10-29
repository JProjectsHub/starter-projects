import random
import pygame

# Initialize the game board as a 4x4 grid
board = [[0 for _ in range(4)] for _ in range(4)]

# Set two random cells to contain a "2" tile
for _ in range(2):
    while True:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            board[row][col] = 2
            break

#Game window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
CELL_SIZE = 100
CELL_MARGIN = 10
BACKGROUND_COLOR = (187,173,160)
TILE_COLORS = {
    0: (205,193,180),
    2: (238,228,218),
    4: (237,224,200),
}

#Initialize Pygame
pygame.init()

#Create game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('2048 Game')

#Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    #Draw the game board
    window.fill(BACKGROUND_COLOR)
    for row in range(4):
        for col in range(4):
            # Calculate the position of the cell on the window
            x = col * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN
            y = row * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN

            # Get the value of the tile in the cell
            tile_value = board[row][col]

            # Draw the cell rectangle
            pygame.draw.rect(window, TILE_COLORS[tile_value], (x, y, CELL_SIZE, CELL_SIZE))

            # Draw the tile value text
            if tile_value > 0:
                font = pygame.font.Font(None, 36)
                text = font.render(str(tile_value), True, (0, 0, 0))  # Black color for tile value text
                window.blit(text, (x + CELL_SIZE // 2 - text.get_width() // 2,
                                   y + CELL_SIZE // 2 - text.get_height() // 2))

    pygame.display.flip()






