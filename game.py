import tkinter as tk
from grid import Grid
from topbar import TopBar

class Game :
    def __init__(self, row_cell_num=9, column_cell_num=9, mines_count=10):
        self.app = tk.Tk()
        self.cell_size = 30
        self.row_cell_num = row_cell_num
        self.column_cell_num = column_cell_num
        self.mines_count = mines_count
        self.flags_count = 0
        self.running = False
        self.game_over = False
        self.is_left_click_pressed = False
        self.is_left_click_active = False
        self.is_right_click_pressed = False
        self.current_cell = None

        # Calculer la taille de la fenêtre
        self.topbar_frame_size_y = 100
        self.app.title("Minesweeper")
        self.grid_size_x = self.row_cell_num * self.cell_size
        self.grid_size_y = self.column_cell_num * self.cell_size
        self.app_x = self.grid_size_x
        self.app_y = self.topbar_frame_size_y + self.grid_size_y
        self.app.geometry(f"{self.app_x}x{self.app_y}")
        # Définir la taille minimale et maximale de la fenêtre
        self.app.maxsize(width=self.app_x, height=self.app_y)  # Taille maximale
        self.app.minsize(width=self.app_x, height=self.app_y)  # Taille minimale

        # Créer une frame pour la TopBar
        self.topbar_frame = tk.Frame(self.app)
        self.app.grid_rowconfigure(0, weight=0, minsize=self.topbar_frame_size_y)
        self.topbar_frame.grid(row=0, column=0, sticky="ew")

        # Créer et placer la TopBar
        self.topbar = TopBar(self.topbar_frame, self, self.grid_size_x)
        self.topbar.grid(row=0, column=0)

        # Créer une frame pour la grille de jeu
        self.grid_frame = tk.Frame(self.app)
        self.grid_frame.grid(row=1, column=0, sticky="nsew")

        def on_right_press(cell, event):
            if not self.game_over :
                """Gestion du clic droit pour poser un drapeau sur la cellule"""
                self.is_right_click_pressed = True
                if self.is_left_click_pressed :
                    self.is_left_click_active = False
                    on_hover()
                if not self.is_left_click_pressed :
                    cell.toggle_flags()
                    self.topbar.update_flags()
            

        def on_right_release(cell, event):
            if not self.game_over :
                """Réinitialise les cellules inspectées quand le clic droit est relâché."""
                self.is_right_click_pressed = False

        def on_left_press(cell, event):
            if not self.game_over :
                """Quand on maintient le clic gauche, on initialise la cellule sous la souris."""
                self.is_left_click_pressed = True
                self.is_left_click_active = True
                self.current_cell = cell
                on_hover()
            
            
        
        def on_left_release(cell, event):

            if not self.game_over :
                """Quand le clic gauche est relâché, la cellule sous la souris n'est plus inspectée."""
                self.is_left_click_pressed = False
                if self.is_left_click_active :
                    self.game_over = self.grid.reveal_cell(self.current_cell.x, self.current_cell.y)
                for cell in self.grid.inspected_cells:
                    cell.is_inspected = False
                    cell.update_button()
                self.grid.inspected_cells.clear()
                self.is_left_click_active = False
                if self.grid.recursive_game_over :
                    if self.game_over :
                        self.handle_game_over()

                
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
            # Obtenir les coordonnées globales du curseur
            global_x, global_y = event.x_root, event.y_root

            # Convertir en coordonnées de grille
            x = (global_x - self.app.winfo_rootx()) // self.cell_size
            y = (global_y - self.topbar_frame_size_y - self.app.winfo_rooty()) // self.cell_size
            
            # Vérifier que la position est bien dans les limites de la grille
            if 0 <= x < self.row_cell_num and 0 <= y < self.column_cell_num:
                self.current_cell = self.grid.cells[x][y]
                if self.is_left_click_pressed :
                    if not self.is_right_click_pressed :
                        self.is_left_click_active = True
                        on_hover()

        # Créer et dessiner la grille
        self.grid = Grid(self.cell_size, self.row_cell_num, self.column_cell_num, self.mines_count, self)
        self.grid.draw(self.grid_frame, on_right_press, on_right_release, on_left_press, on_left_release)
        self.app.bind("<B1-Motion>", on_motion)

    def handle_game_over(self) :
        print("lol")
        self.running = False
        self.game_over = True
        self.current_cell = None
        self.grid.draw_game_over()
        self.topbar.update_timer()

    def reset_game(self):
        self.running = False
        self.current_cell = None
        self.flags_count = 0
        self.game_over = False
        self.is_left_click_pressed = False
        self.is_left_click_active = False
        self.is_right_click_pressed = False
        self.topbar.reset_timer()

    def run(self) :
        self.app.mainloop()

    def destroy(self):
        self.app.destroy()

    def change_mode(self, row_cell_num, column_cell_num, mines_count):
        # Fermer l'ancienne instance de jeu et en créer une nouvelle
        self.destroy()  # Détruire l'ancienne fenêtre
        new_game = Game(row_cell_num, column_cell_num, mines_count)  # Nouvelle instance
        new_game.run()  # Démarrer le nouveau jeu 


if __name__ == "__main__":
    game = Game()
    game.app.mainloop()
