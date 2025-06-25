import random

class SlidingPuzzleGame:
    def __init__(self):
        # 0 is the empty spot.
        self.board = [1,2,3,4,5,6,7,8,0]
    
    @staticmethod
    def count_transpositions(board):
        """
        Returns the transpositions in 'self.board'.
        Note that the hole (the 0) is not part of the permutation.
        """

        # There might be a faster way to count the transpositions
        count = 0
        for i in range(0, 8):
            for j in range(i + 1, 9):
                if board[j] == 0: continue

                if board[i] > board[j]:
                    count += 1
        return count

    def shuffle(self):
        """
        Shuffles the tiles on the board. Always leaves the board in a solvable state, meaning that the tiles can be rearranged to
            1 2 3
            4 5 6
            7 8
        only by sliding the tiles. The above is considered the solved state.   
        """

        """
        COMPLETE EXPLANATION

        NOTATION: for brevity I will use the row by row notation like so:
            6   4
            3 2 8   will be written as 64|328|157.
            1 5 7
        The 0 is represented by a hole.

        Yes, you can order the tiles such that the puzzle is not solvable by only sliding the tiles.
        For example you cannot start with this arrangement:
            1 2 3
            4 5 6
            8 7 
        and end up in this arrangement:
            1 2 3
            4 5 6
            7 8
        only through sliding the tiles.

        Okay, but how do we determine if a position is reducible to 123|456|78 ?
        The following I have NOT proven but I think it is true.
            1. We flatten out the board row by row (just like the notation). If we have:
                1 3 4
                2   7
                5 8 6
                we represent it as the permutation 13427586. The position of the hole doesn't matter, we just go row by row.
            2. We count the transpositions in the permutation (which pairs of numbers are in the wrong order).
                - If the their count is even, then the position is reducible to 123|456|78.
                  In other words if the permutation is even, then it is reducible to our final state.
                - If it's odd then the position is NOT reducible to 123|456|78, but instead is reducible to 123|456|87.
                  In other words if the permutation is odd, then it is NOT reducible to our final state.
                In our example the transpositions are: (3,2) (4,2) (7,5) (7,6) (8,6) - 5 in total, so NOT reducible to 123|456|78.
        
        In our shuffling algorithm we can just generate a random arrangement. If the permutation is even then we return the 
        shuffled board. It it's odd we shuffle again until we end up with even permutation.
        """
        
        random.shuffle(self.board)
        while self.count_transpositions(self.board) % 2 == 1 or self.is_solved():
            random.shuffle(self.board)

    def is_solved(self):
        """
        The solved state is:
            1 2 3
            4 5 6
            7 8 
        """
        for i in range(0, 8):
            if self.board[i] != i + 1:
                return False
        return True
    
    def move_tile(self, row, col):
        """
        Moves the tile in position (row, col) to the adjacent empty spot.
        Does nothing if none of the adjacent spots are empty.
        If the tile was moved, returns the index it was moved to. Returns None otherwise.
        Throws an error for invalid row or col.
        """

        if row < 0 or 2 < row or col < 0 or 2 < col:
            raise ValueError(f'Invalid row or column! They must be 0, 1 or 2. Given: row = {row}, col = {col}.')

        return self.move_tile_by_index(row * 3 + col)
        
    def move_tile_by_index(self, i):
        """
        Moves the tile in position 'i' (index in the list) to the adjacent empty spot. Does nothing if none of the adjacent spots are empty.
        If the tile was moved, returns the index it was moved to. Returns None otherwise.
        Throws an error if index is out of bounds. 
        """

        if i < 0 or 8 < i:
            raise ValueError(f'Tile index must be 0 <= index <= 8. Given {i}.')
        
        h_i = self.board.index(0) # Index of the hole.
        
        # Check if the hole is up, right, down or left of the tile.
        if h_i == i - 3 or (h_i == i + 1 and i % 3 != 2) or h_i == i + 3 or (h_i == i - 1 and i % 3 != 0):
            self.board[h_i], self.board[i] = self.board[i], 0
            return h_i
        
        return None

    def move_hole(self, direction):
        """
        Moves the hole in the specified direction u/r/d/l (up/right/down/left).
        Returns the initial indexes of the tile and the hole.
        Throws an error if the hole cannot be move in the given direction.
        For example if the hole is in top left like so:
              1 2
            3 4 5
            6 7 8
        throws an error if 'direction' is 'u' or 'l'.
        """

        h_i = self.board.index(0) # Index of the hole.

        if direction == 'u':
            t_i = h_i - 3
            if 0 <= t_i:
                self.board[h_i], self.board[t_i] = self.board[t_i], 0
            else:
                raise ValueError(f'Hole cannot be moved up. It is in position {h_i}.')
        elif direction == 'r':
            if h_i % 3 != 2:
                t_i = h_i + 1
                self.board[h_i], self.board[t_i] = self.board[t_i], 0
            else:
                raise ValueError(f'Hole cannot be moved right. It is in position {h_i}.')
        elif direction == 'd':
            t_i = h_i + 3
            if t_i <= 8:
                self.board[h_i], self.board[t_i] = self.board[t_i], 0
            else:
                raise ValueError(f'Hole cannot be moved down. It is in position {h_i}.')
        elif direction == 'l':
            if h_i % 3 != 0:
                t_i = h_i - 1
                self.board[h_i], self.board[t_i] = self.board[t_i], 0
            else:
                raise ValueError(f'Hole cannot be moved left. It is in position {h_i}.')
        else:
            raise ValueError(f'Invalid direction for moving the hole! Valid directions are u/r/d/l. Given {direction}.')
        
        return t_i, h_i