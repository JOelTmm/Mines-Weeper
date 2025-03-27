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
        self.mines_around = 0
        # Load images for mines and neutral (unrevealed) cells
        image = Image.open("images/mines.png")
        self.img_mines = ImageTk.PhotoImage(image)
        image = Image.open("images/exploded-mines.png")
        self.img_exploded_mines = ImageTk.PhotoImage(image)
        image = Image.open("images/wrong-mines.png")
        self.img_wrong_mines = ImageTk.PhotoImage(image)
        image = Image.open("images/neutrals.png")
        self.clicked_neutrals = ImageTk.PhotoImage(image)
        image = Image.open("images/flags.png")
        self.flagged_buttons = ImageTk.PhotoImage(image)
        image = Image.open("images/buttons.png")
        self.img_buttons = ImageTk.PhotoImage(image)
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

    def draw(self, app, on_click):
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
        if self.is_revealed:
            if self.is_mined:
                button.configure(image=self.img_mines)  # Show mine image if the cell is mined
            else:
                if self.mines_around > 1:
                    print(self.mines_around)
                    button.configure(image=self.number_images.get(self.mines_around))  # Display the number of adjacent mines
                else:
                    button.configure(image=self.clicked_neutrals)  # Display neutral cell if not
        elif self.is_flagged :
            button.configure(image=self.flagged_buttons)
        else :
            button.configure(image=self.img_buttons)    # Show button image if not revealed
            

    def toggle_flags(self):
        """
        Toggle flag status if the cell is not revealed.
        """
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged

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
        if self.is_mined:
            self.button.configure(image=self.img_mines)
        else:
            if self.mines_around > 0:
                print(self.mines_around)
                self.button.configure(image=self.number_images.get(self.mines_around))
            else:
                self.button.configure(image=self.clicked_neutrals)  # Neutral image when no adjacent mines
                
