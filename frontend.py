import customtkinter as ctk
import random
import time

# Configuration des niveaux de difficulté
DIFFICULTES = {
    "Facile": (9, 9, 5),
    "Moyen": (16, 16, 40),
    "Difficile": (30, 16, 99)
}

class Case:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mine = False
        self.revealed = False
        self.flagged = 0  # 0 = rien, 1 = drapeau, 2 = ?
        self.mines_voisines = 0
    
    def reveler(self):
        self.revealed = True
    
    def basculer_drapeau(self):
        self.flagged = (self.flagged + 1) % 3

class Demineur:
    def __init__(self, root, difficulte="Facile"):
        self.root = root
        self.difficulte = difficulte
        self.largeur, self.hauteur, self.nb_mines = DIFFICULTES[difficulte]
        self.grille = [[Case(x, y) for y in range(self.hauteur)] for x in range(self.largeur)]
        self.jeu_termine = False
        self.placer_mines()
        self.calculer_mines_voisines()
        self.creer_interface()
        self.start_time = None
        self.timer_running = False

    def placer_mines(self):
        positions = [(x, y) for x in range(self.largeur) for y in range(self.hauteur)]
        random.shuffle(positions)
        for x, y in positions[:self.nb_mines]:
            self.grille[x][y].mine = True

    def calculer_mines_voisines(self):
        for x in range(self.largeur):
            for y in range(self.hauteur):
                if not self.grille[x][y].mine:
                    self.grille[x][y].mines_voisines = sum(
                        self.grille[nx][ny].mine
                        for nx in range(max(0, x-1), min(self.largeur, x+2))
                        for ny in range(max(0, y-1), min(self.hauteur, y+2))
                    )

    def creer_interface(self):
        self.cadres = []
        self.timer_label = ctk.CTkLabel(self.root, text="Temps: 0s", fg_color="white", text_color="black")
        self.timer_label.grid(row=0, column=0, columnspan=self.largeur, pady=5)

        for y in range(self.hauteur):
            ligne = []
            for x in range(self.largeur):
                btn = ctk.CTkButton(self.root, text="", width=30, height=30, command=lambda x=x, y=y: self.reveler_case(x, y))
                btn.grid(row=y+1, column=x, padx=2, pady=2)
                ligne.append(btn)
            self.cadres.append(ligne)

        # Bouton pour changer de difficulté
        change_diff_button = ctk.CTkButton(self.root, text="Changer de difficulté", command=self.changer_difficulte)
        change_diff_button.grid(row=self.hauteur+1, column=0, columnspan=self.largeur, pady=5)

    def reveler_case(self, x, y):
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True

        if self.grille[x][y].mine:
            self.jeu_termine = True
            self.afficher_game_over()
            return
        self.reveal_recursive(x, y)
        self.mettre_a_jour_interface()

    def reveal_recursive(self, x, y):
        if self.grille[x][y].revealed or self.grille[x][y].flagged:
            return
        
        self.grille[x][y].reveler()
        
        if self.grille[x][y].mines_voisines == 0:
            for nx in range(max(0, x-1), min(self.largeur, x+2)):
                for ny in range(max(0, y-1), min(self.hauteur, y+2)):
                    self.reveal_recursive(nx, ny)

    def mettre_a_jour_interface(self):
        for x in range(self.largeur):
            for y in range(self.hauteur):
                case = self.grille[x][y]
                btn = self.cadres[y][x]
                if case.revealed:
                    if case.mine:
                        btn.configure(text="X", fg_color="red")
                    elif case.mines_voisines > 0:
                        btn.configure(text=str(case.mines_voisines), fg_color="white", text_color="black")
                    else:
                        btn.configure(fg_color="white")
                elif case.flagged == 1:
                    btn.configure(text="🚩", fg_color="yellow")
                elif case.flagged == 2:
                    btn.configure(text="?", fg_color="lightgray")
                else:
                    btn.configure(text="", fg_color="lightgray")

        if self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.configure(text=f"Temps: {elapsed_time}s")

    def afficher_game_over(self):
        game_over_win = ctk.CTkToplevel(self.root)
        game_over_win.title("Game Over")
        game_over_label = ctk.CTkLabel(game_over_win, text="Game Over !")
        game_over_label.pack()
        retry_button = ctk.CTkButton(game_over_win, text="Réessayer", command=lambda: [game_over_win.destroy(), self.reset()])
        retry_button.pack()
        change_diff_button = ctk.CTkButton(game_over_win, text="Changer de difficulté", command=lambda: [game_over_win.destroy(), self.changer_difficulte()])
        change_diff_button.pack()
        quit_button = ctk.CTkButton(game_over_win, text="Quitter", command=self.root.quit)
        quit_button.pack()

    def changer_difficulte(self):
        diff_win = ctk.CTkToplevel(self.root)
        diff_win.title("Choisir la difficulté")

        for diff in DIFFICULTES:
            diff_button = ctk.CTkButton(diff_win, text=diff, command=lambda diff=diff: [diff_win.destroy(), self.changer_difficulte_app(diff)])
            diff_button.pack(pady=5)

    def changer_difficulte_app(self, difficulte):
        self.difficulte = difficulte
        self.reset()

    def reset(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root, self.difficulte)

# Interface principale
root = ctk.CTk()
root.title("Démineur")
root.configure(bg="white")

# Appliquer le thème clair
ctk.set_appearance_mode("light")

demineur = Demineur(root)

root.mainloop()
