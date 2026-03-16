# Korean Traditional Board Game: Yut Nori (윷놀이)

**Sunghun Kim** | Calvin University | April 2025

![Yut Nori Board](Board%20picture)

---

## Novelty

This project implements the Korean traditional board game Yut Nori as a digital game using Python's guizero library. It makes the game accessible to people who do not have physical game components (board, pieces and sticks). I have incorporated special logic of the game such as taking shortcut paths, rolling yut and movement function of the pieces.

The Graphical User Interface visualizes the same framework used in Korea: a visual board with numbered positions pieces can move to, roll results, player moves, piece locations and player status updates. This is an entertaining game designed to offer an engaging way for any users to learn about Korean culture through interactive gameplay. Through providing clear instructions in the game interface, it introduces the game's rules and logic to those who may be unfamiliar.

---

## Goals

The goal of this project is to create a digital board game of Yut Nori that functions the traditional logic while leveraging the digital advantage. The objectives are:

1. Implement the game logic and rules including moving pieces, taking shortcuts and win conditions (all pieces reaching the goal position).
2. Create user friendly GUI to visualize the board, pieces, and control elements.
3. Provide interface to users with comprehensive but easy game instructions for those who are new to this game.
4. Implement rolling Yut sticks method with appropriate probabilities and outcomes of the roll (Do, Gae, Geol, Yut, Mo).
5. Create visual highlights for the selected pieces for a better gameplay experience.
6. Update on the interface that displays player's status (rolled result, remaining pieces, current turn).
7. Create interactive control buttons to move selected pieces, start pieces and roll Yut sticks.

---

## Data and Python Data Types

This game utilizes numerous Python data types to run the game logic and manage game state.

**Dictionaries** — The most important part of the game, used to store the position of locations and pieces. Each position of the board is stored in a dictionary with keys of id, x/y coordinates and type (shortcut, outer). Custom paths for shortcuts are also stored in a dictionary where keys are positions and values are lists of positions the piece has to follow in order. Furthermore, player's pieces, remaining pieces and completed pieces information are stored in dictionaries to change the game's state and data as the game is played.

**Lists** — Many functions use dictionaries and lists together, and lists are often stored in dictionaries. It stores data of rolled four sticks, each position of the board, each player's pieces (active, completed piece) and shortcut list to represent sequence of positions for special paths.

**Integers** — Used to track the game state including remaining pieces, completed pieces, rolled values and current player.

**Strings** — Used for display purposes on the interface such as instructions and game state.

**Tuples** — Used to store the information of the user's selected piece (player1/2, piece id). In functions of drawing the board and pieces, it uses coordinate pairs (x, y) to calculate or check the position. The click detects exact x and y coordinates through tuple's event object to match the click location and piece. During player clicks, the event handler captures coordinate tuples, which the code then compares against piece positions using radius-based calculations to determine which game element was selected.

**Booleans** — Used to return true or false if the player won, and setting None for selected_piece to keep the default setting.

---

## Algorithm Design

The main challenge was connecting visualization and game logic functions working correctly together. This section introduces several core algorithms of the game.

### Board Drawing
When drawing the board and positions at the start, the algorithm stores each position's unique id, coordinates and type. This is one of the main core data that the algorithm uses to draw pieces, move pieces, select pieces, define shortcuts, etc.

### Piece Movement
The piece movement algorithm calculates each piece's movement based on the current position, start position (starting new piece) and roll value. For normal paths without taking shortcuts, it simply adds the position number along with the rolled value (positions 2 to 20). For shortcuts, it follows the paths defined in the `custom_paths` dictionary that stores starting positions to sequences of subsequent positions. When a piece's turn ends at a specific position (starting with 6 and 11), the movement follows the predefined paths. Every time movements are made, the board is cleared and pieces are redrawn on a new position. Each player's pieces are drawn in different colors to represent the player's pieces. When a player has made a move, it switches turn to the other player.

### Piece Selection
The piece selection algorithm at `board_click` function detects if the user's click is within the radius of the current position of a game piece. Location of current position is defined through using coordinates data stored in `self.positions`. When a piece is selected, it draws a bigger yellow circle behind the piece to visually highlight it, in order to apply movement to the correct piece. This imports the guizero events `when_clicked` to detect the click.

### Yut Stick Rolling
The Yut sticks rolling algorithm at `roll` function imports random to generate random probability of rolling sticks. It is simulated to produce a random number between 0 and 1 four times (which indicates four sticks rolled), and sum those values for the calculated rolled result. The result represents the number of movements players can take (Do, Gae, Gul, Yut, Mo).

### Win Condition
The win condition algorithm constantly checks each player's completed pieces. Every time a piece has reached the final goal (position 1), dictionaries of remaining pieces and completed pieces are updated. When a player's completed pieces becomes 3, the player's win conditions are met and the game ends.

---

## Program Design

| Function | Input | Output |
|----------|-------|--------|
| `__init__()` | None | Initialize game state, UI, and board |
| `draw_yut_board()` | None | Visualize board and store position data |
| `add_shortcuts()` | None | Add shortcut positions between corners and center |
| `roll()` | None | Simulate Yut stick roll and update movement value |
| `check_win()` | None | Returns Boolean — whether a player has won |
| `start_new_piece()` | None | Place a new piece on the board from rolled value |
| `switch_player()` | None | Switch player's turn and update display |
| `update_player_info()` | None | Update player status text on interface |
| `board_click(event)` | GuiZero event | Handle piece selection from user click |
| `draw_board_with_pieces()` | None | Redraw board with player's piece positions |
| `get_next_position(pos, steps)` | int, int | Returns new position after movement |
| `move_selected_piece()` | None | Move selected piece and update game state |

---

## How to Run

```bash
pip install guizero
python Kim_Sunghun_FinalProject.py
```

---

## Tech Stack

Python 3, guizero, random (standard library)
