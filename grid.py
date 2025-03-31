import random
from cell import Cell

class Grid:
    def __init__(self, cell_size, cell_num, mines_count, game):
        """
        Initialize a Grid object.
        :param cell_size: Size of each cell
        :param cell_num: Number of cells in each row and column (grid dimension)
        :param mines_count: Number of mines to be placed on the grid
        """
        self.cell_size = cell_size
        self.cell_num = cell_num
        self.mines_count = mines_count
        self.game = game
        
        # Create a 2D list of Cell objects for the grid
        self.cells = [[Cell(x, y, self.cell_size, game) for y in range(self.cell_num)]
                      for x in range(self.cell_num)]
        
        self.mines_placed = False
        self.inspected_cells = set()

    def place_mines(self, safe_x, safe_y):
        """
        Randomly place mines on the grid, ensuring not to place one in the safe spot.
        :param safe_x: X coordinate of the safe cell (the first cell clicked by the user)
        :param safe_y: Y coordinate of the safe cell (the first cell clicked by the user)
        """
        mines_to_place = self.mines_count
        safe_zone = {(safe_x + dx, safe_y + dy) for dx in range(-1, 2) for dy in range(-1, 2)}
        while mines_to_place > 0:
            # Randomly pick a cell for the mine
            x = random.randint(0, self.cell_num - 1)
            y = random.randint(0, self.cell_num - 1)
            
            # Avoid placing a mine on the safe cell or on an already mined cell
            if (x, y) not in safe_zone and not self.cells[x][y].is_mined:
                self.cells[x][y].is_mined = True
                mines_to_place -= 1

        # After placing mines, calculate the number of adjacent mines for each cell
        for x in range(self.cell_num):
            for y in range(self.cell_num):
                self.cells[x][y].mines_around = self.count_mines_around(x, y)

    def count_mines_around(self, x, y):
        """
        Count the number of mines around a given cell.
        :param x: X coordinate of the cell
        :param y: Y coordinate of the cell
        :return: Number of mines surrounding the cell
        """
        count = 0
        # Check all adjacent cells (including diagonal neighbors)
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                # Ensure the neighbor is within grid boundaries
                if 0 <= nx < self.cell_num and 0 <= ny < self.cell_num:
                    if self.cells[nx][ny].is_mined:
                        count += 1
        return count
    
    def count_flags_around(self, x, y) :
        count = 0
        # Check all adjacent cells (including diagonal neighbors)
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                # Ensure the neighbor is within grid boundaries
                if 0 <= nx < self.cell_num and 0 <= ny < self.cell_num:
                    if self.cells[nx][ny].is_flagged:
                        count += 1
        print(count)
        return count

    def reveal_cell(self, x, y):
        """
        Reveal a specific cell and trigger further actions if needed.
        :param x: X coordinate of the cell to reveal
        :param y: Y coordinate of the cell to reveal
        :return: True if the revealed cell contains a mine, False otherwise
        """
        if not self.mines_placed:
            # Place mines after the first cell is revealed
            self.place_mines(x, y)
            self.mines_placed = True
        
        # Reveal the cell, and check if it contains a mine
        if self.cells[x][y].reveal():
            self.game_over()
            return True
        
        # If the cell is empty (0 adjacent mines), reveal adjacent cells recursively
        if self.cells[x][y].mines_around == 0:
            self.recursive_reveal(x, y)
        elif self.cells[x][y].mines_around == self.count_flags_around(x, y):
            self.reveal_adjacent(x, y)
        return False

    def recursive_reveal(self, x, y):
        """
        Recursively reveal all adjacent cells to a cell with no mines around.
        :param x: X coordinate of the cell
        :param y: Y coordinate of the cell
        """
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.cell_num and 0 <= ny < self.cell_num:
                    cell = self.cells[nx][ny]
                    if not cell.is_revealed and not cell.is_mined:
                        cell.reveal()
                        # If the newly revealed cell has no adjacent mines, recursively reveal its neighbors
                        if cell.mines_around == 0:
                            self.recursive_reveal(nx, ny)
                        elif cell.is_mined and cell.is_flagged :
                            self.recursive_reveal(nx, ny)

    def reveal_adjacent(self, x, y):
        """
        Recursively reveal all adjacent cells to a cell, including revealing mines.
        :param x: X coordinate of the cell
        :param y: Y coordinate of the cell
        """
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.cell_num and 0 <= ny < self.cell_num:
                    cell = self.cells[nx][ny]
                    
                    # Reveal the cell if it is not revealed
                    if not cell.is_revealed and not cell.is_flagged:
                        self.game.game_over = self.reveal_cell(cell.x, cell.y)

                        # If the revealed cell has no adjacent mines, recursively reveal its neighbors
                        if cell.mines_around == 0:
                            self.reveal_adjacent(nx, ny)

    def check_win_condition(self):
        """
        Check if the player has won the game (all non-mined cells are revealed).
        :return: True if the player has won, False otherwise
        """
        for row in self.cells:
            for cell in row:
                if not cell.is_mined and not cell.is_revealed:
                    return False
        return True

    def draw(self, app, on_right_press, on_right_release, on_left_press, on_left_release):
        """
        Draw the entire grid on the screen.
        :param screen: The parent widget where the grid is drawn
        """
        for row in self.cells:
            for cell in row:

                cell.draw(app, on_right_press, on_right_release, on_left_press, on_left_release)
    
    def game_over(self) :
        for row in self.cells:
            for cell in row:
                cell.draw_game_over()

    def get_adjacent_cells(self, x, y) :
        adjacent_cells = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.cell_num and 0 <= ny < self.cell_num:
                    adjacent_cells.append(self.cells[nx][ny])
        return adjacent_cells

    def update_inspected_cells(self, x, y):
        """Met à jour les cellules inspectées en nettoyant les anciennes et en ajoutant les nouvelles."""
        # Stocke les anciennes cellules inspectées avant de les réinitialiser
        old_inspected_cells = self.inspected_cells.copy()

        # Réinitialise toutes les anciennes cellules inspectées
        for cell in old_inspected_cells:
            cell.is_inspected = False
            cell.update_button()

        # Sélectionner les nouvelles cellules adjacentes
        self.inspected_cells = set(self.get_adjacent_cells(x, y))

        for cell in self.inspected_cells:
            cell.is_inspected = True
            cell.update_button()

    def update_inspected_cells_single(self, x, y):
        """Met à jour uniquement la cellule inspectée (pour hover sur une cellule non révélée)."""
        # Stocke l'ancienne cellule inspectée pour la réinitialiser
        old_inspected_cells = self.inspected_cells.copy()

        print(f"Ancienne cellule inspectée : {[f'({c.x}, {c.y})' for c in old_inspected_cells]}")

        # Réinitialiser les anciennes cellules inspectées
        for cell in old_inspected_cells:
            cell.is_inspected = False
            cell.update_button()

        # Ajouter seulement la cellule survolée
        self.inspected_cells = {self.cells[x][y]}
        self.cells[x][y].is_inspected = True
        self.cells[x][y].update_button()

