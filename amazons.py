
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
        result = [(0,3),(5,3),(8,6)] # example move in wikipedia
        return result

    def isValidMove(self, move, state):
        from_x = move[0][0]
        from_y = move[0][1]
        to_x = move[1][0]
        to_y = move[1][1]
        shot_x = move[2][0]
        shot_y = move[2][1]
        if to_x < 0 or to_x > 10 or to_y < 0 or to_y > 10 or shot_x < 0 or shot_x > 10 or shot_y < 0 or shot_x > 10:
            return false
        if state[to_x][to_y] != '.' or state[shot_x][shot_y] != '.':
            return false
        if abs(to_x - from_x) != abs(to_y - from_y) and to_x != from_x and to_y != from_y:
            return false
        if abs(shot_x - to_x) != abs(shot_y - to_y) and shot_x != to_x and shot_y != to_y:
            return false
        return true
