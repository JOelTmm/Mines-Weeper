import customtkinter as ctk
from PIL import Image


class Cell:
    def __init__(self, x, y, size, top_bar):
        self.x = x
        self.y = y
        self.size = size
        self.top_bar = top_bar
        self.is_mined = False
        self.is_revealed = False
        self.is_flagged = False
        self.mines_around = 0
        self.img_mines = ctk.CTkImage(light_image=Image.open("mines.png"), dark_image=Image.open("mines.png"))
        self.img_neutrals = ctk.CTkImage(light_image=Image.open("neutrals.png"), dark_image=Image.open("neutrals.png"))


    def draw(self, screen):
        button = ctk.CTkButton(screen, width=self.size, height=self.size)
        button.grid(row=self.y, column=self.x, padx=1, pady=1)
        if self.is_revealed :
            if self.is_mined :
                button.configure(image=self.img_mines)
            else :
                if self.mines_around > 0 :
                    button.configure(text=f"{self.mines_around}")    #number img here
        else :
            button.configure(image=self.img_neutrals)

    def toggle_flags(self) :
        if not self.is_revealed :
            self.is_flagged = not self.is_flagged

    def reveal(self) :
        if not self.is_flagged :
            self.is_revealed = True
            return self.is_mined
        return False
    
    def draw(self, screen) :
        for row in self.cells :
            for cell in row :
                cell.draw(screen)