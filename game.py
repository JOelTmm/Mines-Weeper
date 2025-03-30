import customtkinter as ctk
import tkinter as tk
from grid import Grid


class Game :
    def __init__(self, cell_num=9, mines_count=10, num_flags=10):
        self.app = ctk.CTk()
        self.cell_size = 30
        self.cell_num = cell_num
        self.mines_count = mines_count
        self.grid = Grid(self.cell_size, self.cell_num, self.mines_count)
        self.grid_size = self.cell_num * self.cell_size
        self.app.geometry(f"{self.grid_size - self.cell_num * 5 + 2}x{self.grid_size - self.cell_num * 5 + 2}")
        """self.app.maxsize(self.grid_size - self.cell_num * 5 + 2, self.grid_size - self.cell_num * 5+ 2)
        self.app.minsize(self.grid_size - self.cell_num * 5 + 2, self.grid_size - self.cell_num * 5 + 2)"""
        self.app.title("Minesweeper")
        #def top bar here
        self.paused = False
        self.game_over = False

        # Méthode de gestion des clics sur les cellules
        def on_click(cell):
            # Appeler la méthode `reveal()` sur la cellule correspondante
            if self.grid.reveal_cell(cell.x, cell.y):
                cell.draw_game_over()
            if self.grid.check_win_condition():
                print("Victoire!")
                #arrêter timer changer smiley

        def on_right_click(cell):
            """Gestion du clic droit pour poser un drapeau sur la cellule"""
            cell.toggle_flags()
        
        self.grid.draw(self.app, on_click, on_right_click)

    def run(self) :
        self.app.mainloop()




test = Game()


test.run()
