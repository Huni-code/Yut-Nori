import random
from guizero import App, Box, Drawing, Text, PushButton

class YutNori:
    def __init__(self):
        """This function is the default initialization of the Yut Nori game app.
        It sets up the following: game window, game baord, control box, and game state.
        Parameters
        ----------
        None

        Returns
        -------
        None

        Side Effects
        ------------
        -Create guizero app window
        -Initiate YutNori board and control box
        -game state
        -default setting before starting game
        
        """
        self.app = App(title="Yut Nori Game", width=1000, height=600, layout="grid")
        self.app.bg = "#d2b48c" #set the color

        # Create the control panel on the left
        control_box = Box(self.app, width=300, height=600, grid=[0, 0])
        control_box.bg = "#fefbd8"

        # Create the board area on the RIGHT
        board_box = Box(self.app, width=700, height=600, grid=[1, 0])
        board_box.bg = "#f0f0f0"

        # Create the drawing background for the board
        self.board = Drawing(board_box, width=700, height=600)
        #calls the board_click function when the board is clicked
        self.board.when_clicked = self.board_click
        # Add basic controls
        title = Text(control_box, text="Yut Nori", size=20, font="Arial Bold")
        welcome_text = Text(control_box, text="Welcome to Yut Nori!",size=20, font="Arial Bold")
       
        # Store the roll result text widget as an instance variable so we can update it
        self.roll_result = Text(control_box, text="Roll: ")
        
        # Connect the roll button to the roll method
        roll_button = PushButton(control_box, text="Roll Yut Sticks", command=self.roll)
        
        self.current_player=1 #start with player 1
        self.remaining_chess={1:3, 2:3} #each players start with 3 chess
        self.chess= {1:[],2:[]} #stores player's chess
        self.completed_chess = {1:0, 2:0} #stores the number of chess that completed reaching the goal
        self.last_roll_value = 0 #store the last roll value
        self.selected_piece = None #stores the clicked chess
        self.ended_center= False #It will become true if chess is at center
        
        self.custom_paths = { # the gameplay had errors when using shortcuts. So I defined direction for every position in shortcut
            6: [24, 25, 21, 29, 28, 16 , 17, 18, 19, 20, 1],
            11: [26, 27, 21, 23, 22, 1],
            21: {"end_turn": [23,22,1],
                 "continue": [29,28,16,17,18,19,20,1]},
            24: [25, 21, 29, 28, 16, 17, 18, 19, 20, 1],
            25: [21, 29, 28, 16, 17, 18, 19, 20, 1],
            26: [27, 21, 23, 22, 1],
            27: [21, 23, 22, 1],
            28: [16, 17, 18, 19, 20, 1],
            29: [28, 16, 17, 18, 19, 20, 1],
            23: [22, 1],
            22: [1]
            }
        playerbox= Box(control_box, width=300, height=100)
        self.player1_text = Text(playerbox, text=f"Player 1 (Blue): {self.remaining_chess[1]} chess left. \n", color="blue")
        self.player2_text = Text(playerbox, text=f"Player 2 (Red): {self.remaining_chess[2]} chess left \n", color="red")
        
        start_button= PushButton(control_box, text= "Start a New chess", command=self.start_new_piece)
        self.current_player_text = Text(control_box, text=f"Current Turn: Player {self.current_player}", size=14, font="Arial Bold")
        
        self.selected_piece_text = Text(control_box, text = "No piece selected")
        move_button = PushButton(control_box, text="Move Selected Piece" , command=self.move_selected_piece)
        self.game_status_text = Text(control_box, text= "Status: Game in progress")
        
        self.draw_yut_board()
        self.app.display()
        print(self.positions)
        
    def draw_yut_board(self):
        """Drawing the board in detail. 
        stores numbered positions in a list.
        Parameters
        ----------
        None

        Returns
        -------
        None

        Side Effects
        ------------
        -Draw rectangles, lines, circles for the board.
        -Define center position
        -Store each position's information
        
        """
        w= 600
        h= 500  # Width and height of the board
        m = 70  # Margin from the edges
       
        # Initialize a list to store all position data
        self.positions = []
       
        self.board.rectangle(m, m, w-m, h-m, color="#e8d0aa", outline=True)
       
        # Draw the diagonal lines across the board
        self.board.line(m, m, w-m, h-m, color="black")  # Top-left to bottom-right
        self.board.line(m, h-m, w-m, m, color="black")  # Bottom-left to top-right
       
        # 5 positions on each side (not including corners)
        # Create positions with correct numbering (1-20), and store values
        position_coords = []
       
        # positions 1-5
        for i in range(5):
            x = w - m 
            y = h - m - i * 70  
            position_number = i + 1
            position_coords.append((x, y, position_number))

        # positions 6-10
        for i in range(5):
            x = w - m - i * 90  
            y = m  
            position_number = i + 6
            position_coords.append((x, y, position_number))

        # positions 11-15
        for i in range(5):
            x = m 
            y = m + i * 70  
            position_number = i + 11
            position_coords.append((x, y, position_number))

        # positions 16-20
        for i in range(5):
            x = m + i * 90  
            y = h - m 
            position_number = i + 16
            position_coords.append((x, y, position_number))
       
        # Draw all positions with circles
        for x, y, num in position_coords:
            self.board.oval(x-12, y-12, x+12, y+12, color="white", outline=True)
            self.board.text(x, y, text=str(num), color="black")
            self.positions.append({"id": num, "x": x, "y": y, "type": "outer"})
       
        # With the stored values, draw connecting lines between positions
        for i in range(19):
            start = self.positions[i]
            end = self.positions[i + 1]
            self.board.line(start["x"], start["y"], end["x"], end["y"], color="black")
       
        # Connect the last position back to the first to complete the circuit
        start = self.positions[19]  # Position 20
        end = self.positions[0]     # Position 1
        self.board.line(start["x"], start["y"], end["x"], end["y"], color="black")
       
        # Draw the center position
        center_x= w/2
        center_y = h/2
        self.board.oval(center_x-15, center_y-15, center_x+15, center_y+15, color="yellow", outline=True)
        self.board.text(center_x-5, center_y-8, text="C", color="black", size=14)
        self.positions.append({"id": 21, "x": center_x, "y": center_y, "type": "center"})
    
        self.add_shortcuts() #call this function for drawing shortcuts
        
    def add_shortcuts(self):
        """Add shortcut positions between corners and the center of the game board.

        Creates additional positions that provide alternative movement paths.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Side Effects
        ------------
        - Adds shortcut positions to self.positions
        - Draws orange-colored oval markers for shortcut positions
        """
        corner_positions = [ #initialize corner positions for drawing
            self.positions[0],   
            self.positions[5],   
            self.positions[10],  
            self.positions[15]   
        ]
        
        # center id is 21.
        center_pos = self.positions[-1]
        
        # add 2 positions in between center and corners
        shortcut_id = 22
        for corner_pos in corner_positions:
    
            # first shortcut location between corner and mid point
            mid1_x = corner_pos["x"] * (2/3) + center_pos["x"] * (1/3)
            mid1_y = corner_pos["y"] * (2/3) + center_pos["y"] * (1/3)
            
            # second shortcut location between corner and mid point
            mid2_x = corner_pos["x"] * (1/3) + center_pos["x"] * (2/3)
            mid2_y = corner_pos["y"] * (1/3) + center_pos["y"] * (2/3)
            
            self.board.oval(mid1_x-10, mid1_y-10, mid1_x+10, mid1_y+10, color="orange", outline=True)
            self.board.text(mid1_x, mid1_y, text=str(shortcut_id), color="black")
            
            # all positions are stored in the positions dictionary
            self.positions.append({
                "id": shortcut_id, 
                "x": mid1_x, 
                "y": mid1_y, 
                "type": "shortcut", 
                "from": corner_pos["id"]
            })
            
            shortcut_id += 1
            
            # first shortcut location between corner and mid point
            self.board.oval(mid2_x-10, mid2_y-10, mid2_x+10, mid2_y+10, color="orange", outline=True)
            self.board.text(mid2_x, mid2_y, text=(shortcut_id), color="black")
            
            # store position's information in dict
            self.positions.append({
                "id": shortcut_id, 
                "x": mid2_x, 
                "y": mid2_y, 
                "type": "shortcut", 
                "from": corner_pos["id"]
            })
            
            shortcut_id += 1
            
    def get_position_id(self, position):
        """This returns 'id' of a position for sorting purposes which is important.

        Parameters
        ----------
        position : dict
            Dictionary to represent the position of the board

        Returns
        -------
        number of the 'id' of the given position
        """
        return position["id"]
       
    def roll(self):
        """ function to roll the sticks to get the value of the movement.
            Randomly rolls 4 sticks and gives the result.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Side Effects
        ------------
        - Updates self.roll_result with roll text
        - Sets self.last_roll_value to the calculated movement value
        """
        count = 0
        rolls = []
        for sticks in range(4):
            yutroll = random.randint(0, 1) # there is only 2 possibility in yut: front or back. This is expressed in 0 and 1. We throw 4 yut
            count += yutroll
            rolls.append(yutroll)
           
        result_name = ""
        result_value = 0
       
        if count == 0:
            result_name = "Mo: 모"
            result_value = 5
        elif count == 1:
            result_name = "Do: 도"
            result_value = 1
        elif count == 2:
            result_name = "Gae: 개"
            result_value = 2
        elif count == 3:
            result_name = "Gul: 걸"
            result_value = 3
        elif count == 4:
            result_name = "Yut: 윷"
            result_value = 4
       
        text_result = f"Rolled Result: {result_name} Move: {result_value}"
        self.roll_result.value = text_result #update UI with the result and store the result for the movement
        
        self.last_roll_value = result_value
        
    def check_win(self):
        """ This checks if a player won the game or not. 

        Parameters
        ----------
        None

        Returns
        -------
        bool
            True if a player has won, False otherwise

        Side Effects
        ------------
        - Updates game status text if a player wins, and game stops.
        """   
        for player in [1,2]:
            if self.completed_chess[player] == 3:
                self.game_status_text.value = f"Player {player} wins!"
                return True
        return False
    
    def start_new_piece(self):
        """This palces a new chess piece on the board, and it has the logic of adding a new piece from the last roll result.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Side Effects
        ------------
        - Adds a new chess piece
        - Update remaining chess pieces
        - Draws the chess
        - Switches player turn
        """
            
        if self.remaining_chess[self.current_player] > 0 and self.last_roll_value > 0: # Check if the current player has remaining pieces and yut is rolled.
            piece_id = len(self.chess[self.current_player]) + 1
            new_position = 2  # Starting position is at 2

            new_position += self.last_roll_value - 1  # from the rolled value, new position is adjusted. -1 because 2 is the start
            
            # If position is more than 20, adjust it
            if new_position > 20:
                new_position = new_position - 20 + 1
                
            # 1 is the final destination. If reached, chess dissapears and changes status to completed
            if new_position == 1:
                self.completed_chess[self.current_player] += 1
                new_piece = {"id": piece_id, "position": -1, "status": "completed"}
                self.chess[self.current_player].append(new_piece)
                self.roll_result.value = f"Player {self.current_player}'s chess has completed!"
            else:
                # if other position, keep in the board and update chess location
                new_piece = {"id": piece_id, "position": new_position, "status": "active"}
                self.chess[self.current_player].append(new_piece)
                self.roll_result.value = f"Player {self.current_player} placed a new piece at position {new_position}"
            
            self.remaining_chess[self.current_player] -= 1
            
            # Text update
            self.update_player_info()
            self.draw_board_with_pieces()
            
            if self.check_win():
                return
                
            # initiate for next turn
            self.last_roll_value = 0
            
            # switch to next turn
            self.switch_player()
            
    def switch_player(self):
        """This switches the turn to the other player between 1 and 2.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Side Effects
        ------------
        - Changes self.current_player
        - Updates the display of player info
        """
        self.current_player = 3 - self.current_player #switch current player between 1 and 2
        self.update_player_info()
        
    def update_player_info(self):
        """updated display for each players and refreshes it

        Parameters
        ----------
        None

        Returns
        -------
        None

        Side Effects
        ------------
        - Updates player text widgets
        - Changes current player text
        """
        self.player1_text.value = f"Player1 (Blue): {self.remaining_chess[1]} chess left"
        self.player2_text.value = f"Player 2 (Red): {self.remaining_chess[2]} chess left"
        self.current_player_text.value = f"Current Turn: Player {self.current_player}"
        
    def board_click(self, event):
        """guizero supports "when_clicked", events function to detect click in the GUI.
            this selects a piece when clicked within the range of radius.

        Parameters
        ----------
        event : GuiZero event
            detects mouse click, and returns containing x and y coordinates

        Returns
        -------
        None

        Side Effects
        ------------
        - Selects or deselects a chess piece
        - Updates selected piece text
        - Redraws the board
        """
        x = event.x # get the x and y coordinates of the mouse click
        y = event.y
        radius = 15

        for pos in self.positions:
            # Loop all positions and checking the mouse click within the radius. If within 15, it will detect it
            if (pos["x"] - radius <= x <= pos["x"] + radius) and (pos["y"] - radius <= y <= pos["y"] + radius):
                
                for piece in self.chess[self.current_player]: #when found, check if player's piece is at that position
                    if piece["position"] == pos["id"]:
                        self.selected_piece = (self.current_player, piece["id"]) # Set the selected piece to be the current player and the ID of the clicked piece
                        self.selected_piece_text.value = f"Selected: Player {self.current_player}, Piece {piece['id']}"
                        self.draw_board_with_pieces() # Redraw the board to visually highlight the selected piece
                        return

        self.selected_piece = None # go back to the default setting
        self.selected_piece_text.value = "No piece selected"
        self.draw_board_with_pieces()
        
    def draw_board_with_pieces(self):
        """Draw the game board with chess piece positions. Clears the board and redraws as pieces move.
        A bigger yellow circle is drawn when it is clicked to make user see that it is clicked.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Side Effects
        ------------
        - Clears the board
        - Redraws the board and all chess pieces
        - Highlights selected piece
        """
        self.board.clear()
        self.draw_yut_board()
        
        for piece in self.chess[1]:
            pos_id = piece["position"]
            if pos_id > 0: #draw it only if it's on the board
                for pos in self.positions:
                    if pos["id"] == pos_id: #when position ID matches the board position
                        x = pos["x"]
                        y= pos["y"]
                        
                        if self.selected_piece and self.selected_piece[0] == 1 and self.selected_piece[1] == piece["id"]: #check if it is the selected piece
                            self.board.oval(x-23, y-23, x+23, y+23, color = "yellow", outline=True) # draw a larger yellow circle to highlight
                        self.board.oval(x-15, y-15, x+15, y+15, color="blue", outline=True)
                        self.board.text(x, y, text= piece["id"], color="white", size=10) #specificy chess id with visualization
                        break #when position is found/drawn, end loop
                    
        for piece in self.chess[2]: #same with player 2
            pos_id = piece["position"]
            if pos_id > 0:
                for pos in self.positions:
                    if pos["id"] == pos_id:
                        x = pos["x"]
                        y= pos["y"]
                        if self.selected_piece and self.selected_piece[0] == 2 and self.selected_piece[1] == piece["id"]:
                            self.board.oval(x-23, y-23, x+23, y+23, color = "yellow", outline=True)
                        self.board.oval(x-15, y-15, x+15, y+15, color="red", outline=True)
                        self.board.text(x, y, text= piece["id"], color="white", size=10)
                        break
                    
    def get_next_position(self, current_position, steps):
        """Calculate the next position for a chess piece.

        Handles special movement paths and board navigation.

        Parameters
        ----------
        current_position : int
            The current position of the chess piece
        steps : int
            Number of steps to move

        Returns
        -------
        int
            The next position after moving the specified steps
        """
        # Special path logic for positions 6, 11, and 21. First check if position is in the custom_path.
        if current_position in self.custom_paths:
            if current_position == 21:
                # Position 21 has different paths depending on if turn ends specifically at 21
                if steps == 0:  # Turn ends at 21
                    path = self.custom_paths[21]["end_turn"] # Get the "end_turn" path from the custom paths for position 21 (at __init__)
                    return path[0]  # Return the first position in the "end_turn" path (which is 23)
                else:  # Turn continues
                    if self.ended_center:
                        path =self.custom_paths[21]["end_turn"]
                        if steps <= len(path):  # If the remaining steps are within the length of this path
                            return path[steps-1]  # return the position at (steps - 1) index of the custom path
                        else:
                            return 1 # Return to the finish line (position 1)
                    else:
                        path = self.custom_paths[21]["continue"] # Use the "continue" path for moving from the center
                        if steps <= len(path):
                            return path[steps - 1]
                        else:
                            return 1
            else:
                # Other special positions (6, 11)
                path = self.custom_paths[current_position] # Get the custom path for the current position
                if steps <= len(path):
                    return path[steps - 1]
                else:
                    return 1
        else:# Moving along the normal track (positions 1-20)
            new_position = current_position + steps
            if new_position > 20:  # If past position 20, wrap around to position 1
                new_position = new_position - 20
                    
            return new_position
                
    def move_selected_piece(self):
        """Move the chess based on the roll result, and switch turn.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Side Effects
        ------------
        - Moves the selected chess piece
        - Updates piece position
        - Switches player turn
        - Checks for game win requirement
        """
        #check is the chess is selected
        if not self.selected_piece:
            self.roll_result.value = "please select the chess to move!"
            return
        if self.last_roll_value <=0: #checck if yut is rolled
            self.roll_result.value = "please roll the Yut to move!"
            return
        
        player, piece_id =self.selected_piece
        
        for i, piece in enumerate(self.chess[player]): # loop through the pieces of the current player to find the selected piece.
            if piece["id"] == piece_id:
                current_position = piece["position"] # Get the current position of the piece
                
                new_position = self.get_next_position(current_position, self.last_roll_value) # Calculate the new position based on the current position and the roll value.
                
                if new_position==1: #if goal reached, change status to completed and update the info
                    self.completed_chess[player] +=1 # Update completed chess count
                    piece["position"] =-1 # Mark the piece as completed
                    piece["status"] = "completed"
                    self.roll_result.value = f"Player {player}'s chesss {piece_id} has reached the goal!"
                else: # If the goal is not reached, update the piece's position to the new position.
                    piece["position"] = new_position
                    self.roll_result.value = f"Player {player}'s chess moved from {current_position} to {new_position} !"
                self.last_roll_value = 0
                
                self.selected_piece = None #reset
                self.selected_piece_text.value = "No piece selected"
                
                self.ended_center = (new_position == 21)  # Check if piece ended at the center
                self.update_player_info()
                self.draw_board_with_pieces()
                
                if self.check_win(): #check fist if player is valid for the win
                    return
                
                self.switch_player() # if not, switch player
                break
            
if __name__ == "__main__": #https://builtin.com/articles/name-python#:~:text=The%20%E2%80%9Cif%20__%20name%20__,the%20name%20of%20the%20module.
    game = YutNori()