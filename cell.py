import tkinter as tk
from PIL import Image, ImageTk


class Cell:
    def __init__(self, x, y, size, game):
        """
        Initialize a Cell object.
        :param x: X coordinate in the grid
        :param y: Y coordinate in the grid
        :param size: Size of the cell (width = height)
        :param game: Reference to the game instance
        """
        self.x = x
        self.y = y
        self.size = size        
        self.is_mined = False
        self.is_revealed = False
        self.is_flagged = False
        self.is_questionned = False
        self.is_inspected = False
        self.mines_around = 0
        self.flags_around = 0
        self.game = game
        
        # Load images for different cell states
        self.mine = ImageTk.PhotoImage(Image.open("images/mine.png"))
        self.exploded_mine = ImageTk.PhotoImage(Image.open("images/exploded-mine.png"))
        self.wrong_mine = ImageTk.PhotoImage(Image.open("images/wrong-mine.png"))
        self.neutral = ImageTk.PhotoImage(Image.open("images/neutral.png"))
        self.flagged = ImageTk.PhotoImage(Image.open("images/flag.png"))
        self.img_button = ImageTk.PhotoImage(Image.open("images/button.png"))
        self.question_mark = ImageTk.PhotoImage(Image.open("images/QM.png"))
        
        # Load number images from 1 to 8
        self.number_images = {
            i: ImageTk.PhotoImage(Image.open(f"images/{i}.png")) for i in range(1, 9)
        }

    def draw(self, parent_frame, on_right_press, on_right_release, on_left_press, on_left_release):
        """
        Draw the cell as a button in the given screen.
        :param parent_frame: Parent widget (the game grid)
        """
        button = tk.Button(
            parent_frame,
            width=self.size,
            height=self.size,
            borderwidth=0,  # Remove the border
            relief="sunken",  # Prevent click effect
            highlightthickness=0
        )
        button.grid(row=self.y, column=self.x, padx=0, pady=0)
        self.button = button  # Keep a reference to the button for later updates
        
        # Bind mouse click events
        button.bind("<ButtonPress-1>", lambda event: on_left_press(self, event))
        self.button.bind("<ButtonRelease-1>", lambda event: on_left_release(self, event))
        self.button.bind("<ButtonPress-3>", lambda event: on_right_press(self, event))
        self.button.bind("<ButtonRelease-3>", lambda event: on_right_release(self, event))
        
        button.configure(image=self.img_button)  # Show button image if not revealed
            
    def toggle_flags(self):
        """
        Toggle flag status if the cell is not revealed.
        """
        if not self.is_revealed:
            if self.game.flags_count <= self.game.mines_count:
                if not self.is_questionned and not self.is_flagged:
                    if self.game.flags_count < self.game.mines_count:
                        self.game.flags_count += 1
                        self.is_flagged = True
                elif self.is_flagged:
                    self.is_flagged = False
                    self.is_questionned = True
                    self.game.flags_count -= 1
                else:
                    self.is_questionned = False
        self.update_button()

    def reveal(self):
        """
        Reveal the cell if it's not flagged.
        :return: True if the cell contains a mine, False otherwise
        """
        if not self.is_flagged:
            self.is_revealed = True
            self.update_button()
            return self.is_mined
        return False
    
    def update_button(self):
        """
        Update the button's image after revealing the cell.
        """
        if self.is_revealed:
            if self.is_mined:
                self.button.configure(image=self.exploded_mine)
            elif self.mines_around > 0:
                self.button.configure(image=self.number_images.get(self.mines_around))
            else:
                self.button.configure(image=self.neutral)  # Neutral image when no adjacent mines
        else:
            if self.is_flagged:
                self.button.configure(image=self.flagged)
            elif self.is_questionned:
                self.button.configure(image=self.question_mark)
            elif self.is_inspected:
                self.button.configure(image=self.neutral)
            else:
                self.button.configure(image=self.img_button)
        
    def draw_game_over(self):
        """
        Update the button's image for game over state.
        """
        if self.is_mined:
            if self.is_flagged:
                self.button.configure(image=self.flagged)
            elif self.is_revealed:
                self.button.configure(image=self.exploded_mine)
            else:
                self.button.configure(image=self.mine)
        else:
            if self.is_flagged:
                self.button.configure(image=self.wrong_mine)
    
    def reset(self):
        """
        Reset the cell to its initial state.
        """
        self.is_mined = False
        self.is_revealed = False
        self.is_flagged = False
        self.is_questionned = False
        self.is_inspected = False
        self.mines_around = 0
        self.flags_around = 0
