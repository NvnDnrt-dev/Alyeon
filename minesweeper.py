import random
from enum import Enum

class CellState(Enum):
    UNREVEALED = 0
    REVEALED = 1
    FLAGGED = 2

class Minesweeper:
    def __init__(self, rows=18, cols=18, mines=40):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.state = [[CellState.UNREVEALED for _ in range(cols)] for _ in range(rows)]
        self.game_over = False
        self.game_won = False
        
        # Place mines randomly
        mine_count = 0
        while mine_count < mines:
            r = random.randint(0, rows - 1)
            c = random.randint(0, cols - 1)
            if self.board[r][c] != -1:  # -1 represents a mine
                self.board[r][c] = -1
                mine_count += 1
        
        # Calculate numbers
        self._calculate_numbers()
    
    def _calculate_numbers(self):
        """Calculate the number of adjacent mines for each cell"""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != -1:
                    count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                                if self.board[nr][nc] == -1:
                                    count += 1
                    self.board[r][c] = count
    
    def reveal_cell(self, r, c):
        """Reveal a cell and handle game logic"""
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return
        
        if self.state[r][c] == CellState.FLAGGED:
            return
        
        if self.state[r][c] == CellState.REVEALED:
            return
        
        # Hit a mine
        if self.board[r][c] == -1:
            self.game_over = True
            self.state[r][c] = CellState.REVEALED
            return
        
        # Reveal the cell
        self.state[r][c] = CellState.REVEALED
        
        # If it's a blank cell, reveal all adjacent cells
        if self.board[r][c] == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if self.state[nr][nc] == CellState.UNREVEALED:
                            self.reveal_cell(nr, nc)
    
    def toggle_flag(self, r, c):
        """Toggle flag on a cell"""
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return
        
        if self.state[r][c] == CellState.REVEALED:
            return
        
        if self.state[r][c] == CellState.FLAGGED:
            self.state[r][c] = CellState.UNREVEALED
        else:
            self.state[r][c] = CellState.FLAGGED
    
    def check_win(self):
        """Check if the player has won"""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != -1 and self.state[r][c] != CellState.REVEALED:
                    return False
        return True
    
    def get_cell_display(self, r, c):
        """Get the display value for a cell"""
        state = self.state[r][c]
        
        if state == CellState.FLAGGED:
            return "F"
        elif state == CellState.UNREVEALED:
            return "."
        else:  # REVEALED
            if self.board[r][c] == -1:
                return "*"
            elif self.board[r][c] == 0:
                return " "
            else:
                return str(self.board[r][c])

class MinesweeperCLI:
    def __init__(self, rows=6, cols=7, mines=5):
        self.game = Minesweeper(rows, cols, mines)
        self.rows = rows
        self.cols = cols
    
    def display_board(self):
        """Display the game board"""
        print("\n" + "="*40)
        print(f"Minesweeper {self.rows}x{self.cols}")
        print("="*40)
        
        # Print column numbers
        print("  ", end="")
        for c in range(self.cols):
            print(c, end="")
        print()
        
        # Print board
        for r in range(self.rows):
            print(f"{r} ", end="")
            for c in range(self.cols):
                print(self.game.get_cell_display(r, c), end="")
            print()
        
        print("="*40)
        print("Legend: . = unrevealed, F = flagged, * = mine, space = empty, 1-8 = adjacent mines")
        print("="*40)
    
    def play(self):
        """Main game loop"""
        while True:
            self.display_board()
            
            if self.game.game_won:
                print("\n🎉 CONGRATULATIONS! YOU WON! 🎉\n")
                break
            
            if self.game.game_over:
                print("\n💣 GAME OVER! YOU HIT A MINE! 💣\n")
                # Reveal all mines
                for r in range(self.rows):
                    for c in range(self.cols):
                        if self.game.board[r][c] == -1:
                            self.game.state[r][c] = CellState.REVEALED
                self.display_board()
                break
            
            # Get user input
            while True:
                try:
                    command = input("\nEnter command (r=reveal, f=flag, q=quit): ").strip().lower()
                    
                    if command == "q":
                        print("Thanks for playing!")
                        return
                    
                    if command not in ["r", "f"]:
                        print("Invalid command. Use 'r', 'f', or 'q'")
                        continue
                    
                    coords = input("Enter coordinates (row col): ").strip().split()
                    if len(coords) != 2:
                        print("Invalid input. Use 'row col' format (e.g., '2 3')")
                        continue
                    
                    r, c = int(coords[0]), int(coords[1])
                    
                    if command == "r":
                        self.game.reveal_cell(r, c)
                    else:  # f
                        self.game.toggle_flag(r, c)
                    
                    if self.game.check_win():
                        self.game.game_won = True
                    
                    break
                
                except ValueError:
                    print("Invalid input. Please enter numbers for row and column.")
                except Exception as e:
                    print(f"Error: {e}")

if __name__ == "__main__":
    cli = MinesweeperCLI(rows=6, cols=7, mines=5)
    cli.play()
