import tkinter as tk
from tkinter import Menu


# Classe TopBar qui contient le timer et le compteur de drapeaux
class TopBar(tk.Frame):
    def __init__(self, parent, game, width):
        super().__init__(parent, width=width)
        self.game = game
        self.timer_value = 0
        self.max_flag = self.game.mines_count
        
        # Timer affichage
        self.timer_label = tk.Label(self, text="Timer: 0", font=("Arial", 14))
        self.timer_label.grid(row=0, column=0)

        # Bouton Start Game
        self.start_button = tk.Button(self, text="Reset", command=self.reset)
        self.start_button.grid(row=0, column=1)

        # Menu déroulant (clic droit)
        self.menu = Menu(self, tearoff=0)
        self.menu.add_command(label="Easy 9x9 10 mines", command=lambda: self.game.change_mode(9, 9, 10))
        self.menu.add_command(label="Medium 16x16 40 mines", command=lambda: self.game.change_mode(16, 16, 40))
        self.menu.add_command(label="Hard 30x16 99 mines", command=lambda: self.game.change_mode(30, 16, 99))

        # Lier le clic droit au bouton pour afficher le menu
        self.start_button.bind("<Button-3>", self.show_menu)  # Clic droit pour afficher le menu

        # Compteur de drapeaux
        self.flags_label = tk.Label(self, text=f"Flags: {self.max_flag}", font=("Arial", 14))
        self.flags_label.grid(row=0, column=2)

    def start_timer(self):
        """Démarre le timer"""
        if not self.game.running:
            self.game.running = True
            self.update_timer()
    
    def reset_timer(self) :
        self.game.running = False
        self.timer_value = 0  
        self.update_timer()

    def update_timer(self):
        """Met à jour le timer"""
        if self.game.running:
            self.timer_value += 1
            self.timer_label.config(text=f"Timer: {self.timer_value}")
            self.after(1000, self.update_timer)    # Mise à jour chaque seconde
        else :
            self.timer_label.config(text=f"Timer: {self.timer_value}")
              

    def update_flags(self):
            """Update the flags remaining."""
            remaining_flags = self.max_flag - self.game.flags_count
            self.flags_label.configure(text=remaining_flags)

    def reset(self):
        # Supprimer toutes les mines et réinitialiser les boutons
        self.game.grid.reset_all_cells()    # Appel à la méthode de réinitialisation de la grille
        self.game.reset_game()
        self.update_flags()
        self.update_timer()


    def show_menu(self, event):
        # Afficher le menu déroulant au clic droit
        self.menu.post(event.x_root, event.y_root)
