import customtkinter as ctk
import tkinter as tk
from grid import Grid


class Game :
    def __init__(self, cell_num=9, mines_count=10, num_flags=10):
        self.app = ctk.CTk()
        self.cell_size = 30
        self.cell_num = cell_num
        self.mines_count = mines_count
        self.grid = Grid(self.cell_size, self.cell_num, self.mines_count, self)
        self.grid_size = self.cell_num * self.cell_size
        self.app.geometry(f"{self.grid_size - self.cell_num * 5 + 2}x{self.grid_size - self.cell_num * 5 + 2}")
        """self.app.maxsize(self.grid_size - self.cell_num * 5 + 2, self.grid_size - self.cell_num * 5+ 2)
        self.app.minsize(self.grid_size - self.cell_num * 5 + 2, self.grid_size - self.cell_num * 5 + 2)"""
        self.app.title("Minesweeper")
        #def top bar here
        self.paused = False
        self.game_over = False
        self.is_left_click_pressed = False
        self.is_left_click_active = False
        self.is_right_click_pressed = False
        self.current_cell = None

        def on_right_press(cell, event):
            """Gestion du clic droit pour poser un drapeau sur la cellule"""
            self.is_right_click_pressed = True
            if self.is_left_click_pressed :
                self.is_left_click_active = False
                on_hover()
            if not self.is_left_click_pressed :
                cell.toggle_flags()
            

        def on_right_release(cell, event):
            """Réinitialise les cellules inspectées quand le clic droit est relâché."""
            self.is_right_click_pressed = False
            on_hover()

        def on_left_press(cell, event):
            """Quand on maintient le clic gauche, on initialise la cellule sous la souris."""
            self.is_left_click_pressed = True
            self.is_left_click_active = True
            self.current_cell = cell
            on_hover()
            
            
        
        def on_left_release(cell, event):
            """Quand le clic gauche est relâché, la cellule sous la souris n'est plus inspectée."""
            self.is_left_click_pressed = False
            if self.is_left_click_active :
                self.grid.reveal_cell(self.current_cell.x, self.current_cell.y)
            for cell in self.grid.inspected_cells:
                cell.is_inspected = False
                cell.update_button()
            self.grid.inspected_cells.clear()
            self.is_left_click_active = False
            if self.game_over :
                self.grid.game_over()

                
        def on_hover():
            """Quand la souris survole une cellule, et que le clic gauche est maintenu, inspecte la cellule."""
            if self.is_left_click_pressed and self.current_cell.is_revealed and self.current_cell.mines_around > 0:
                self.grid.update_inspected_cells(self.current_cell.x, self.current_cell.y)

            # Condition 2: Clic gauche et droit maintenus et hover sur une cellule non révélée
            elif self.is_left_click_pressed and self.is_right_click_pressed and not self.current_cell.is_revealed:
                self.grid.update_inspected_cells(self.current_cell.x, self.current_cell.y)

            # Condition 3: Clic gauche maintenu + Cellule non révélée → Inspecter uniquement cette cellule
            elif self.is_left_click_pressed and not self.current_cell.is_revealed:
                self.grid.update_inspected_cells_single(self.current_cell.x, self.current_cell.y)

                

        def on_motion(event):
            """Détecte le mouvement de la souris quand le clic gauche est maintenu."""
            if self.is_left_click_pressed :
                if not self.is_right_click_pressed :
                    self.is_left_click_active = True
                # Obtenir les coordonnées globales du curseur
                global_x, global_y = event.x_root, event.y_root

                # Convertir en coordonnées de grille
                x = (global_x - self.app.winfo_rootx()) // self.cell_size
                y = (global_y - self.app.winfo_rooty()) // self.cell_size

                # Vérifier que la position est bien dans les limites de la grille
                if 0 <= x < self.cell_num and 0 <= y < self.cell_num:
                    self.current_cell = self.grid.cells[x][y]
                    on_hover()

        self.grid.draw(self.app, on_right_press, on_right_release, on_left_press, on_left_release)
        self.app.bind("<B1-Motion>", on_motion)

    def run(self) :
        self.app.mainloop()


test = Game()
test.run()
