# Project Documentation


## Game Scripts

The following scripts are needed to play the game.
- `button.py`
- `counter.py`
- `game_constants.py`
- `game.py`
- `play.py`
- `sliding_puzzle.py`
- `solver.py`
- `start_menu.py`

### ***button.py***

---

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

- `check_btn_press(point) -> bool` - checks if `point` is inside of the button.
- `draw() -> None` - draws the button on `screen`.
- `erase(color) -> None` - fills the button with the given color. Color is RGB triplet (0-255, 0-255, 0-255).

### ***counter.py***

---

`class Counter` - GUI counter.

`Counter(screen, center) -> Counter`

- `screen` - *Pygame surface* to draw on.
- `center` - position of the center of the containing rectangle.

**Methods**

- `draw() -> None` - draws the value of the counter on `screen`.
- `erase() -> None` - fills the containing rectangle of the text with `BACKGROUND_COLOR` from `game_constants.py`.
- `increment() -> None` - erases the counter; increments it; draws it on `screen`.
- `zero() -> None` - erases the counter; sets it to 0; draws it on `screen`.

### ***play.py***

---

Stars the game.

### ***sliding_puzzle.py***

---

`class SlidingPuzzleGame` - puzzle logic

`SlidingPuzzleGame() -> SlidingPuzzleGame`

The puzzle is represented with a list of the numbers from 0 to 8 where 0 is considered the empty spot (the hole). The firs, second and third triples of elements are the first, second and third rows respectively. For example the **final position (solved position)**:

<p align='center'>
  <img src='media\8-puzzle_solved_board.png' width='180'>
</p>

is be represented as `[1,2,3,4,5,6,7,8,0]`.

**Methods**

- `count_transpositions(board) -> number` - `@staticmethod`, takes a list with the numbers 0 to 8 and returns the transposition count **of the numbers 1 to 8**. The result is used to check wether a tile arrangement is solvable (i.e. if the final position `[1,2,3,4,5,6,7,8,0]` can be reached only through sliding of the tiles). If the result is even the puzzle is solvable; if it is odd it cannot be solved through sliding.
- `is_solved() -> bool` - returns true if the puzzle is in the solved position.
- `move_hole(direction)` - takes a direction `'u'/'r'/'d'/'l'` and *"moves the hole"* in this direction. For example if the hole is top center and call `move_hole('down')` the center tile will slide up:
<p align='center'>
<table style='margin: 0px auto'>
  <tr>
    <th>Before call</th>
    <th>After call</th>
  </tr>
  <tr>
    <td><img src='media\8-puzzle_shuffled_board.png' width='180'></td>
  </tr>
</table>
</p>
  