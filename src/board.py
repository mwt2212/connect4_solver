import pygame
WIDTH = 700
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
LIGHTGRAY = (175, 175, 175)
GRAY = (211, 211, 211)
DARKGRAY = (109, 109, 109)
DARKERGRAY = (65, 65, 65)

def draw_board(screen, board):
    rows, cols = len(board), len(board[0])
    SIZE = screen.get_width() // cols
    RAD = SIZE // 2 - 5
    
    for row in range(rows):
        for col in range(cols):
            pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, SIZE))
            pygame.draw.rect(screen, DARKERGRAY, (col * SIZE, row * SIZE + SIZE, SIZE, SIZE))

            pygame.draw.circle(screen, LIGHTGRAY, (int(col * SIZE + SIZE / 2), int(row * SIZE + SIZE + SIZE / 2)), RAD)
    
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, (int(col * SIZE + SIZE / 2), screen.get_height() - int(row * SIZE + SIZE / 2)), RAD)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, ORANGE, (int(col * SIZE + SIZE / 2), screen.get_height() - int(row * SIZE + SIZE / 2)), RAD)
    
    pygame.display.update()

