import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
    "Bonus": 1
}

symbol_value = {
    "A": 15,
    "B": 12,
    "C": 9,
    "D": 6,
    "Bonus": 24
}

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    bonus_triggered = False
    for line in range(lines):
        symbols_in_line = [column[line] for column in columns]
        unique_symbols = set(symbols_in_line)

        if len(unique_symbols) == 2 and "Bonus" in unique_symbols:
            bonus_triggered = True

        for column in columns:
            symbol = column[line]
            if symbol != symbols_in_line[0]:
                break
        else:
            winnings += values[symbols_in_line[0]] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines, bonus_triggered

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)
    columns = []
    current_symbols = all_symbols[:]
    for _ in range(cols):
        column = []
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns

def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end =" | ")
            else:
                print(column[row], end = "")
        print()

def deposit():
    while True:
        amount = input("What would you like to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Please enter an amount greater than 0.")
        else:
            print("Please enter a valid number")
    return amount

def get_number_of_lines():
    while True:
        lines = input("Enter the number of lines to bet on (1 -" + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= 3:
                break
            else:
                print("Please enter a valid number of lines")
        else:
            print("Please enter a valid number")
    return lines

def get_bet():
    while True:
        amount = input("What would you like to bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Please enter an amount between ${MIN_BET} - ${MAX_BET}.")
        else:
            print("Please enter a valid number")
    return amount

def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines
        if total_bet > balance:
            print(f"You do not have enough to bet that amount, your current balance is: ${balance}")
        else:
            break
    print(f"You are betting ${bet} on ${lines} lines. Total bet is equal to: ${total_bet}")
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)

    winnings, winning_lines, bonus_triggered = check_winnings(slots, lines, bet, symbol_value)

    if bonus_triggered:
        bonus_winnings = bonus_round(bet)
        winnings += bonus_winnings
    balance -= total_bet

    print(f"You won ${winnings}.")
    print(f"You won on lines: ", *winning_lines)
    return winnings - total_bet

def bonus_round(bet):
    print("Congratulations you reached the bonus round")
    bonus_winnings = bet * 2
    total_bonus_winnings = bonus_winnings * 3
    print(f"Bonus round winnings: ${total_bonus_winnings} (Triple total earnings)")
    return total_bonus_winnings

def main(): 
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to play (q to quit). ")
        if answer == "q":
            break
        balance += spin(balance)
    print(f"You cashed out with ${balance}")  
main()