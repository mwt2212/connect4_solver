class Connect4:
    def __init__(self):
        self.board = self.create_board()
        self.rows = len(self.board)
        self.cols = len(self.board[0])
        self.current_player = 1

    def create_board(self):
        return [[0 for _ in range(7)] for _ in range(6)]
    
    def drop_disc(self, column, board=None, player=None):
        if board is None:
            board = self.board
        if player is None:
            player = self.current_player
        
        for row in reversed(range(self.rows)):
            if board[row][column] == 0:
                board[row][column] = player
                return True
        return False
    
    def print_board(self):
        for row in self.board:
            print(row)
    
    def check_win(self, player=None):
        if player is None:
            player = self.current_player

        for row in range(self.rows):        # Horizontal win
            for col in range(self.cols - 3):
                if all(self.board[row][col+i] == player for i in range(4)):
                    return True
            
        for col in range(self.cols):        # Vertical win
            for row in range(self.rows - 3):
                if all(self.board[row+i][col] == player for i in range(4)):
                    return True
                
        for row in range(self.rows - 3):    # Pos sloped wins, bottom left to top right
            for col in range(self.cols - 3):
                if all(self.board[row+i][col+i] == player for i in range(4)):
                    return True
        
        for row in range(3, self.rows):     # Neg sloped wins, top left to bottom right
            for col in range(self.cols - 3):
                if all(self.board[row-i][col+i] == player for i in range(4)):
                    return True
        
        return False
    
    def switch_player(self):
        self.current_player = 1 if self.current_player == 2 else 2

    

