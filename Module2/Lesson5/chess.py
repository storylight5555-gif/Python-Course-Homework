import os
import sys

# Unique Unicode pieces lookup mapper
UNICODE_PIECES = {
    'wP': '♙', 'wR': '♖', 'wN': '♘', 'wB': '♗', 'wQ': '♕', 'wK': '♔',
    'bP': '♟', 'bR': '♜', 'bN': '♞', 'bB': '♝', 'bQ': '♛', 'bK': '♚',
    '--': '.'
}

class GameState:
    def __init__(self):
        # 8x8 Board Matrix: '--' represents empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.white_to_move = True

    def print_board(self):
        """Clears terminal screen and prints the visual text chess board layout."""
        # Clear console (works for Windows 'cls' and Unix 'clear')
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n    a  b  c  d  e  f  g  h")
        print("  +------------------------+")
        for r in range(8):
            row_string = f"{8 - r} |"
            for c in range(8):
                piece = self.board[r][c]
                symbol = UNICODE_PIECES[piece]
                row_string += f" {symbol} "
            row_string += f"| {8 - r}"
            print(row_string)
        print("  +------------------------+")
        print("    a  b  c  d  e  f  g  h\n")
        
        turn = "White" if self.white_to_move else "Black"
        print(f"Current Turn: {turn}")

    def make_move(self, start_sq, end_sq):
        """Executes a move manipulation on the matrix array grid."""
        s_row, s_col = start_sq
        e_row, e_col = end_sq
        
        piece = self.board[s_row][s_col]
        
        # Move piece and clear old square
        self.board[e_row][e_col] = piece
        self.board[s_row][s_col] = "--"
        
        # Simple pawn promotion to Queen automatically at end ranks
        if piece == 'wP' and e_row == 0:
            self.board[e_row][e_col] = 'wQ'
        if piece == 'bP' and e_row == 7:
            self.board[e_row][e_col] = 'bQ'

        self.white_to_move = not self.white_to_move

    def get_valid_moves(self, row, col):
        """Calculates valid legal movements for the selected coordinate piece."""
        piece = self.board[row][col]
        if piece == "--":
            return []
            
        color = piece[0]
        # Restrict players to moving only their active turn assets
        if (color == 'w' and not self.white_to_move) or (color == 'b' and self.white_to_move):
            return []

        piece_type = piece[1]
        moves = []

        if piece_type == 'P':
            moves = self.get_pawn_moves(row, col, color)
        elif piece_type == 'R':
            moves = self.get_sliding_moves(row, col, [(1,0), (-1,0), (0,1), (0,-1)])
        elif piece_type == 'B':
            moves = self.get_sliding_moves(row, col, [(1,1), (-1,-1), (1,-1), (-1,1)])
        elif piece_type == 'Q':
            moves = self.get_sliding_moves(row, col, [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)])
        elif piece_type == 'N':
            moves = self.get_jump_moves(row, col, [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)])
        elif piece_type == 'K':
            moves = self.get_jump_moves(row, col, [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)])

        return moves

    def get_pawn_moves(self, r, c, color):
        moves = []
        direction = -1 if color == 'w' else 1
        start_row = 6 if color == 'w' else 1

        # 1-Square Forward Move
        if 0 <= r + direction < 8 and self.board[r + direction][c] == "--":
            moves.append((r + direction, c))
            # 2-Square Initial Jump Move
            if r == start_row and self.board[r + 2 * direction][c] == "--":
                moves.append((r + 2 * direction, c))

        # Diagonal Captures
        for dc in [-1, 1]:
            next_c = c + dc
            next_r = r + direction
            if 0 <= next_r < 8 and 0 <= next_c < 8:
                target = self.board[next_r][next_c]
                if target != "--" and target[0] != color:
                    moves.append((next_r, next_c))
        return moves

    def get_sliding_moves(self, r, c, directions):
        moves = []
        color = self.board[r][c][0]
        for dr, dc in directions:
            for i in range(1, 8):
                end_r, end_c = r + dr * i, c + dc * i
                if 0 <= end_r < 8 and 0 <= end_c < 8:
                    target = self.board[end_r][end_c]
                    if target == "--":
                        moves.append((end_r, end_c))
                    elif target[0] != color:
                        moves.append((end_r, end_c))
                        break # Blocked after enemy capture
                    else:
                        break # Blocked by friendly piece
                else:
                    break # Out of boundaries
        return moves

    def get_jump_moves(self, r, c, offsets):
        moves = []
        color = self.board[r][c][0]
        for dr, dc in offsets:
            end_r, end_c = r + dr, c + dc
            if 0 <= end_r < 8 and 0 <= end_c < 8:
                target = self.board[end_r][end_c]
                if target == "--" or target[0] != color:
                    moves.append((end_r, end_c))
        return moves


def parse_notation(notation_str):
    """Converts algebraic standard notations like 'e2' to row, col tuple (6, 4)."""
    if len(notation_str) != 2:
        return None
    files = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    ranks = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
    
    f, r = notation_str[0].lower(), notation_str[1]
    if f in files and r in ranks:
        return ranks[r], files[f]
    return None


def main():
    gs = GameState()

    while True:
        gs.print_board()
        
        # User input handling loop
        user_input = input("\nEnter move (e.g., 'e2 e4' or type 'exit'): ").strip()
        if user_input.lower() == 'exit':
            print("Game exited.")
            sys.exit()

        parts = user_input.split()
        if len(parts) != 2:
            input("Invalid format! Use format space separation: 'e2 e4'. Press Enter to retry.")
            continue

        start_sq = parse_notation(parts[0])
        end_sq = parse_notation(parts[1])

        if start_sq is None or end_sq is None:
            input("Invalid notation format! Numbers 1-8, Letters a-h. Press Enter to retry.")
            continue

        valid_moves = gs.get_valid_moves(start_sq[0], start_sq[1])

        if end_sq in valid_moves:
            gs.make_move(start_sq, end_sq)
        else:
            input("Illegal move! That piece cannot move there. Press Enter to retry.")


if __name__ == "__main__":
    main()
