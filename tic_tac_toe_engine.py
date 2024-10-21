import numpy as np
from fastapi import HTTPException

# Constants for players
PLAYER_X = "X"
PLAYER_O = "O"

def check_winner(board):
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != 0:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != 0:
            return board[0][i]
    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != 0:
        return board[0][2]
    
    # Check for draw
    if np.all(board != 0):
        return "draw"
    
    return "ongoing"

def validate_board(board):
    """Validate that the board is a 3x3 grid and contains only valid values."""
    if not isinstance(board, list) or len(board) != 3:
        raise HTTPException(status_code=400, detail="Invalid board size. The board must be a 3x3 grid.")
    
    for row in board:
        if not isinstance(row, list) or len(row) != 3:
            raise HTTPException(status_code=400, detail="Invalid board size. The board must be a 3x3 grid.")
        
        for cell in row:
            if cell not in [0, PLAYER_X, PLAYER_O]:
                raise HTTPException(status_code=400, detail="Invalid board values. Board must contain only 0, 'X', or 'O'.")

def validate_player(player):
    """Validate that the player is either 'X' or 'O'."""
    if player not in [PLAYER_X, PLAYER_O]:
        raise HTTPException(status_code=400, detail="Invalid player. Player must be 'X' or 'O'.")

def validate_move(board, row, col):
    """Validate that the move is within bounds and is on an empty cell."""
    if not (0 <= row < 3 and 0 <= col < 3):
        raise HTTPException(status_code=400, detail="Move out of bounds. Row and column must be between 0 and 2.")
    
    if board[row][col] != 0:
        raise HTTPException(status_code=400, detail="Invalid move. Cell is already occupied.")

def get_computer_move(board):
    """Finds the next available move for the computer (just a random empty spot for simplicity)."""
    empty_cells = np.argwhere(board == 0)
    if len(empty_cells) == 0:
        raise HTTPException(status_code=400, detail="No available moves. The game is a draw.")
    
    move = empty_cells[np.random.choice(len(empty_cells))]
    return int(move[0]), int(move[1])

def make_move(board, current_player):
    """Updates the board with the current player's move and returns the updated board."""
    validate_board(board)
    validate_player(current_player)
    
    # Check if the game is already over
    result = check_winner(board)
    if result != "ongoing":
        raise HTTPException(status_code=400, detail=f"Game is already over. Result: {result}.")
    
    if current_player == PLAYER_O:
        row, col = get_computer_move(board)
    else:
        # Assume the move comes from the user; validation should be done on frontend
        raise HTTPException(status_code=400, detail="User move not provided. Expected computer move.")

    board[row][col] = current_player
    return board

