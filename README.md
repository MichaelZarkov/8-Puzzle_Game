# 8-Puzzle Game

The 8-Puzzle consists of a 3x3 board and 8 tiles usually nubered 1 through 8. The goal of the puzzle is to arrange the tiles in accending order only by sliding them. The tiles may not be numbered but instead be the squares of a picture:

<p align='center'>
  <img src='docs\media\8-puzzle_solved_board.png' align='center' width='180' height='180'>
  <img src='docs\media\scrambled_picture.png' align='center' width='164' height='164'>
</p>

## Demo

Demo of the built-in puzzle solver.

<p align='center'>
  <img src='docs\media\solver_demo.gif' width='241'>
</p>

## How to Play

If you are on Windows you can just download the contents of the `exe` folder and run `8-puzzle_game.exe` - **no need to install Python**.

Alternatively you can download the folders `imgs`, `q_tables` and `src`; install the listed packages in `requirements.txt`; run the script `play.py`.

## Project Structure

- `docs` - project documentation.
- `exe` - contains the final game as a Windows executable. To play just download its contents and run `8-puzzle_game.exe` - **no need to install Python**.
- `imgs` - contains images for the GUI of the game.
- `q_tables` - contains the state-action map used by the automatic puzzle solver.
- `src` - Python source code of the game and the Q-learning algorithm (which generates a state-action map). To run the scripts you need the folders `imgs` and `q_tables`. You also need to install the Python packages listed in `requirements.txt`. `play.py` runs the game; `train.py` runs the Q-learning algorithm.

For more info check out the `docs`.