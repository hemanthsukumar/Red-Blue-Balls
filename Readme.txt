README


Name: Hemanth Sukumar Vangala
UTA ID: 1002118951


Description:
This code implements a simple two-player game called "Red-Blue Balls". The game is played by two players, one of whom starts with a certain number of red balls and the other with a certain number of blue balls. On each turn, a player can remove one ball of either colour. The game continues until one of the players has no balls left. The player who removes the last ball from either pile loses the game.


The code uses the minimax algorithm with alpha-beta pruning to implement an AI player that plays against a human player. 
The minimax_abp function implements the minimax algorithm with alpha-beta pruning. The play_game function starts a new game and alternates turn between the human and AI players until the game ends. The get_possible_moves function returns the possible moves for a given state, and evaluate function assigns a score to each state based on the number of balls left for each color.
The code also includes a TimeoutError exception and a timeout_handler function that raises the exception if the AI player takes too long to make a move.


Structure:
The main structure of the code includes several functions that are used to define the game rules and AI algorithm and a play_game function that puts everything together and allows the human player to interact with the game. The minimax_abp function is recursive and uses memoisation to avoid redundant calculations. The play_game function also prints the current state of the game and prompts the human player to make a move, and uses the minimax_abp function to make moves for the AI player. The code also includes some error handling, such as checking for invalid user inputs and raising an exception if the AI player takes too long to make a move.


Here are brief descriptions of the functions used in the script:
* timeout_handler: This function is called if the human player takes too long to choose a move. It raises a TimeoutError.
* evaluate: This function takes a game state and returns a score based on how advantageous the state is for the current player.
* get_possible_moves: This function takes a game state and returns a list of all possible moves (i.e., which color ball to pick) for the current player.
* is_game_over: This function takes a game state and returns True if the game is over (i.e., all balls of one color have been picked).
* minimax_abp: This function is an implementation of the minimax algorithm with alpha-beta pruning. It takes a game state, a maximum depth to search, and the current values of alpha and beta, and returns the best move and associated score for the current player.
* play_game: This function allows a human player to play against the computer. It takes the initial number of red and blue balls, the current player (either "human" or "computer"), and the maximum search depth for the minimax algorithm. It alternates turns between the human and computer players until the game is over, and announces the winner.


Usage:
Run the file “red_blue_nim.py”
The command line invocation should follow the following format:
red_blue_nim.py <number of red balls> <number of blue balls> <first-player> <depth>


Example:
python red_blue_nim.py 10 10 human 10
If ‘first-player’ is not given, it takes “computer” by default.
If ‘depth’ is not given, it takes the “None” value by default.


Main Module:
red_blue_nim.py
Readme.txt
Note: All files must be in the same folder


Requirements:
OS: Windows or Mac
This program requires Python 3 to run.