import random

# Class representing an individual cell in the game
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False  # Is this cell a mine?
        self.is_revealed = False  # Has this cell been revealed?
        self.is_flagged = 0  # 0: unknown, 1: flag, 2: question mark
        self.adjacent_mines = 0  # Number of adjacent mines

    def reveal(self, game_board):
        """Reveal this cell and handle the result."""
        if self.is_revealed or self.is_flagged != 0:
            return "Continue"
        self.is_revealed = True
        if self.is_mine:
            return "Game Over"
        if self.adjacent_mines == 0:
            self.reveal_adjacent(game_board)
        return "Continue"

    def reveal_adjacent(self, game_board):
        """Recursively reveal adjacent cells if they are empty."""
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x, new_y = self.x + dx, self.y + dy
                if (0 <= new_x < game_board.width and 
                    0 <= new_y < game_board.height):
                    game_board.grid[new_x][new_y].reveal(game_board)

    def toggle_flag(self):
        """Cycle between unknown -> flag -> question mark -> unknown."""
        if not self.is_revealed:
            self.is_flagged = (self.is_flagged + 1) % 3

# Class managing the game board and its logic
class GameBoard:
    def __init__(self, difficulty="beginner"):
        """Initialize the game board based on difficulty level."""
        self.set_difficulty(difficulty)
        self.grid = [[Cell(x, y) for y in range(self.height)] for x in range(self.width)]
        self.mines_placed = False  # Mines are placed after the first click
        self.game_over = False
        self.cells_revealed = 0  # Track revealed non-mine cells

    def set_difficulty(self, difficulty):
        """Set board size and mine count based on difficulty."""
        if difficulty == "beginner":
            self.width, self.height = 9, 9
            self.mines = 5
        elif difficulty == "intermediate":
            self.width, self.height = 16, 16
            self.mines = 40
        elif difficulty == "advanced":
            self.width, self.height = 30, 16
            self.mines = 99
        else:
            raise ValueError("Invalid difficulty level. Choose: beginner, intermediate, advanced")

    def place_mines(self, first_x, first_y):
        """Place mines randomly, excluding the first clicked cell."""
        if self.mines_placed:
            return
        mines_to_place = self.mines
        while mines_to_place > 0:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if not self.grid[x][y].is_mine and (x != first_x or y != first_y):
                self.grid[x][y].is_mine = True
                mines_to_place -= 1
        self.mines_placed = True
        self.calculate_adjacent_mines()

    def calculate_adjacent_mines(self):
        """Calculate the number of adjacent mines for each cell."""
        for x in range(self.width):
            for y in range(self.height):
                if not self.grid[x][y].is_mine:
                    count = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = x + dx, y + dy
                            if (0 <= nx < self.width and 
                                0 <= ny < self.height and 
                                self.grid[nx][ny].is_mine):
                                count += 1
                    self.grid[x][y].adjacent_mines = count

    def reveal_cell(self, x, y):
        """Handle the logic when a cell is clicked."""
        if self.game_over:
            return "Game is already over."
        if not self.mines_placed:
            self.place_mines(x, y)
        cell = self.grid[x][y]
        result = cell.reveal(self)
        if result == "Game Over":
            self.game_over = True
            return "You hit a mine! Game Over."
        self.cells_revealed += 1
        if self.check_victory():
            self.game_over = True
            return "Congratulations! You won!"
        return "Continue"

    def toggle_flag(self, x, y):
        """Toggle flag or question mark on a cell."""
        if not self.game_over and not self.grid[x][y].is_revealed:
            self.grid[x][y].toggle_flag()

    def check_victory(self):
        """Check if the player has won."""
        total_non_mine_cells = (self.width * self.height) - self.mines
        return self.cells_revealed >= total_non_mine_cells

    def get_cell_state(self, x, y):
        """Return the current state of a cell for display purposes."""
        cell = self.grid[x][y]
        if cell.is_revealed:
            if cell.is_mine:
                return "M"  # Mine
            return str(cell.adjacent_mines) if cell.adjacent_mines > 0 else " "
        elif cell.is_flagged == 1:
            return "F"  # Flag
        elif cell.is_flagged == 2:
            return "?"  # Question mark
        return "#"  # Hidden

    def display_board(self):
        """Print the current state of the board (for debugging)."""
        for x in range(self.width):
            row = [self.get_cell_state(x, y) for y in range(self.height)]
            print(" ".join(row))

# Example usage with different difficulty levels
if __name__ == "__main__":
    # Test Beginner level (9x9, 5 mines)
    print("Beginner Level:")
    beginner_game = GameBoard("beginner")
    beginner_game.reveal_cell(4, 4)  # First click
    beginner_game.toggle_flag(0, 0)  # Place a flag
    beginner_game.toggle_flag(1, 1)  # Place a flag
    beginner_game.toggle_flag(1, 1)  # Change flag to question mark
    beginner_game.display_board()
    print()

    # Test Intermediate level (16x16, 40 mines)
    print("Intermediate Level:")
    intermediate_game = GameBoard("intermediate")
    intermediate_game.reveal_cell(8, 8)  # First click
    intermediate_game.display_board()
    print()

    # Test Advanced level (30x16, 99 mines)
    print("Advanced Level:")
    advanced_game = GameBoard("advanced")
    advanced_game.reveal_cell(15, 8)  # First click
    advanced_game.display_board()