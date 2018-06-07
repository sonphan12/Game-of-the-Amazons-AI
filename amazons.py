import random


# ======================== Class Player =======================================
class Player:
    # student do not allow to change two first functions
    def __init__(self, str_name):
        self.str = str_name

    def __str__(self):
        return self.str

    # Student MUST implement this function
    # The return value should be a move that is denoted by a list of tuples:
    # [(row1, col1), (row2, col2), (row3, col3)] with:
    # (row1, col1): current position of selected amazon
    # (row2, col2): new position of selected amazon
    # (row3, col3): position of the square is shot
    def nextMove(self, state):
        result = [(0, 3), (5, 3), (8, 6)]  # example move in wikipedia
        result = [(random.randint(0, 9), random.randint(0, 9)), (random.randint(0, 9), random.randint(0, 9)),
                  (random.randint(0, 9), random.randint(0, 9))]
        while not self.isValidMove(result, state):
            result = [(random.randint(0, 9), random.randint(0, 9)), (random.randint(0, 9), random.randint(0, 9)),
                      (random.randint(0, 9), random.randint(0, 9))]
        return result

    def board_copy(self, board):
        new_board = [[]] * 10
        for i in range(10):
            new_board[i] = [] + board[i]
        return new_board

    def isValidMove(self, move, state):
        from_x = move[0][0]
        from_y = move[0][1]
        to_x = move[1][0]
        to_y = move[1][1]
        shot_x = move[2][0]
        shot_y = move[2][1]
        # Out of bound
        if to_x < 0 or to_x > 10 or to_y < 0 or to_y > 10 or shot_x < 0 or shot_x > 10 or shot_y < 0 or shot_x > 10:
            return False
        # The 'from' has invalid object
        if state[from_x][from_y] != self.str:
            return False
        # The place is already having something on
        if state[to_x][to_y] != '.' or state[shot_x][shot_y] != '.':
            return False
        # Trying to shoot 'to' position
        if to_x == shot_x and to_y == shot_y:
            return False
        # Invalid rule
        if abs(to_x - from_x) != abs(to_y - from_y) and to_x != from_x and to_y != from_y:
            return False
        if abs(shot_x - to_x) != abs(shot_y - to_y) and shot_x != to_x and shot_y != to_y:
            return False
        # Check block
        if self.isBlocked(move, state):
            return False
        return True

    def move(self, move, state):
        from_x = move[0][0]
        from_y = move[0][1]
        to_x = move[1][0]
        to_y = move[1][1]
        shot_x = move[2][0]
        shot_y = move[2][1]
        state[from_x][from_y] = '.'
        state[to_x][to_y] = self.str
        state[shot_x][shot_y] = 'X'

    # # Evaluate a state
    # def evaluate(self, state):
    #     block_dict = {}
    #     queen_dict = {}
    #     evaluate_value = 0
    #     for i in [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]:
    #         for j in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
    #             if state[i][j] == 'X':
    #                 block_dict[(i, j)] = state[i][j]
    #             elif state[i][j] != '.':
    #                 queen_dict[(i, j)] = state[i][j]
    #
    #     for queen in queen_dict:

    # Block each other?
    def isBlockEachOther(self, place1, place2):
        if abs(place1[0] - place2[0]) != abs(place1[0] - place2[0]) and place1[0] != place2[0] \
                and place1[1] != place2[1]:
            return False
        return True

    def isBlocked(self, move, state):
        from_x = move[0][0]
        from_y = move[0][1]
        to_x = move[1][0]
        to_y = move[1][1]
        shot_x = move[2][0]
        shot_y = move[2][1]
        # Check block when moving
        # Horizontal aligned
        if from_x == to_x:
            if from_y < to_y:
                for i in range(from_y + 1, to_y):
                    if state[from_x][i] != '.':
                        return True
            else:
                for i in range(to_y + 1, from_y):
                    if state[from_x][i] != '.':
                        return True
        # Vertical aligned
        elif from_y == to_y:
            if from_x < to_x:
                for i in range(from_x + 1, to_x):
                    if state[from_x][i] != '.':
                        return True
            else:
                for i in range(to_x + 1, from_x):
                    if state[from_x][i] != '.':
                        return True
        # Diagonally aligned
        elif abs(from_x - to_x) == abs(from_y - to_y):
            # Bottom right
            if to_x < from_x and to_y > from_y:
                i = from_x - 1
                j = from_y + 1
                while i > to_x and j < to_y:
                    if state[i][j] != '.':
                        return True
                    i = i - 1
                    j = j + 1
            # Top right
            elif to_x > from_x and to_y > from_y:
                i = from_x + 1
                j = from_y + 1
                while i < to_x and j < to_y:
                    if state[i][j] != '.':
                        return True
                    i = i + 1
                    j = j + 1
            # Bottom left
            elif to_x < from_x and to_y < from_y:
                i = from_x - 1
                j = from_y - 1
                while i > to_x and j > to_y:
                    if state[i][j] != '.':
                        return True
                    i = i - 1
                    j = j - 1
            # Top left
            elif to_x > from_x and to_y < from_y:
                i = from_x + 1
                j = from_y - 1
                while i < to_x and j > to_y:
                    if state[i][j] != '.':
                        return True
                    i = i + 1
                    j = j - 1

        # Check block when shooting
        # Horizontal aligned
        if to_x == shot_x:
            if to_y < shot_y:
                for i in range(to_y + 1, shot_y):
                    if state[to_x][i] != '.':
                        return True
            else:
                for i in range(shot_y + 1, to_y):
                    if state[to_x][i] != '.':
                        return True
        # Vertical aligned
        elif to_y == shot_y:
            if to_x < shot_x:
                for i in range(to_x + 1, shot_x):
                    if state[to_x][i] != '.':
                        return True
            else:
                for i in range(shot_x + 1, to_x):
                    if state[to_x][i] != '.':
                        return True
        # Diagonally aligned
        elif abs(to_x - shot_x) == abs(to_y - shot_y):
            # Bottom right
            if shot_x < to_x and shot_y > to_y:
                i = to_x - 1
                j = to_y + 1
                while i > shot_x and j < shot_y:
                    if state[i][j] != '.':
                        return True
                    i = i - 1
                    j = j + 1
            # Top right
            elif shot_x > to_x and shot_y > to_y:
                i = to_x + 1
                j = to_y + 1
                while i < shot_x and j < shot_y:
                    if state[i][j] != '.':
                        return True
                    i = i + 1
                    j = j + 1
            # Bottom left
            elif shot_x < to_x and shot_y < to_y:
                i = to_x - 1
                j = to_y - 1
                while i > shot_x and j > shot_y:
                    if state[i][j] != '.':
                        return True
                    i = i - 1
                    j = j - 1
            # Top left
            elif shot_x > to_x and shot_y < to_y:
                i = to_x + 1
                j = to_y - 1
                while i < shot_x and j > shot_y:
                    if state[i][j] != '.':
                        return True
                    i = i + 1
                    j = j - 1
        return False
