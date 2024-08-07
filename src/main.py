# TODO: Arena.py: Compete AI against one another

import pygame
import sys
from game import Connect4
from board import draw_board

pygame.init()

WIDTH, SIZE = 700, 100
HEIGHT = SIZE * 7
SIZE = WIDTH // 7
RAD = SIZE // 2 - 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
LIGHTGRAY = (211, 211, 211)
LIGHTERGRAY = (175, 175, 175)
DARKGRAY = (109, 109, 109)

button_font = pygame.font.SysFont('Arial', 25)
button_text = button_font.render('Restart', True, BLACK)
button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT + 10, 100, 30)


def main():
    game = Connect4()
    game_over = False

    draw_board(screen, game.board)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, DARKGRAY, (0, 0, WIDTH, SIZE))
                posx = event.pos[0]
                col = posx // SIZE
                posx = col * SIZE + SIZE // 2

                if game.current_player == 1:
                    pygame.draw.circle(screen, RED, (posx, SIZE // 2), RAD)
                else:
                    pygame.draw.circle(screen, ORANGE, (posx, SIZE // 2), RAD) 

                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, LIGHTGRAY, (0, 0, WIDTH, SIZE))
                posx = event.pos[0]
                col = posx // SIZE

                if game.drop_disc(col):
                    draw_board(screen, game.board)
                    if game.check_win():
                        winner = "Red" if game.current_player == 1 else "Orange"
                        print(f"\nPlayer {game.current_player}/{winner} wins.")
                        game_over = True
                    else:
                        game.switch_player()

                draw_board(screen, game.board)

def aiplay():
    game = Connect4()
    game_over = False
    
    draw_board(screen, game.board)

    while not game_over:
        pass

if __name__ == "__main__":
    main()
