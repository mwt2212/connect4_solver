# TODO: Build arena to compete AI, testing for best weights.

from game import Connect4
import pygame
import sys
from ai import AIPlayer
from board import draw_board
DEPTH = 2

class Arena:
    def __init__(self, ai1, ai2):
        self.ai1 = ai1
        self.ai2 = ai2
        self.results = {"AI1 Wins": 0, "AI2 Wins": 0, "Draws": 0}
        self.board1 = None
        self.board2 = None
        self.screen1 = pygame.display.set_mode((700, 700))
        self.screen2 = pygame.display.set_mode((700, 700))
        pygame.display.set_caption("Connect 4 AI Arena")

    def play_game(self, ai1, ai2):
        game = Connect4()
        game_over = False
        current_player = ai1 if game.current_player == 1 else ai2
        

        while not game_over:
            col, _ = current_player.get_best_move(game)
            game.drop_disc(col)
            game_over = game.check_win(game.current_player) or game.is_draw()
            if not game_over:
                game.switch_player()
                current_player = ai1 if game.current_player == 1 else ai2

        
        if game.check_win(game.current_player):
            game.print_board()
            print(f'\n{game.current_player} wins.')
            return game.current_player, game.board
        else:
            game.print_board()
            print('\nTie.')
            return 0, game.board
        

    def run(self):
        result1, board1 = self.play_game(self.ai1, self.ai2)
        if result1 == 1:
            self.results["AI1 Wins"] += 1
        elif result1 == 2:
            self.results["AI2 Wins"] += 1
        else:
            self.results["Draws"] += 1


        self.ai1.player_id = 2
        self.ai2.player_id = 1
        result2, board2 = self.play_game(self.ai2, self.ai1)
        if result2 == 1:
            self.results["AI2 Wins"] += 1
        elif result2 == 2:
            self.results["AI1 Wins"] += 1
        else:
            self.results["Draws"] += 1

        self.board1 = board1
        self.board2 = board2

        self.display_boards()

        print(f'AI 1 Wins: {self.results["AI1 Wins"]}, AI 2 Wins: {self.results["AI2 Wins"]}, Draws: {self.results["Draws"]}')

    def display_boards(self):
        pygame.display.set_caption("Results")
        waiting = True
        while waiting:
            self.screen1.fill((0, 0, 0))
            self.screen2.fill((0, 0, 0))
            draw_board(self.screen1, self.board1)
            draw_board(self.screen2, self.board2)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    waiting = False


if __name__ == "__main__":
    weights_ai1 = {'total_pieces': 0.1, 
                   'count_two': 0.3, 
                   'count_three': 0.9, 
                   'center': 0.15, 
                   'adjacent': 0.125
                   }
    
    weights_ai2 = {'total_pieces': 0.1, 
                   'count_two': 0.5, 
                   'count_three': .4, 
                   'center': 0.2, 
                   'adjacent': 0.6
                   }

    ai_player1 = AIPlayer(player_id=1, weights=weights_ai1, depth=DEPTH)
    ai_player2 = AIPlayer(player_id=2, weights=weights_ai2, depth=DEPTH)

    arena = Arena(ai_player1, ai_player2)
    arena.run()

