# Korean Traditional Board Game: Yut Nori (윷놀이)

**Sunghun Kim** | Calvin University

![Yut Nori Board](Board%20picture)

---

## Overview

This project implements the Korean traditional board game **Yut Nori** as a digital game using Python's `guizero` library. It makes the game accessible to people who do not have physical game components (board, pieces and sticks).

The GUI visualizes the same framework used in Korea: a visual board with numbered positions, roll results, player moves, piece locations and player status updates. This is an entertaining game designed to offer an engaging way for any users to learn about Korean culture through interactive gameplay.

---

## How to Play

Yut Nori is a two-player board game where each player has **3 game pieces (말)**. Players take turns rolling 4 sticks and moving their pieces around the board. The first player to get all 3 pieces to the goal (Position 1) wins.

### Roll Results

| Roll | Korean | Value |
|------|:---:|:---:|
| Do | 도 | 1 step |
| Gae | 개 | 2 steps |
| Gul | 걸 | 3 steps |
| Yut | 윷 | 4 steps |
| Mo | 모 | 5 steps |

### Game Controls

1. **Roll Yut Sticks** — Roll to get your movement value
2. **Start a New Piece** — Place a new piece on the board using the roll value
3. **Click a piece** on the board to select it (highlighted in yellow)
4. **Move Selected Piece** — Move the selected piece by the rolled value

---

## Features

- **Visual Board** with 20 outer positions, 8 shortcut positions, and a center point
- **Shortcut Paths** — Pieces landing on corner positions (6, 11) can take diagonal shortcuts through the center
- **Piece Selection** — Click detection with radius-based matching and yellow highlight for selected pieces
- **Turn-based Gameplay** — Automatic turn switching between Player 1 (Blue) and Player 2 (Red)
- **Win Detection** — Game ends when a player gets all 3 pieces to the goal

---

## Algorithm Design

### Board Drawing
Each position stores a unique ID, x/y coordinates, and type (outer, center, shortcut). This core data drives piece drawing, movement, selection, and shortcut definitions.

### Piece Movement
For normal paths (positions 2–20), the algorithm adds the roll value to the current position. For shortcuts, it follows predefined paths stored in a `custom_paths` dictionary. Positions 6 and 11 trigger shortcut entries, and position 21 (center) has branching logic depending on whether the piece's turn ends there.

### Piece Selection
The `board_click` function uses guizero's `when_clicked` event to detect clicks within a 15-pixel radius of each position. When matched to a player's piece, it highlights the selection with a larger yellow circle.

### Yut Stick Rolling
The `roll` function uses `random.randint(0, 1)` four times to simulate flipping 4 sticks. The sum determines the roll result (0 = Mo, 1 = Do, 2 = Gae, 3 = Gul, 4 = Yut).

### Win Condition
Every time a piece reaches position 1 (goal), the completed pieces counter increments. When a player reaches 3 completed pieces, the game ends.

---

## Data Types Used

| Type | Usage |
|------|-------|
| **Dictionaries** | Board positions (id, x/y, type), custom shortcut paths, player pieces, game state tracking |
| **Lists** | Rolled stick values, position sequences, player piece collections |
| **Integers** | Remaining pieces, completed pieces, roll values, current player |
| **Strings** | UI display text (instructions, status updates) |
| **Tuples** | Selected piece info (player, piece_id), coordinate pairs for click detection |
| **Booleans** | Win condition checks, center position tracking |

---

## Program Design

| Function | Input | Output |
|----------|-------|--------|
| `__init__()` | None | Initialize game state, UI, and board |
| `draw_yut_board()` | None | Visualize board and store position data |
| `add_shortcuts()` | None | Add shortcut positions between corners and center |
| `roll()` | None | Simulate Yut stick roll and update movement value |
| `check_win()` | None | Returns `True` if a player has won |
| `start_new_piece()` | None | Place a new piece on the board |
| `switch_player()` | None | Switch turn between players |
| `update_player_info()` | None | Refresh player status display |
| `board_click(event)` | GuiZero event | Handle piece selection from click |
| `draw_board_with_pieces()` | None | Redraw board with current piece positions |
| `get_next_position(pos, steps)` | int, int | Returns new position after movement |
| `move_selected_piece()` | None | Move selected piece and update game state |

---

## Tech Stack

- Python 3
- guizero (GUI framework)
- random (standard library)

## How to Run

```bash
pip install guizero
python Kim_Sunghun_FinalProject.py
```
