import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk


class Cell:
    def __init__(self, x, y, size):
        """
        Initialize a Cell object.
        :param x: X coordinate in the grid
        :param y: Y coordinate in the grid
        :param size: Size of the cell (width = height)
        """
        self.x = x
        self.y = y
        self.size = size        
        self.is_mined = False
        self.is_revealed = False
        self.is_flagged = False
        self.is_questionned = False
        self.mines_around = 0
        # Load images for mines and neutral (unrevealed) cells
        image = Image.open("images/mine.png")
        self.mine = ImageTk.PhotoImage(image)
        image = Image.open("images/exploded-mine.png")
        self.exploded_mine = ImageTk.PhotoImage(image)
        image = Image.open("images/wrong-mine.png")
        self.wrong_mine = ImageTk.PhotoImage(image)
        image = Image.open("images/neutral.png")
        self.neutral = ImageTk.PhotoImage(image)
        image = Image.open("images/flag.png")
        self.flagged = ImageTk.PhotoImage(image)
        image = Image.open("images/button.png")
        self.img_button = ImageTk.PhotoImage(image)
        image = Image.open("images/QM.png")
        self.question_mark = ImageTk.PhotoImage(image)
        self.number_images = {
            1: ImageTk.PhotoImage(Image.open("images/1.png")),
            2: ImageTk.PhotoImage(Image.open("images/2.png")),
            3: ImageTk.PhotoImage(Image.open("images/3.png")),
            4: ImageTk.PhotoImage(Image.open("images/4.png")),
            5: ImageTk.PhotoImage(Image.open("images/5.png")),
            6: ImageTk.PhotoImage(Image.open("images/6.png")),
            7: ImageTk.PhotoImage(Image.open("images/7.png")),
            8: ImageTk.PhotoImage(Image.open("images/8.png"))
        }

    def draw(self, app, on_click, on_right_click):
        """
        Draw the cell as a button in the given screen.
        :param screen: Parent widget (the game grid)
        """
        button = tk.Button(
            app,
            width=self.size,
            height=self.size,
            borderwidth=0,         # Supprime la bordure
            relief="sunken",         # Empêche l'effet de clic
            highlightthickness=0,  # Épaisseur du bord
            command=lambda: on_click(self)
        )
        button.grid(row=self.y, column=self.x, padx=0, pady=0)
        self.button = button  # Keep a reference to the button for later updates
        # Associer un clic droit au bouton
        self.button.bind("<Button-3>", lambda event: on_right_click(self))
        """if self.is_revealed:
            if self.is_mined:
                button.configure(image=self.mine)  # Show mine image if the cell is mined
            else:
                if self.mines_around > 1:
                    button.configure(image=self.number_images.get(self.mines_around))  # Display the number of adjacent mines
                else:
                    button.configure(image=self.neutral)  # Display neutral cell if not
            elif self.is_flagged :
                button.configure(image=self.flagged)
            else :"""
        button.configure(image=self.img_button)    # Show button image if not revealed
            

    def toggle_flags(self):
        """
        Toggle flag status if the cell is not revealed.
        """
        if not self.is_revealed:
            if not self.is_questionned :
                self.is_flagged = not self.is_flagged
                if not self.is_flagged :
                    self.is_questionned = not self.is_questionned
            else :
                self.is_questionned = not self.is_questionned
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
        # Assumes `button` is available for updating the image. 
        # If you don't pass the button reference, you should ensure the button 
        # is correctly fetched and updated when revealing the cell.
        if self.is_revealed :
            if self.is_mined :
                self.button.configure(image=self.exploded_mine)
            elif self.mines_around > 0 :
                self.button.configure(image=self.number_images.get(self.mines_around))
            else:
                self.button.configure(image=self.neutral)  # Neutral image when no adjacent mines
        else :
            if self.is_flagged :
                self.button.configure(image=self.flagged)
            elif self.is_questionned :
                self.button.configure(image=self.question_mark)
            else :
                self.button.configure(image=self.img_button)

    def draw_game_over(self):
        if self.is_mined :
            if self.is_flagged :
                self.button.configure(image=self.flagged)
            elif self.is_revealed :
                self.button.configure(image=self.exploded_mine)
            else :
                self.button.configure(image=self.mine)
        else :
            if self.is_flagged :
                self.button.configure(image=self.wrong_mine)
                
