'''NOTE: THIS IS A POTENTIAL SOLUTION
         If approved we will be removing code part from all functions except play_game inside YantraCollector Class.
'''
import random
from adversary import AdversaryMove, NoviceMove

class YantraCollector:
    def __init__(self, p1_pos, p2_pos, goal_pos,grid_size,player1_strategy):
        """
        Initializes the game with the starting positions of Player 1, Player 2, and the goal position.
       

        Parameters:
        - p1_pos (tuple): (row, col) position of Player 1.
        - p2_pos (tuple): (row, col) position of Player 2.
        - goal_pos (tuple): (row, col) position of the goal.

        Returns:
        - None
        """
        self.p1_pos = p1_pos  
        self.p2_pos = p2_pos
        self.goal_pos = goal_pos
        self.grid_size = grid_size
        self.p1_strat = player1_strategy 
        self.is_p1_turn = True  # Track whose turn it is
        self.path=[]

    def is_valid(self, pos):
        """
        Checks if a position is within the game grid boundaries.

        Parameters:
        - pos (tuple): (row, col) position to check.

        Returns:
        - bool: True if position is valid, False otherwise.
        """
        # pass
        x,y = pos
        if(x < 0 or x > self.grid_size or y < 0 or y > self.grid_size):return False
        return True


    def move_player(self, player, direction):
        """
        Moves the given player in the specified direction. 
        ENSURE THAT THE PLAYER MAKES A MOVE THAT IS "VALID", i.e., IT IS MOVING TO A POSITION INSIDE THE GRID

        Parameters:
        - player (int): 1 for Player 1, 2 for Player 2.
        - direction (str): One of ['N', 'S', 'E', 'W'] indicating the movement direction.

        Returns:
        - None
        """
        move_offsets = {'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0)}
        
        if player == 1:
            new_pos = (self.p1_pos[0] + move_offsets[direction][0], self.p1_pos[1] + move_offsets[direction][1])
            if self.is_valid(new_pos):
                self.p1_pos = new_pos
        else:
            new_pos = (self.p2_pos[0] + move_offsets[direction][0], self.p2_pos[1] + move_offsets[direction][1])
            if self.is_valid(new_pos):
                self.p2_pos = new_pos

    def utility(self, pos):
        """
        Computes a utility score based on the player's distance to the goal vs the opponent's distance to the goal.

        Parameters:
        - pos (tuple): The position to evaluate.

        Returns:
        - int: The utility value (lower values are better for the player).
        """
        # pass
        g_x, g_y = self.goal_pos
        x, y = pos
        return abs(g_x - x) + abs(g_y - y)

    def best_player_move(self, pos):
        """
        Determines the best move for Player 1 as per the current strategy for Player 1 (stored in self.p1_strat)

        Parameters:
        - pos (tuple): The current position of the player.
        - depth (int): Search depth for minimax.

        Returns:
        - str: The best move direction ('N', 'S', 'E', 'W').
        """
        # pass

        if self.p1_strat == "random":
            return self.random_move(pos)
        
        elif self.p1_strat == "minimax_vanilla":
            
            #here we have to find the best move for the player to choose so in our fn we have to keep track of the best move as well
            move_to_choose = ""
            max_score = -999999

            for move in ['N','S','W','E']:
                self.move_player(1,move)

                score = self.minimax_vanilla(self.p1_pos,4, max_turn=False)


                self.p1_pos = pos

                if score > max_score:
                    max_score = score
                    move_to_choose = move
            return move_to_choose


        elif self.p1_strat == "minimax":
                
                #here we have to find the best move for the player to choose so in our fn we have to keep track of the best move as well
            move_to_choose = ""
            max_score = -999999

            for move in ['N','S','W','E']:
                self.move_player(1,move)

                score = self.minimax(self.p1_pos,4,alpha=float('-inf'), beta=float('inf'), max_turn=False)


                self.p1_pos = pos

                if score > max_score:
                    max_score = score
                    move_to_choose = move
            return move_to_choose

        else:
            print("Wrong strategy\n")
    
    def random_move(self, pos):
        """
        Chooses a random valid move.
        Parameters:
        - pos (tuple): The current position.

        Returns:
        - str: A random move direction ('N', 'S', 'E', 'W').
        """

        no = random.randint(0,3)
        x,y = pos
        value = None
        # store_pos = pos
        if no == 0:
            y = y+1
            if self.is_valid((x,y)):return 'N'
            else: value = self.random_move(pos)
        elif no == 1:
            y = y-1
            if self.is_valid((x,y)):return 'S'
            else: value = self.random_move(pos)


        elif no == 2:
            x = x + 1
            if self.is_valid((x,y)):return 'E'
            else: value  =  self.random_move(pos)

        elif no == 3 :
            x = x -1
            if self.is_valid((x,y)):return 'W'
            else: value = self.random_move(pos)

        return value
        

        # return None 
    
    def minimax_vanilla(self, pos, depth, max_turn=True):
        """
        Determines the best move using the vanilla Minimax algorithm (without alpha-beta pruning).

        Parameters:
        - pos (tuple): The current position of the player.
        - depth (int): Search depth for minimax.
        - max_turn (bool): True if maximizing Player 1, False for minimizing Player 2.

        Returns:
        - int: The minimax score if called recursively.
        """
        # pass


        #check if the depth is zero or not
        if depth == 0:
            return self.utility(pos)
        
        if max_turn:
            max_value = -999999
            possible_dir = ['N','S','E','W']
            for move in possible_dir:

                prev_pos = pos

                self.move_player(1,move)

                value = self.minimax_vanilla(self.p1_pos, depth-1, False)

                pos = prev_pos

                max_value = max(max_value, value)
            return max_value
        
        else:
            min_value = 999999
            possible_dir = ['N','S','E','W']
            for move in possible_dir:
                prev_pos = pos
                self.move_player(1,move)
                value = self.minimax_vanilla(self.p1_pos, depth-1, True)

                pos = prev_pos

                min_value = min(min_value, value)

            return min_value

    def minimax(self, pos, depth, alpha=float('-inf'), beta=float('inf'), max_turn=True):
        """
        Implements the minimax algorithm with alpha-beta pruning to determine the best move.

        Parameters:
        - pos (tuple): The current position.
        - depth (int): Depth remaining in search.
        - alpha (float): Alpha value for pruning.
        - beta (float): Beta value for pruning.
        - max_turn (bool): True if maximizing Player 1, False for minimizing Player 2.

        Returns:
        - int: The minimax score.
        """
        # pass
        if depth == 0:
            return self.utility(pos)
        
        if max_turn:
            max_value = -999999
            possible_dir = ['N','S','E','W']
            for move in possible_dir:
                prev_pos = pos
                self.move_player(1,move)
                # new_pos = (pos[0] + 
                value = self.minimax_vanilla(self.p1_pos, depth-1, False)
                pos = prev_pos
                max_value = max(max_value, value)

                alpha = max(alpha, max_value)

                if beta <= alpha:
                    break

            return max_value
        
        else:
            min_value = 999999
            possible_dir = ['N','S','E','W']
            for move in possible_dir:
                prev_pos = pos
                self.move_player(1,move)
                value = self.minimax_vanilla(self.p1_pos, depth-1, True)

                pos = prev_pos

                min_value = min(min_value, value)

                beta = min(beta, min_value)
                if beta <= alpha:
                    break


            return min_value



    def play_game(self):
        """
        Runs the game loop until a player reaches the goal or a draw occurs.

        Returns:
        - str: "P1" if Player 1 wins, "P2" if Player 2 wins, or "draw" if there's no winner.
        """
        seen_positions = set()
        while True:
            state = (self.p1_pos, self.p2_pos)
            if self.p1_pos == self.p2_pos:
                return "draw"
            if state in seen_positions:
                return "draw"
            seen_positions.add(state)

            if self.is_p1_turn:
                best_move = self.best_player_move(self.p1_pos)
                self.path.append(best_move)
                self.move_player(1, best_move)
                self.move_player(2, best_move)  # P2 mimics P1
            else:
                best_move = AdversaryMove(self.p2_pos, self)
                self.move_player(2, best_move)
                self.move_player(1, best_move)  # P1 mimics P2
                    
            if self.p1_pos == self.goal_pos:
                return "P1"
            
            elif self.p2_pos == self.goal_pos:
                return "P2"
            
            self.is_p1_turn = not self.is_p1_turn

    def play_game_novice(self):
        """
        Runs the game loop where Player 2 follows a novice strategy (always moving East if possible).

        Returns:
        - str: "P1" if Player 1 wins, "P2" if Player 2 wins, or "draw" if there's no winner.
        """
        seen_positions = set()
        while True:
            state = (self.p1_pos, self.p2_pos)
            if self.p1_pos == self.p2_pos:
                return "draw"
            if state in seen_positions:
                return "draw"
            seen_positions.add(state)

            if self.is_p1_turn:
                best_move = self.best_player_move(self.p1_pos)
                self.path.append(best_move)
                self.move_player(1, best_move)
                self.move_player(2, best_move)  # P2 mimics P1
            else:
                best_move = NoviceMove(self.p2_pos,self)  # Using NoviceMove
                self.move_player(2, best_move)
                self.move_player(1, best_move)  # P1 mimics P2
                    
            if self.p1_pos == self.goal_pos:
                return "P1"
            
            elif self.p2_pos == self.goal_pos:
                return "P2"
            
            self.is_p1_turn = not self.is_p1_turn  

