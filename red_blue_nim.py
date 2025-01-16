import random
import sys

class TimeoutError(Exception):
    pass

#function to be called in case of time out
def timeout_handler(signum, frame):
    raise TimeoutError("Timeout! Your turn is skipped.")

def verify(state):
    if state["red_balls"] == 0:
        return -100
    elif state["blue_balls"] == 0:
        return 100
    else:
        return 0
    
#function takes the current state of the game and returns a list of possible next steps that can be taken by the computer
def next_steps_to_follow(state, memo={}):
    key = (state['red_balls'], state['blue_balls'])
    if key in memo:
        return memo[key]
    steps = []
    if state["red_balls"] > 1 and state["red_balls"] % 2 == 0:
        steps.append("red")
    elif state["blue_balls"] > 1 and state["blue_balls"] % 2 == 0:
        steps.append("blue")
    else:
        if state["red_balls"] > state["blue_balls"] and state["blue_balls"] > 0:
            steps.append("red")
        elif state["red_balls"] > 0 and state["red_balls"] < state["blue_balls"]:
            steps.append("blue")
        elif state["red_balls"] == state["blue_balls"]:
            steps.append('red')
            steps.append('blue')
        memo[key] = steps
    return steps

#function checks if the game is over by checking if either the red or blue pile has zero balls remaining
def is_game_over(state, memo={}):
    key = (state['red_balls'], state['blue_balls'])
    if key in memo:
        return memo[key]
    result = state["red_balls"] == 0 or state["blue_balls"] == 0
    memo[key] = result
    return result

#implementation of depth limited minimax alpha beta pruning algorithm
def minmax_alpha_beta_pruning(depth, max_depth, alpha, beta, is_max_player, state, memo={}):
    key = (depth, is_max_player, state['red_balls'], state['blue_balls'])
    if key in memo:
        return memo[key]

    # Evaluate the state if the maximum depth has been reached or the game is over
    if depth == max_depth or is_game_over(state):
        return None, verify(state)

    if is_max_player:
        max_value = float('-inf')
        best_step = None
        for move in next_steps_to_follow(state):
            new_state = {'red_balls': state['red_balls'], 'blue_balls': state['blue_balls']}
            if move == 'red':
                new_state['red_balls'] -= 1
            else:
                new_state['blue_balls'] -= 1
            # Recursively call the function for the next depth level
            _, value = minmax_alpha_beta_pruning(depth + 1, max_depth, alpha, beta, False, new_state, memo)
            if value > max_value:
                max_value = value
                best_step = move
            alpha = max(alpha, max_value)
            # Check if the pruning condition has been met
            if beta <= alpha:
                break
        memo[key] = best_step, max_value
        return best_step, max_value

    else:
        min_value = float('inf')
        best_step = None
        for move in next_steps_to_follow(state):
            new_state = {'red_balls': state['red_balls'], 'blue_balls': state['blue_balls']}
            if move == 'red':
                new_state['red_balls'] -= 1
            else:
                new_state['blue_balls'] -= 1
            # Recursively call the function for the next depth level
            _, value = minmax_alpha_beta_pruning(depth + 1, max_depth, alpha, beta, True, new_state, memo)
            if value < min_value:
                min_value = value
                best_step = move
            beta = min(beta, min_value)
            # Check if the pruning condition has been met
            if beta <= alpha:
                break
        memo[key] = best_step, min_value
        return best_step, min_value

#algorithm to play game, this initiates the game and let players take their turns
def play_game(red_balls, blue_balls, current_player, max_depth):
    print(f"\nStarting game with {red_balls} red balls and {blue_balls} blue balls")
    # Loop until there are no more red or blue balls left
    while red_balls > 0 and blue_balls > 0:
        # Print the current state of the game
        print(f"\nCurrent state: \n\tred balls: {red_balls}\n\tblue balls: {blue_balls} ")
        # If it's the human player's turn, ask them for their move
        if current_player == "human":
            while True:
                color = input("\nYour turn! Which color ball do you want to pick? (red/blue): ").lower()
                if color == "red" and red_balls > 0:
                    red_balls -= 1
                    break
                elif color == "blue" and blue_balls > 0:
                    blue_balls -= 1
                    break
                else:
                    print("\nInvalid choice! Please select a valid color.")
        # If it's the computer's turn, use the minimax algorithm to make a move
        else:
            # If there are an equal number of red and blue balls, randomly choose a color
            if red_balls == blue_balls:
                color = random.choice(["red", "blue"])
            # Otherwise, use the minimax algorithm to determine the best move
            else:
                state = {"current_player": "computer", "red_balls": red_balls, "blue_balls": blue_balls}
                color, _ = minmax_alpha_beta_pruning(0, max_depth, float('-inf'), float('inf'), True, state)
            # Make the move chosen by the computer
            if color == "red":
                red_balls -= 1
                if red_balls == 0:
                    print("\nComputer picked the last red ball! You win!")
                    winner("human", red_balls, blue_balls)
                    return
                else:
                    print("\nComputer picked a red ball.")
            else:
                blue_balls -= 1
                if blue_balls == 0:
                    print("\nComputer picked the last blue ball! You win!")
                    winner("human", red_balls, blue_balls)
                    return
                else:
                    print("\nComputer picked a blue ball.")
        # Switch the current player
        current_player = "computer" if current_player == "human" else "human"    
    print("\nGame over!")
    # Determine the winner of the game
    winner(current_player, red_balls, blue_balls)
    
#to display the winner and points scored 
def winner(player, red_balls, blue_balls):
    print(f"\n{player} has won the game with {red_balls * 2 + blue_balls * 3} points")

#main 
if __name__ == "__main__":
    # get input arguments from command line
    red_balls = int(sys.argv[1])
    blue_balls = int(sys.argv[2])
    current_player = sys.argv[3] if len(sys.argv) >= 4 else "computer"
    max_depth = int(sys.argv[4]) if len(sys.argv) >= 5 else None
    play_game(red_balls, blue_balls, current_player, max_depth)
    