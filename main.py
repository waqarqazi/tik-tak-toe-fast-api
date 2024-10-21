from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
from typing import Dict, List

app = FastAPI()

# Game state storage
game_sessions: Dict[str, List[List[str]]] = {}  # session_id -> board
current_players: Dict[str, str] = {}  # session_id -> current_player

class Move(BaseModel):
    session_id: str
    row: int
    col: int
    player: str

class ComputerMoveResponse(BaseModel):
    session_id: str
    row: int
    col: int
    board: List[List[str]]

@app.post("/start-game")
def start_game():
    session_id = str(len(game_sessions) + 1)  # Simple session ID generation
    board = [['', '', ''], ['', '', ''], ['', '', '']]
    game_sessions[session_id] = board
    current_players[session_id] = 'X'  # X starts the game
    return {"session_id": session_id, "board": board}

@app.post("/make-move")
def make_move(move: Move):
    if move.session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Game session not found.")

    board = game_sessions[move.session_id]

    # Check if the move is valid
    if board[move.row][move.col] != '':
        raise HTTPException(status_code=400, detail="Invalid move. Cell is already occupied.")

    # Place the player's mark on the board
    board[move.row][move.col] = move.player

    # Check for a win or draw after player's move
    if check_win(board, move.player):
        return {"session_id": move.session_id, "board": board, "winner": move.player}
    if check_draw(board):
        return {"session_id": move.session_id, "board": board, "winner": "Draw"}

    # Switch to the next player (computer)
    computer_move = generate_computer_move(move.session_id)
    board[computer_move.row][computer_move.col] = 'O'  # Computer plays 'O'

    # Check for a win or draw after computer move
    if check_win(board, 'O'):
        return {"session_id": move.session_id, "board": board, "winner": 'O'}
    if check_draw(board):
        return {"session_id": move.session_id, "board": board, "winner": "Draw"}

    return {"session_id": move.session_id, "board": board}

def generate_computer_move(session_id: str):
    board = game_sessions[session_id]
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
    row, col = random.choice(empty_cells)  # Randomly choose an empty cell
    return ComputerMoveResponse(session_id=session_id, row=row, col=col, board=board)

def check_win(board: List[List[str]], player: str) -> bool:
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if all(cell == player for cell in board[i]):  # Check row
            return True
        if all(board[j][i] == player for j in range(3)):  # Check column
            return True
    if all(board[i][i] == player for i in range(3)):  # Check diagonal
        return True
    if all(board[i][2 - i] == player for i in range(3)):  # Check anti-diagonal
        return True
    return False

def check_draw(board: List[List[str]]) -> bool:
    # Check if the board is full and no winner exists
    return all(cell != '' for row in board for cell in row)

@app.get("/status/{session_id}")
def get_status(session_id: str):
    if session_id not in game_sessions:
        raise HTTPException(status_code=404, detail="Game session not found.")
    
    return {"session_id": session_id, "board": game_sessions[session_id]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
