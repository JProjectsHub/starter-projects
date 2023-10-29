import random
from time import sleep


def get_user_move():
    move = input("Rock (R), Papeer (P), Scissors (S)?: ")
    return move.upper()

def get_computer_move():
    computer_move = random.random()
    if 0 < computer_move < 0.37:
        computer_move = "R"
    elif 0.37 < computer_move < 0.74:
        computer_move = "P"
    else:
        computer_move = "S"
    return computer_move

def compute_winner(user_move, computer_move):
    if user_move == computer_move:
        return "It's a draw!"
    elif (user_move == "R" and computer_move == "S" or user_move == "P"
          and computer_move == "R" or user_move == "S" and computer_move == "P"):
        return "You win!"
    else:
        return "The computer wins!"
    
def print_computer_move(computer_move):
    printed_move = ""
    if computer_move == "R":
        printed_move = "Rock"
    elif computer_move == "P":
        printed_move = "Paper"
    elif computer_move == "S":
        printed_move = "Scissors"
    return printed_move

if __name__ == '__main__':
    delay = 0.5

answer = input("Would you like to play Rock Paper Scissors?: \nYes (Y) or No (N): ")
if answer.upper() == "Y" or answer.upper() == "YES":
    print("Let's play!")
    moves = ["Rock", "Paper", "Scissors"]
    for move in moves:
        sleep(delay)
        print("\n" + move)
    user_move = get_user_move()
    computer_move = get_computer_move()
    sleep(delay)
    print("Shoot!")
    sleep(delay)
    print(f'The computer chooses: {print_computer_move(computer_move)}')
    print(compute_winner(user_move, computer_move))
else:
    quit()

