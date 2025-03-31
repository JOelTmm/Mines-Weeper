import random
from cell import Cell


class Grid:
    def __init__(self, cell_size, row_cell_num, column_cell_num, mines_count, game):
        """
        Initialize a Grid object.
        :param cell_size: Size of each cell
        :param row_cell_num: Number of rows in the grid
        :param column_cell_num: Number of columns in the grid
        :param mines_count: Number of mines to be placed on the grid
        :param game: Reference to the main game instance
        """
        self.cell_size = cell_size
        self.row_cell_num = row_cell_num
        self.column_cell_num = column_cell_num
        self.mines_count = mines_count
        self.game = game
        self.recursive_game_over = False

        # Create a 2D list of Cell objects for the grid
        self.cells = [
            [Cell(x, y, self.cell_size, game) for y in range(self.column_cell_num)]
            for x in range(self.row_cell_num)
        ]

        self.mines_placed = False
        self.inspected_cells = set()

    def place_mines(self, safe_x, safe_y):
        """
        Randomly place mines on the grid, ensuring not to place one in the safe zone.
        :param safe_x: X coordinate of the safe cell (first clicked cell)
        :param safe_y: Y coordinate of the safe cell (first clicked cell)
        """
        mines_to_place = self.mines_count
        safe_zone = {
            (safe_x + dx, safe_y + dy) for dx in range(-1, 2) for dy in range(-1, 2)
        }
        while mines_to_place > 0:
            # Randomly pick a cell for the mine
            x = random.randint(0, self.row_cell_num - 1)
            y = random.randint(0, self.column_cell_num - 1)

            # Avoid placing a mine on the safe cell or on an already mined cell
            if (x, y) not in safe_zone and not self.cells[x][y].is_mined:
                self.cells[x][y].is_mined = True
                mines_to_place -= 1

        # After placing mines, calculate the number of adjacent mines for each cell
        for x in range(self.row_cell_num):
            for y in range(self.column_cell_num):
                self.cells[x][y].mines_around = self.count_mines_around(x, y)

    def count_mines_around(self, x, y):
        """
        Count the number of mines around a given cell.
        :param x: X coordinate of the cell
        :param y: Y coordinate of the cell
        :return: Number of mines surrounding the cell
        """
        count = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.row_cell_num and 0 <= ny < self.column_cell_num:
                    if self.cells[nx][ny].is_mined:
                        count += 1
        return count

    def count_flags_around(self, x, y):
        """Count the number of flagged cells around a given cell."""
        count = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.row_cell_num and 0 <= ny < self.column_cell_num:
                    if self.cells[nx][ny].is_flagged:
                        count += 1
        return count

    def reveal_cell(self, x, y):
        """
        Reveal a specific cell and trigger further actions if needed.
        :param x: X coordinate of the cell to reveal
        :param y: Y coordinate of the cell to reveal
        :return: True if the revealed cell contains a mine, False otherwise
        """
        if not self.mines_placed:
            self.game.topbar.start_timer()
            self.place_mines(x, y)
            self.mines_placed = True

        if self.cells[x][y].reveal():
            self.draw_game_over()
            return True

        if self.cells[x][y].mines_around == 0:
            self.recursive_reveal(x, y)
        elif self.cells[x][y].mines_around == self.count_flags_around(x, y):
            self.reveal_adjacent(x, y)
        return False

    def recursive_reveal(self, x, y):
        """Recursively reveal all adjacent cells to a cell with no mines around."""
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.row_cell_num and 0 <= ny < self.column_cell_num:
                    cell = self.cells[nx][ny]
                    if not cell.is_revealed and not cell.is_mined:
                        cell.reveal()
                        if cell.mines_around == 0:
                            self.recursive_reveal(nx, ny)
                        elif cell.is_mined and cell.is_flagged:
                            self.recursive_reveal(nx, ny)

    def reveal_adjacent(self, x, y):
        """Reveal all adjacent cells, including mines."""
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.row_cell_num and 0 <= ny < self.column_cell_num:
                    cell = self.cells[nx][ny]
                    if not cell.is_revealed and not cell.is_flagged:
                        if cell.mines_around == 0:
                            self.recursive_reveal(nx, ny)
                        self.recursive_game_over = self.reveal_cell(cell.x, cell.y)
                        if self.recursive_game_over:
                            self.game.handle_game_over()

    def draw(self, parent_frame, on_right_press, on_right_release, on_left_press, on_left_release):
        """Draw the entire grid."""
        for row in self.cells:
            for cell in row:
                cell.draw(parent_frame, on_right_press, on_right_release, on_left_press, on_left_release)

    def draw_game_over(self):
        """Update the grid display when the game is over."""
        for row in self.cells:
            for cell in row:
                cell.draw_game_over()

    def get_adjacent_cells(self, x, y):
        """Get the list of adjacent cells."""
        adjacent_cells = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.row_cell_num and 0 <= ny < self.column_cell_num:
                    adjacent_cells.append(self.cells[nx][ny])
        return adjacent_cells

    def update_inspected_cells(self, x, y):
        """Update the inspected cells by resetting old ones and adding new ones."""
        old_inspected_cells = self.inspected_cells.copy()
        for cell in old_inspected_cells:
            cell.is_inspected = False
            cell.update_button()

        self.inspected_cells = set(self.get_adjacent_cells(x, y))
        for cell in self.inspected_cells:
            cell.is_inspected = True
            cell.update_button()

    def update_inspected_cells_single(self, x, y):
        """Update only the inspected cell for hovering on an unrevealed cell."""
        old_inspected_cells = self.inspected_cells.copy()
        for cell in old_inspected_cells:
            cell.is_inspected = False
            cell.update_button()

        self.inspected_cells = {self.cells[x][y]}
        self.cells[x][y].is_inspected = True
        self.cells[x][y].update_button()

    def reset_all_cells(self):
        """Reset all cells in the grid."""
        for row in self.cells:
            for cell in row:
                cell.reset()
                cell.update_button()
        self.mines_placed = False

    def check_victory(self):
        """Check if all mines are correctly flagged."""
        for row in self.cells:
            for cell in row:
                if cell.is_mined and not cell.is_flagged:
                    return False
                if not cell.is_mined and cell.is_flagged:
                    return False
        return True
