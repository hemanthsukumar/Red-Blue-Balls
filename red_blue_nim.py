import random
import sys


def get_possible_moves(state):
    moves = []
    if state["red_balls"] > 0:
        moves.append("red")
    if state["blue_balls"] > 0:
        moves.append("blue")
    return moves


def is_game_over(state):
    return state["red_balls"] == 0 or state["blue_balls"] == 0


def evaluate(is_max_player):
    # The player who just moved (opposite of is_max_player) took the last ball and loses.
    # If it is now the max player's turn, the min player just lost → computer wins.
    if is_max_player:
        return 100
    return -100


def minmax_alpha_beta_pruning(depth, max_depth, alpha, beta, is_max_player, state, memo):
    key = (depth, is_max_player, state['red_balls'], state['blue_balls'])
    if key in memo:
        return memo[key]

    if is_game_over(state):
        return None, evaluate(is_max_player)

    if depth == max_depth:
        return None, 0

    if is_max_player:
        max_value = float('-inf')
        best_step = None
        for move in get_possible_moves(state):
            new_state = {'red_balls': state['red_balls'], 'blue_balls': state['blue_balls']}
            if move == 'red':
                new_state['red_balls'] -= 1
            else:
                new_state['blue_balls'] -= 1
            _, value = minmax_alpha_beta_pruning(depth + 1, max_depth, alpha, beta, False, new_state, memo)
            if value > max_value:
                max_value = value
                best_step = move
            alpha = max(alpha, max_value)
            if beta <= alpha:
                break
        memo[key] = best_step, max_value
        return best_step, max_value
    else:
        min_value = float('inf')
        best_step = None
        for move in get_possible_moves(state):
            new_state = {'red_balls': state['red_balls'], 'blue_balls': state['blue_balls']}
            if move == 'red':
                new_state['red_balls'] -= 1
            else:
                new_state['blue_balls'] -= 1
            _, value = minmax_alpha_beta_pruning(depth + 1, max_depth, alpha, beta, True, new_state, memo)
            if value < min_value:
                min_value = value
                best_step = move
            beta = min(beta, min_value)
            if beta <= alpha:
                break
        memo[key] = best_step, min_value
        return best_step, min_value


def play_game(red_balls, blue_balls, current_player, max_depth):
    print(f"\nStarting game with {red_balls} red balls and {blue_balls} blue balls")
    memo = {}
    while red_balls > 0 and blue_balls > 0:
        print(f"\nCurrent state:\n\tred balls: {red_balls}\n\tblue balls: {blue_balls}")
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
        else:
            state = {"red_balls": red_balls, "blue_balls": blue_balls}
            color, _ = minmax_alpha_beta_pruning(0, max_depth, float('-inf'), float('inf'), True, state, memo)
            if color is None:
                color = random.choice(get_possible_moves(state))
            if color == "red":
                red_balls -= 1
                print("\nComputer picked a red ball.")
            else:
                blue_balls -= 1
                print("\nComputer picked a blue ball.")
        current_player = "computer" if current_player == "human" else "human"

    print("\nGame over!")
    # current_player is now the player who did NOT take the last ball — they win.
    winner(current_player, red_balls, blue_balls)


def winner(player, red_balls, blue_balls):
    print(f"\n{player} has won the game with {red_balls * 2 + blue_balls * 3} points")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python red_blue_nim.py <red_balls> <blue_balls> [first_player] [max_depth]")
        sys.exit(1)

    try:
        red_balls = int(sys.argv[1])
        blue_balls = int(sys.argv[2])
    except ValueError:
        print("Error: red_balls and blue_balls must be integers")
        sys.exit(1)

    if red_balls <= 0 or blue_balls <= 0:
        print("Error: both piles must have at least 1 ball")
        sys.exit(1)

    current_player = sys.argv[3] if len(sys.argv) >= 4 else "computer"
    if current_player not in ("human", "computer"):
        print("Error: first_player must be 'human' or 'computer'")
        sys.exit(1)

    max_depth = int(sys.argv[4]) if len(sys.argv) >= 5 else red_balls + blue_balls
    play_game(red_balls, blue_balls, current_player, max_depth)
