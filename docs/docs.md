# Project Documentation

- [Project Documentation](#project-documentation)
- [Game Scripts](#game-scripts)
  - [*button.py*](#buttonpy)
      - [`check_btn_press(point) -> bool`](#check_btn_presspoint---bool)
      - [`draw() -> None`](#draw---none)
      - [`erase(color) -> None`](#erasecolor---none)
  - [*counter.py*](#counterpy)
      - [`draw() -> None`](#draw---none-1)
      - [`erase() -> None`](#erase---none)
      - [`increment() -> None`](#increment---none)
      - [`zero() -> None`](#zero---none)
  - [*game.py*](#gamepy)
  - [*game\_constants.py*](#game_constantspy)
  - [*play.py*](#playpy)
  - [*sliding\_puzzle.py*](#sliding_puzzlepy)
      - [`count_transpositions(board) -> number` `@staticmethod`](#count_transpositionsboard---number-staticmethod)
      - [`is_solved() -> bool`](#is_solved---bool)
      - [`move_hole(direction) -> (tile_index, hole_index)`](#move_holedirection---tile_index-hole_index)
      - [`move_tile(row, col) -> index`](#move_tilerow-col---index)
      - [`move_tile_by_index(i) -> index`](#move_tile_by_indexi---index)
      - [`shuffle() -> None`](#shuffle---none)
  - [*solver.py*](#solverpy)
      - [`get_action(puzzle) -> 'u'|'r'|'d'|'l'`](#get_actionpuzzle---urdl)
  - [*start\_menu.py*](#start_menupy)
      - [`draw() -> 'play'|'quit'`](#draw---playquit)
- [Q-learning Scripts](#q-learning-scripts)
  - [*q\_learning.py*](#q_learningpy)
    - [Q-algorithm](#q-algorithm)
    - [A Note on Optimality](#a-note-on-optimality)
    - [Why Choose These Learning Parameters?](#why-choose-these-learning-parameters)
      - [`convert_to_number(board) -> number` `@staticmethod`](#convert_to_numberboard---number-staticmethod)
      - [`save(file_name) -> None`](#savefile_name---none)
      - [`train() -> None`](#train---none)
      - [`test() -> list, number`](#test---list-number)
  - [*train.py*](#trainpy)

# Game Scripts

The following scripts are needed to play the game.
- [***button.py***](#buttonpy)
- [***counter.py***](#counterpy)
- [***game.py***](#gamepy)
- [***game_constants.py***](#game_constantspy)
- [***play.py***](#playpy)
- [***sliding_puzzle.py***](#sliding_puzzlepy)
- [***solver.py***](#solverpy)
- [***start_menu.py***](#start_menupy)

## *button.py*

`class Button` - a GUI button element.  

`Button(screen, width, height, text, font, center) -> Button`  
`Button(screen, width, height, text, font, bottom_left) -> Button`  
`Button(screen, width, height, text, font, bottom_right) -> Button`

- `screen` - *Pygame surface* the button will be drawn on.
- `width`, `height` - height and width of the button. All buttons have rounded corners - their short sides are semicircles.
- `text` - text to be displayed inside the button.
- `font` - *Pygame Font object* to render `text`.
- `center`, `bottom_left`, `bottom_right` - a pair of coordinates for button position on `screen`.

**Methods**

#### `check_btn_press(point) -> bool`

- Checks if `point` is inside of the button.

#### `draw() -> None`

- Draws the button on `screen`.

#### `erase(color) -> None`

- Fills the button with the given color. Color is RGB triplet (0-255, 0-255, 0-255).

## *counter.py*

`class Counter` - GUI counter.

`Counter(screen, center) -> Counter`

- `screen` - *Pygame surface* to draw on.
- `center` - position of the center of the containing rectangle.

**Methods**

#### `draw() -> None`

- Draws the value of the counter on `screen`.

#### `erase() -> None`

- Fills the containing rectangle of the text with `BACKGROUND_COLOR` from `game_constants.py`.

#### `increment() -> None`

- Erases the counter; increments it; draws it on `screen`.

#### `zero() -> None`

- Erases the counter; sets it to 0; draws it on `screen`.

## *game.py*

`class Game` - GUI of the game. Handles the game initialization and the puzzle screen.

The game starts running when you create an instance `Game()`. Loads the image from folder *imgs* and the state-action map (used by the solver) from folder *q_tables*.

## *game_constants.py*

Game constants like screen size, FPS, folder location of assets, etc.

## *play.py*

Starts the game.

## *sliding_puzzle.py*

`class SlidingPuzzleGame` - puzzle logic.

`SlidingPuzzleGame() -> SlidingPuzzleGame`

The puzzle is represented with a *Python list* of the numbers from 0 to 8 where 0 is considered the empty spot (the hole). The first, second and third triples of elements are the first, second and third rows respectively. For example the **final position (solved position)**:

<p align='center'>
  <img src='media\8-puzzle_solved_board.png' width='180'>
</p>

is be represented as `[1,2,3,4,5,6,7,8,0]`.

**Methods**

#### `count_transpositions(board) -> number` `@staticmethod`

- Takes a list with the numbers 0 to 8 and returns the transposition count **of the numbers 1 to 8**. The result is used to check wether a tile arrangement is solvable (i.e. if the final position `[1,2,3,4,5,6,7,8,0]` can be reached only through sliding of the tiles). If the result is even the puzzle is solvable; if it's odd it cannot be solved through sliding.

#### `is_solved() -> bool`

- Returns true if the puzzle is in the solved position.

#### `move_hole(direction) -> (tile_index, hole_index)`

- takes a direction `'u'|'r'|'d'|'l'` and *"moves the hole"* in this direction. For example if the hole is top center and we call `move_hole('d')`, the center tile will slide up:

<table align='center'>
  <tr>
    <th style='text-align:center'>Before call</th>
    <th style='text-align:center'>After call</th>
  </tr>
  <tr>
    <td><img src='media\8-puzzle_shuffled_board_1.png' width='180'></td>
    <td><img src='media\8-puzzle_shuffled_board_2.png' width='180'></td>
  </tr>
</table>

- Throws an error of the hole can't be moved in the direction. For example error is thrown if the hole is top center and we call `move_hole('u')`.
- Returns the index of the tile to be moved and the index of the hole before the slide. In the above example `(4, 1)` will be returned.

#### `move_tile(row, col) -> index` 

- Moves the tile in position (row, col) to the adjacent empty spot.
- Does nothing if none of the adjacent spots are empty.
- If the tile was moved, **returns the index it was moved to**. Returns None otherwise.
- Throws an error for invalid row or col.

#### `move_tile_by_index(i) -> index`

- Moves the tile in position `i` (index in the list) to the adjacent empty spot.
- Does nothing if none of the adjacent spots are empty.
- If the tile was moved, **returns the index it was moved to**. Returns None otherwise.
- Throws an error if index is out of bounds. 

#### `shuffle() -> None`

- Shuffles the tiles. The resulting board is never in the solved position.

## *solver.py*

`class Solver` - interface for the state-action map.

`Solver() -> Solver`

When created loads the state-action map from folder *q_tables*.

**Methods**

#### `get_action(puzzle) -> 'u'|'r'|'d'|'l'`

- Takes `SlidingPuzzleGame` object and returns a move (string) according to the state-action map.

## *start_menu.py*

`class StartMenu` - the game start screen.

`StartMenu(screen) -> StartMenu`

**Methods**

#### `draw() -> 'play'|'quit'`

- Draws the start menu on the `screen`. Returns `'play'` or `'quit'` string depending on the user input.

# Q-learning Scripts

The following scripts are needed to run the Q-learning algorithm:
- [***q_learning.py***](#q_learningpy)
- [***sliding_puzzle.py***](#sliding_puzzlepy)
- [***train.py***](#trainpy)

## *q_learning.py*

`class QLearning`

```
QLearning(
  learning_rate,
  discount_factor,
  generations,
  max_steps,
  exploration_probability
) -> QLearning
```

### [Q-algorithm](https://en.wikipedia.org/wiki/Q-learning#Algorithm)

This class implements the Q-learning algorithm for 8-puzzle. The 8-puzzle has $9!/2 = 181440$ possible
states (board arrangements) which are reachable from the solved position `[1,2,3,4,5,6,7,8,0]`.

The algorithm creates a Q-function:
```math
Q:  S \times A \rightarrow \mathbb{R}
```
where for every board arrangement and for every **possible** movement of the hole in this board arrangement, the function returns a number called the *Q-value of the state-action pair*. The bigger the number the better the move is considered to be.

More precisely the Q-function is represented as a *Python dictionary*, where the keys are the board arrangements converted to numbers (e.g., `[1,2,3,4,0,5,7,8,6] -> 123405786`), and the values are *dictionaries* of the form `{ 'u': number, 'r': number, 'd': number, 'l': number }` - the possible movements of the hole. The dictionary does not include impossible moves - for example, if the hole is top left, then it can only move *right* or *down*, so we have `{ 'r': number, 'd': number }`. Initially all `number`s are set to zero. They will be learned during the training.

During the training the Q-table (the dictionary) is updated according to the Q-algorithm:
```math
Q_{new}(S_i,A_i) = (1 - \lambda)\,Q_{old}(S_i,A_i) + \lambda\,(r + \alpha\,.\,max\{Q_{next}\})
```
Where:
- $Q_{new}(S_i,A_i)$ - the new value that will be assigned in the Q-table for the state $S_i$ and action $A_i$.
- $\lambda$ - the learning rate $0 < \lambda \leq 1$.
- $Q_{old}(S_i,A_i)$ - old value in the Q-table for the state $S_i$ and action $A_i$.
- $r$ - the reward given from the puzzle when we take action $A_i$ in state $S_i$.
- $\alpha$ - the discount factor $0 \leq \alpha \lt 1$. This dictates how valuable future rewards are.
- $max\{Q_{next}\}$ - the maximum possible Q-value according to the Q-table in the next state $S_{i+1}$ (the state we go to when we take action $A_i$ in state $S_i$).

In the code implementation, reward (of 1) is only given when an action that reaches the final state is chosen.

### A Note on Optimality

The Q-learning algorithm **is not the best way to solve this puzzle** both in terms of optimality and time complexity. The problem with optimality is that we don't systematically go through all possible state-action pairs. Instead Q-learning relies on *random exploration of the states*, so we cannot be absolutely sure that we found the fastest solve for every state - this has to be checked another way. A better way will be to use some sort of graph search like _A*_ or *iterative deepening*. 

If we run the algorithm with the following parameters:
```python
learning_rate=1.0,
discount_factor=0.92,
generations=2000000,
max_steps=40,
exploration_probability=1.0
```
the resulting state-action map is **optimal or almost optimal** - meaning that it solves every position close to the least possible steps. Again, we have to check if the reached solutions are optimal.

The current state-action map in the folder *q_tables* is trained on the above parameters and it is optimal or almost optimal - **on all states it takes at most 31 moves**. It is proven that the hardest to solve states take at least 31 moves, so this map is optimal at least on the hardest states.

The training with the above parameters takes about 7 minutes.

### Why Choose These Learning Parameters?

- `learning_rate=1.0` - game is deterministic so the latest info is the most correct info - we just assign it to the table.
- `discount_factor=0.92` - nice constant that doesn't run into floating point error when we raise it to the power of 31.
- `generations=2000000` - found with trial and error, seems OK.
- `max_steps=40` - an optimal game takes at most 31 moves so we reset the game around that mark (maybe exactly 31 will provide even faster learning).
- `exploration_probability=1.0` - we have a lot of states and a lot of actions to take - try to explore them all.

**Methods**

#### `convert_to_number(board) -> number` `@staticmethod`

- Converts a list of digits to a number - e.g., `[1,2,3,4,0,5,7,8,6] -> 123405786`.

#### `save(file_name) -> None`

- Saves a state-action map in the given location.
- You have to call `train()` before you call this function, in order to initialize the Q-table. Throws an error if the Q-table is not initialized.
- The state action map is a *dictionary* with keys all solvable board states as numbers an values `'u'`, `'r'`, `'d'` or `'l'` - the direction to move the hole (the best action according to the original Q-table).
- The dictionary is saved with `pickle.dump()`. You can read it back to a dictionary with `pickle.load()`.

#### `train() -> None`

- Trains the Q-table with the parameters given to the constructor.

#### `test() -> list, number`

- Goes through all solvable board states and test the Q-table.
- Returns the board which took the most steps to solve and the number of steps it took. Does not check beyond 200 steps.

## *train.py*

A script to run the Q-algorithm. Saves the resulting state-action map to *q_tables\table_1.pkl*.