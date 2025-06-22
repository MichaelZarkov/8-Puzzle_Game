import copy
import itertools
import pickle
import random

from sliding_puzzle import SlidingPuzzleGame

class QLearning:

    def __init__(self, learning_rate, discount_factor, generations, max_steps, exploration_probability):
        self.learning_rate = learning_rate # Must be 0 < lr <= 1
        self.discount_factor = discount_factor # Must be 0 <= df <= 1. The higher the number, the more valuable future rewards are.
        self.generations = generations # Number of games to play when training.
        self.max_steps = max_steps # Max steps in a game before it is reset.
        self.exploration_probability = exploration_probability # Must be 0 < ef <= 1. Probability of choosing exploration over exploitation.

        self.table = None # The resulting state-action map from the trained q-table.

    @staticmethod
    def _generate_q_table():
        """
        Generates a dictionary with keys all possible reachable states of the board and values the possible directions you can "move the hole" (up, right, down, left).
        The keys are numbers derived from the board state. For example if we have the board:
            3 2 1
            5 4 6
            7 0 8
        the associated key(number) is 321546708.

        The possible actions depend on the position of the hole (represented by 0).
        If we have the hole right in the middle, the actions we can take are 4: "move the hole up/right/down/left".
        If we have the hole at top left corner the actions are 2: "move the hole right/down".
        """

        # Possible actions according to the position of the hole.
        possible_actions = {
            0: { 'r': 0, 'd': 0 },
            1: { 'r': 0, 'd': 0, 'l': 0 },
            2: { 'd': 0, 'l': 0 },
            3: { 'u': 0, 'r': 0, 'd': 0 },
            4: { 'u': 0, 'r': 0, 'd': 0, 'l': 0 },
            5: { 'u': 0, 'd': 0, 'l': 0 },
            6: { 'u': 0, 'r': 0 },
            7: { 'u': 0, 'r': 0, 'l': 0 },
            8: { 'u': 0, 'l': 0 }
        }
        
        # Go through each position the hole can be in (9 in total).
        # Go through all permutations of the other tiles.
        # Make an entry in the dictionary with the possible actions we can take to move the hole.
        q_table = {}
        for i in range(0, 9):
            for p in itertools.permutations([1,2,3,4,5,6,7,8]):
                # Put the hole on the board.
                board = p[0:i] + (0,) + p[i:8]

                # Discard the unsolvable positions.
                if SlidingPuzzleGame.count_transpositions(board) % 2 == 1:
                    continue

                key = QLearning.convert_to_number(board)
                value = copy.deepcopy(possible_actions[i])

                q_table[key] = value

        q_table[123456780] = {} # This is the final state. The puzzle is solved so no more actions are needed.

        return q_table

    @staticmethod
    def convert_to_number(board):
        result = 0
        for n in board:
            result *= 10
            result += n
        return result

    @staticmethod
    def _choose_rand_action(action_dict):
        """
        Returns a random action and its q-value as a tuple (action, value).
        """
        action = random.choice(list(action_dict.keys()))
        return action, action_dict[action]

    @staticmethod
    def _find_best_action(action_dict):
        """
        Returns the action with the highest q-value and its q-value as a tuple (action, value).
        """
        best_action = (None, float('-inf'))
        for action in action_dict:
            if action_dict[action] > best_action[1]:
                best_action = action, action_dict[action]
        return best_action

    @staticmethod
    def _get_simple_table(q_table):
        """
        Returns a state-action map.
        Takes in a q_table and returns a dictionary with keys all possible(reachable) board
        arrangements as numbers and the best action to take according to the given q_table.
        The best action is represented as movement of the hole up/right/down/left.
        """
        simple_table = {}
        for key in q_table:
            simple_table[key] = QLearning._find_best_action(q_table[key])[0]

        return simple_table

    def train(self):
        q_table = self._generate_q_table()
        puzzle = SlidingPuzzleGame()

        # Play the game this many times.
        for gen in range(1, self.generations + 1):
            puzzle.shuffle()
            if puzzle.is_solved(): continue

            # Reset games longer than given max.
            for _ in range(0, self.max_steps):
                current_state = q_table[self.convert_to_number(puzzle.board)]

                # Choose action - explore or exploit.
                explore_or_exploit = random.random()
                if explore_or_exploit < self.exploration_probability:
                    action = self._choose_rand_action(current_state)
                else:
                    action = self._find_best_action(current_state)

                # Take action.
                puzzle.move_hole(action[0])

                # Set reward.
                is_solved = puzzle.is_solved()
                if is_solved:
                    reward = 1
                    next_best_action_value = 0 # This is the final state. No actions can be taken.
                else:
                    reward = 0
                    next_best_action_value = self._find_best_action(q_table[self.convert_to_number(puzzle.board)])[1]

                # Update Q-table.
                current_state[action[0]] = (1 - self.learning_rate) * current_state[action[0]] + self.learning_rate * (reward + self.discount_factor * next_best_action_value)

                # Maybe can do this better and not check 2 times if the puzzle is solved.
                if is_solved: break

            if gen % 10000 == 0:
                print(f'{gen} generations completed.')
        
        self.table = self._get_simple_table(q_table)
                
    def test(self):
        """
        Goes through all possible(reachable) board arrangements, checks how many steps each of them takes to solve 
        and returns the arrangement which took the most steps along with the number of steps it took.
        """
        if self.table is None:
            raise ValueError('The table is not initialized yet! Train the agent first.')

        hardest_board_state = None
        most_moves = -1
        puzzle = SlidingPuzzleGame()
        for curr_start_board in itertools.permutations([0,1,2,3,4,5,6,7,8]):
            if SlidingPuzzleGame.count_transpositions(curr_start_board) % 2 == 1: continue
            
            puzzle.board = list(curr_start_board)

            # Solve.
            move_count = 0
            for i in range(0, 200): # Stop if a game takes more than 200 moves.
                if puzzle.is_solved(): break

                puzzle.move_hole(self.table[self.convert_to_number(puzzle.board)])
                move_count += 1

            if move_count > most_moves:
                most_moves = move_count
                hardest_board_state = list(curr_start_board)
        
        return hardest_board_state, most_moves

    def save(self, file_name):
        """
        Save the state-action map to a file.
        It is not mandatory but it's best to use the '.pkl' extension because we are saving in this format.
        Raises an exception if the file already exists.
        """
        if self.table is None:
            raise ValueError('The table is not initialized yet! Train the agent first.')
        
        with open(file_name, 'xb') as f:
            pickle.dump(self.table, f) # Save the dictionary in binary format.

