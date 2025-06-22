import pickle

from q_learning import QLearning as ql

class Solver:
    def __init__(self, file_name):
        self.table = self._load(file_name)

    @staticmethod
    def _load(file_name):
        """
        Load a state-action map from file.
        """
        with open(file_name, 'rb') as f:
            return pickle.load(f)
        
    def get_action(self, puzzle):
        """
        Given a puzzle, returns an action from the state-action map.
        Actions are the four directions to move the hole: u/r/d/l.
        """
        if puzzle.is_solved():
            return None
        else:
            return self.table[ql.convert_to_number(puzzle.board)]