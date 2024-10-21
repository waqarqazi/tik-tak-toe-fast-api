from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, conlist, ValidationError
from typing import List, Union
import numpy as np

app = FastAPI()

# Constants for players
PLAYER_X = "X"
PLAYER_O = "O"

class MoveRequest(BaseModel):
    board: List[List[Union[int, str]]]  # Board can contain integers (0 for empty) and strings ('X' or 'O')
    current_player: str

def check_winner(board):
    """Check rows, columns, and diagonals for a win."""
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
    if all(cell != 0 for row in board for cell in row):
        return "draw"

    return "ongoing"

def validate_board(board):
    """Validate that the board is a 3x3 grid and contains only valid values (0, 'X', 'O')."""
    if not isinstance(board, list) or len(board) != 3:
        raise HTTPException(status_code=400, detail="Invalid board size. The board must be a 3x3 grid.")
    
    for row in board:
        if not isinstance(row, list) or len(row) != 3:
            raise HTTPException(status_code=400, detail="Each row must be a list of size 3.")
        for cell in row:
            if cell not in [0, PLAYER_X, PLAYER_O]:
                raise HTTPException(status_code=400, detail="Invalid board values. Must be 0, 'X', or 'O'.")

def validate_player(player):
    """Validate that the player is either 'X' or 'O'."""
    if player not in [PLAYER_X, PLAYER_O]:
        raise HTTPException(status_code=400, detail="Invalid player. Player must be 'X' or 'O'.")

@app.post("/make-move")
def make_move_endpoint(request: MoveRequest):
    """Process a player's move and return the updated board."""
    validate_board(request.board)
    validate_player(request.current_player)

    board = request.board
    result = check_winner(board)
    
    if result != "ongoing":
        raise HTTPException(status_code=400, detail=f"Game is already over. Result: {result}.")

    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == 0]
    if not empty_cells:
        raise HTTPException(status_code=400, detail="No available moves. The game is a draw.")

    row, col = empty_cells[np.random.choice(len(empty_cells))]
    board[row][col] = request.current_player
    return {"updated_board": board}

@app.post("/check-state")
def check_game_state(request: MoveRequest):
    """Check the current state of the game."""
    validate_board(request.board)
    validate_player(request.current_player)

    board = request.board
    result = check_winner(board)
    return {"status": result}

@app.post("/reset")
def reset_game():
    """Reset the game to an empty board."""
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    return {"board": board}

# To run the app, use the command: uvicorn main:app --reload
