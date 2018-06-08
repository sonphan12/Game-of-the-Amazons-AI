import random
import copy


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
        # result = [(0, 3), (5, 3), (8, 6)]  # example move in wikipedia
        # result = [(random.randint(0, 9), random.randint(0, 9)), (random.randint(0, 9), random.randint(0, 9)),
        #           (random.randint(0, 9), random.randint(0, 9))]
        # while not self.isValidMove(result, state):
        #     result = [(random.randint(0, 9), random.randint(0, 9)), (random.randint(0, 9), random.randint(0, 9)),
        #               (random.randint(0, 9), random.randint(0, 9))]
        result = None
        validMoves = self.getAllValidMove(state)
        if len(validMoves) != 0:
            result = validMoves[random.randint(0, len(validMoves) - 1)]
            # result = validMoves[0]
        return result

    def board_copy(self, board):
        new_board = [[]] * 10
        for i in range(10):
            new_board[i] = [] + board[i]
        return new_board

    def isValidMove(self, move, state):
        return self.isValidPlaceQueen([move[0], move[1]], state) and self.isValidShooting(move, state)

    def isValidPlaceQueen(self, move, state):
        from_x = move[0][0]
        from_y = move[0][1]
        to_x = move[1][0]
        to_y = move[1][1]
        # Out of bound
        if to_x < 0 or to_x > 10 or to_y < 0 or to_y > 10:
            return False
        # The 'from' has invalid object
        if state[from_x][from_y] != self.str:
            return False
        # The place is already having something on
        if state[to_x][to_y] != '.':
            return False
        # Invalid rule
        if abs(to_x - from_x) != abs(to_y - from_y) and to_x != from_x and to_y != from_y:
            return False
        # Check block
        if self.isBlockedPlaceQueen(move, state):
            return False
        return True

    def isValidShooting(self, move, state):
        shoot_from_x = move[1][0]
        shoot_from_y = move[1][1]
        shoot_to_x = move[2][0]
        shoot_to_y = move[2][1]
        last_from_x = move[0][0]
        last_from_y = move[0][1]
        # Out of bound
        if shoot_from_x < 0 or shoot_from_x > 10 or shoot_from_y < 0 or shoot_from_y > 10\
                or shoot_to_x < 0 or shoot_to_x > 10 or shoot_to_y < 0 or shoot_to_y > 10:
            return False
        # The place is already having something on
        if state[shoot_to_x][shoot_to_y] != '.' and (shoot_to_x != last_from_x or shoot_to_y != last_from_y):
            return False
        # Invalid rule
        if abs(shoot_from_x - shoot_to_x) != abs(shoot_from_y - shoot_to_y) and shoot_to_x != shoot_from_x and shoot_to_y != shoot_from_y:
            return False
        # Shoot itself:
        if shoot_from_x == shoot_to_x and shoot_from_y == shoot_to_y:
            return False
        # Check block
        if self.isBlockedShooting(move, state):
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

    def getAllValidMove(self, state):
        # Move format ((from_x, from_y), (to_x, to_y), (shot_x, shot_y))
        moveArr = []
        placeArr = self.getAllValidPlaceQueen(state)
        for place in placeArr:
            moveArr += self.getAllValidShootingFromPlace(place, state)
        return moveArr

    def getAllValidPlaceQueen(self, state):
        result = []
        for i in [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]:
            for j in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                if state[i][j] == self.str:
                    # Horizontal move
                    m = i
                    n = 0
                    while n < 10:
                        if self.isValidPlaceQueen([(i, j), (m, n)], state):
                            result.append([(i, j), (m, n)])
                        n += 1
                    # Vertical move
                    m = 0
                    n = j
                    while m < 10:
                        if self.isValidPlaceQueen([(i, j), (m, n)], state):
                            result.append([(i, j), (m, n)])
                        m += 1
                    # Top left
                    m = i + 1
                    n = j - 1
                    while m < 10 and n > -1:
                        if self.isValidPlaceQueen([(i, j), (m, n)], state):
                            result.append([(i, j), (m, n)])
                        m += 1
                        n -= 1
                    # Top right
                    m = i + 1
                    n = j + 1
                    while m < 10 and n < 10:
                        if self.isValidPlaceQueen([(i, j), (m, n)], state):
                            result.append([(i, j), (m, n)])
                        m += 1
                        n += 1
                    # Bottom left
                    m = i - 1
                    n = j - 1
                    while m > -1 and n > -1:
                        if self.isValidPlaceQueen([(i, j), (m, n)], state):
                            result.append([(i, j), (m, n)])
                        m -= 1
                        n -= 1
                    # Bottom right:
                    m = i - 1
                    n = j + 1
                    while m > -1 and n < 10:
                        if self.isValidPlaceQueen([(i, j), (m, n)], state):
                            result.append([(i, j), (m, n)])
                        m -= 1
                        n += 1
        return result

    def getAllValidShootingFromPlace(self, place, state):
        result = []
        # Horizontal
        m = place[1][0]
        n = 0
        while n < 10:
            m_place = copy.deepcopy(place)
            m_place.append((m, n))
            if self.isValidShooting(m_place, state):
                result.append(m_place)
            n += 1
        # Vertical
        m = 0
        n = place[1][1]
        while m < 10:
            m_place = copy.deepcopy(place)
            m_place.append((m, n))
            if self.isValidShooting(m_place, state):
                result.append(m_place)
            m += 1
        # Top left
        m = place[1][0] + 1
        n = place[1][1] - 1
        while m < 10 and n > -1:
            m_place = copy.deepcopy(place)
            m_place.append((m, n))
            if self.isValidShooting(m_place, state):
                result.append(m_place)
            m += 1
            n -= 1
        # Top right
        m = place[1][0] + 1
        n = place[1][1] + 1
        while m < 10 and n < 10:
            m_place = copy.deepcopy(place)
            m_place.append((m, n))
            if self.isValidShooting(m_place, state):
                result.append(m_place)
            m += 1
            n += 1
        # Bottom left
        m = place[1][0] - 1
        n = place[1][1] - 1
        while m > -1 and n > -1:
            m_place = copy.deepcopy(place)
            m_place.append((m, n))
            if self.isValidShooting(m_place, state):
                result.append(m_place)
            m -= 1
            n -= 1
        # Bottom right:
        m = place[1][0] - 1
        n = place[1][1] + 1
        while m > -1 and n < 10:
            m_place = copy.deepcopy(place)
            m_place.append((m, n))
            if self.isValidShooting(m_place, state):
                result.append(m_place)
            m -= 1
            n += 1
        return result



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
        return self.isBlockedPlaceQueen([move[0], move[1]], state) and self.isBlockedShooting(move, state)

    def isBlockedPlaceQueen(self, move, state):
        from_x = move[0][0]
        from_y = move[0][1]
        to_x = move[1][0]
        to_y = move[1][1]
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
                    if state[i][from_y] != '.':
                        return True
            else:
                for i in range(to_x + 1, from_x):
                    if state[i][from_y] != '.':
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
                    i -= 1
                    j += 1
            # Top right
            elif to_x > from_x and to_y > from_y:
                i = from_x + 1
                j = from_y + 1
                while i < to_x and j < to_y:
                    if state[i][j] != '.':
                        return True
                    i += 1
                    j += 1
            # Bottom left
            elif to_x < from_x and to_y < from_y:
                i = from_x - 1
                j = from_y - 1
                while i > to_x and j > to_y:
                    if state[i][j] != '.':
                        return True
                    i -= 1
                    j -= 1
            # Top left
            elif to_x > from_x and to_y < from_y:
                i = from_x + 1
                j = from_y - 1
                while i < to_x and j > to_y:
                    if state[i][j] != '.':
                        return True
                    i += 1
                    j -= 1
        return False

    def isBlockedShooting(self, move, state):
        shoot_from_x = move[1][0]
        shoot_from_y = move[1][1]
        shoot_to_x = move[2][0]
        shoot_to_y = move[2][1]
        last_from_x = move[0][0]
        last_from_y = move[0][1]
        # Check block when shooting
        # Horizontal aligned
        if shoot_from_x == shoot_to_x:
            if shoot_from_y < shoot_to_y:
                for i in range(shoot_from_y + 1, shoot_to_y):
                    if state[shoot_from_x][i] != '.' and (shoot_from_x != last_from_x or i != last_from_y):
                        return True
            else:
                for i in range(shoot_to_y + 1, shoot_from_y):
                    if state[shoot_from_x][i] != '.' and (shoot_from_x != last_from_x or i != last_from_y):
                        return True
        # Vertical aligned
        elif shoot_from_y == shoot_to_y:
            if shoot_from_x < shoot_to_x:
                for i in range(shoot_from_x + 1, shoot_to_x):
                    if state[i][shoot_from_y] != '.' and (i != last_from_x or shoot_from_y != last_from_y):
                        return True
            else:
                for i in range(shoot_to_x + 1, shoot_from_x):
                    if state[i][shoot_from_y] != '.' and (i != last_from_x or shoot_from_y != last_from_y):
                        return True
        # Diagonally aligned
        elif abs(shoot_from_x - shoot_to_x) == abs(shoot_from_y - shoot_to_y):
            # Bottom right
            if shoot_to_x < shoot_from_x and shoot_to_y > shoot_from_y:
                i = shoot_from_x - 1
                j = shoot_from_y + 1
                while i > shoot_to_x and j < shoot_to_y:
                    if state[i][j] != '.' and (i != last_from_x or j != last_from_y):
                        return True
                    i -= 1
                    j += 1
            # Top right
            elif shoot_to_x > shoot_from_x and shoot_to_y > shoot_from_y:
                i = shoot_from_x + 1
                j = shoot_from_y + 1
                while i < shoot_to_x and j < shoot_to_y:
                    if state[i][j] != '.' and (i != last_from_x or j != last_from_y):
                        return True
                    i += 1
                    j += 1
            # Bottom left
            elif shoot_to_x < shoot_from_x and shoot_to_y < shoot_from_y:
                i = shoot_from_x - 1
                j = shoot_from_y - 1
                while i > shoot_to_x and j > shoot_to_y:
                    if state[i][j] != '.' and (i != last_from_x or j != last_from_y):
                        return True
                    i -= 1
                    j -= 1
            # Top left
            elif shoot_to_x > shoot_from_x and shoot_to_y < shoot_from_y:
                i = shoot_from_x + 1
                j = shoot_from_y - 1
                while i < shoot_to_x and j > shoot_to_y:
                    if state[i][j] != '.' and (i != last_from_x or j != last_from_y):
                        return True
                    i += 1
                    j -= 1
