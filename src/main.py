# TODO: Arena.py: Compete AI against one another

import pygame
import sys
from game import Connect4
from board import draw_board
from ai import get_best_move

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
    draw_menu(screen)
    play_against_ai = get_menu_choice()

    game = Connect4()
    game_over = False

    draw_board(screen, game.board)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if game.current_player == 1:
                if play_against_ai:
                    game_over = ai_move(game)
                    pygame.time.wait(200)
                else:
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
                                print("\nPlayer 1/Red wins.")
                                game.print_board()
                                game_over = True
                            else:
                                game.switch_player()

                        draw_board(screen, game.board)
            
            else:       # Player 2's turn 
                #print(f'\rBest move for player {game.current_player} is column {bmove+1} with a score of {bscore}.')
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, LIGHTGRAY, (0, 0, WIDTH, SIZE))
                    posx = event.pos[0]
                    col = posx // SIZE
                    posx = col * SIZE + SIZE // 2

                    pygame.draw.circle(screen, ORANGE, (posx, SIZE // 2), RAD)
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, LIGHTGRAY, (0, 0, WIDTH, SIZE))
                    posx = event.pos[0]
                    col = posx // SIZE

                    if game.drop_disc(col):
                        draw_board(screen, game.board)
                        if game.check_win():
                            print("\nPlayer 2/Orange wins.")
                            game.print_board()
                            game_over = True
                        else:
                            game.switch_player()

                        draw_board(screen, game.board)


def draw_menu(screen):
    screen.fill(BLACK)
    font = pygame.font.SysFont('Arial', 50)
    text1 = font.render('1. Play against AI', True, WHITE)
    text2 = font.render('2. Play against Human', True, WHITE)
    screen.blit(text1, (100, 150))
    screen.blit(text2, (100, 250))
    pygame.display.update()

def get_menu_choice():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return True
                elif event.key == pygame.K_2:
                    return False

def ai_move(game):
    best_move, _ = get_best_move(game, game.current_player)
    game.drop_disc(best_move, game.board, game.current_player)
    draw_board(screen, game.board)
    if game.check_win():
        print('end')
        winner = "Red" if game.current_player == 1 else "Orange"
        pygame.time.wait(2000)
        game.print_board()
        print(f"\nPlayer {game.current_player}/{winner} wins.")
        return True
    else:
        game.switch_player()
    return False

if __name__ == "__main__":
    main()
