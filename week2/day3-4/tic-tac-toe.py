'''Instructions:
Tic Tac Toe is played on a 3x3 grid. Players take turns marking empty squares with their symbol (‘O’ or ‘X’). The first player to get three of their symbols in a row (horizontally, vertically, or diagonally) wins. If all squares are filled and no player has three in a row, the game is a tie.



Step 1: Representing the Game Board

You’ll need a way to represent the 3x3 grid.
A list of lists (a 2D list) is a good choice.
Initially, each cell in the grid should be empty (e.g., represented by a space ‘ ‘).


Step 2: Displaying the Game Board

Create a function called display_board() to print the current state of the game board.
The output should visually represent the 3x3 grid.
Think about how to format the output to make it easy to read.


Step 3: Getting Player Input

Create a function called player_input(player) to get the player’s move.
The function should ask the player to enter a position (e.g., row and column numbers).
Validate the input to ensure it’s within the valid range and that the chosen cell is empty.
Think about how to ask the user for input, and how to validate that input.


Step 4: Checking for a Winner

Create a function called check_win(board, player) to check if the current player has won.
The function should check all possible winning combinations (rows, columns, diagonals).
If a player has won, return True; otherwise, return False.
Think about how to check every possible winning combination.


Step 5: Checking for a Tie

Create a function to check if the game has resulted in a tie.
The function should check if all positions of the board are full, without a winner.


Step 6: The Main Game Loop

Create a function called play() to manage the game flow.
Initialize the game board.
Use a while loop to continue the game until there’s a winner or a tie.
Inside the loop:
Display the board.
Get the current player’s input.
Update the board with the player’s move.
Check for a winner.
Check for a tie.
Switch to the next player.
After the loop ends, display the final result (winner or tie).


Tips:

Consider creating helper functions to break down the logic into smaller, manageable parts.
Follow the single responsibility principle: each function should do one thing and do it well.
Think about how to switch between players.
Think about how you will store the player’s symbol.
'''
board = [[' ' for _ in range(3)] for _ in range(3)]
def display_board():
    for row in board:
        print(' |'.join(row))
        print('-' * 8)
def player_input(player):
    row=int(input(f"Player {player}, enter row (1-3): "))
    col=int(input(f"Player {player}, enter column (1-3): "))
    if 1 <= row <= 3 and 1 <= col <= 3 and board[row-1][col-1] == ' ':
        return row-1, col-1
    else:
        print("Invalid input. Please try again.")
        return player_input(player)

def check_win(player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def check_tie():
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

def play():
    current_player = 'X'
    while True:
        display_board()
        row, col = player_input(current_player)
        board[row][col] = current_player
        if check_win(current_player):
            display_board()
            print(f"Player {current_player} wins!")
            break
        if check_tie():
            display_board()
            print("It's a tie!")
            break
        current_player = 'O' if current_player == 'X' else 'X'

play()