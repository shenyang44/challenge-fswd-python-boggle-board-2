import string
import random

board = [['-', '-', '-', '-'], ['-', '-', '-', '-'],
         ['-', '-', '-', '-'], ['-', '-', '-', '-']]


def print_board():
    print('\nA Game of BOGGLE!\n')
    for row in board:
        revised_row = "  ".join(row)
        print(revised_row)
    print('\n')


dice = ['AAEEGN',
        'ELRTTY',
        'AOOTTW',
        'ABBJOO',
        'EHRTVW',
        'CIMOTU',
        'DISTTY',
        'EIOSST',
        'DELRVY',
        'ACHOPS',
        'HIMNQU',
        'EEINSU',
        'EEGHNW',
        'AFFKPS',
        'HLNNRZ',
        'DEILRX']


def shake():
    taken = []
    for row in board:
        for i in range(len(row)):
            index = random.randint(0, len(dice)-1)
            while taken.count(index) > 0:
                index = random.randint(0, len(dice)-1)
            taken.append(index)
            die = dice[index]
            die_list = list(die)
            row[i] = random.choice(die_list)
            if row[i] == 'Q':
                row[i] = 'Qu'
            row[i] = row[i].ljust(2)


shake()
print_board()
submitted_words = []
wonnered = False


def check(guess):
    if guess in submitted_words:
        print('You have said that word before!')
        return

    guess_list = list(guess)
    if len(guess_list) < 3:
        print('Sorry, but guesses need to be at least 3 characters long.')
        return
    # Combining the 'Q' and  'U' in the guess_list to a single 'Qu'
    for i in range(len(guess_list)-1):
        if guess_list[i] == 'Q' and guess_list[i+1] == 'U':
            guess_list[i] = 'Qu'
            guess_list.pop(i+1)

    board_list = []
    # Removing empty spaces from the board tiles.
    for rows in board:
        for tile in rows:
            board_list.append(tile.strip())

    # Checks if all letters in the guess exist on the board.
    for i in range(len(guess_list)):
        if not board_list.count(guess_list[i]):
            print('That does not exist')
            return

    guess_copy = guess_list.copy()

    def inner_check(old_i, i, nono_list=[], start_indices=[]):
        global wonnered
        # If inner check has been called the right amount of times word is valid
        if i == (len(guess_list)-1):
            wonnered = True
            return
        if i > 0:
            nono_list.append(old_i)

        # setting variables for current and next letter indices.
        if start_indices == []:
            start_indices = [j for j, x in enumerate(
                board_list) if x == guess_copy[i]]

        next_indices = [j for j, x in enumerate(
            board_list) if x == guess_copy[i+1]]

        for start_i in start_indices:
            for next_i in next_indices:
                if (next_i not in nono_list) and next_i != start_i:
                    # Checks centre blocks and the next possible moves.
                    if start_i in [5, 6, 9, 10]:
                        if (next_i != start_i - 2 or next_i != start_i + 2) and next_i <= start_i + 5 and next_i >= start_i - 5:
                            inner_check(start_i, i+1, nono_list,
                                        start_indices=[next_i])

                    # Checks corner start tiles and next possible moves.
                    elif start_i in [0, 3, 12, 15]:
                        x, y, z = 1, 4, 5
                        if start_i == 3:
                            x, y, z = 2, 6, 7
                        elif start_i == 12:
                            x, y, z = 8, 9, 13
                        elif start_i == 15:
                            x, y, z = 10, 11, 14

                        if next_i in [x, y, z]:
                            inner_check(start_i, i+1, nono_list,
                                        start_indices=[next_i])

                    # Next 3 elif and 1 else will check sides and next possible moves
                    elif start_i == 1 or start_i == 2:
                        if next_i <= start_i + 5 and next_i >= start_i - 1 and next_i != start_i + 2:
                            inner_check(start_i, i+1, nono_list,
                                        start_indices=[next_i])

                    elif start_i in [4, 8]:
                        if next_i in [start_i - 4, start_i - 3, start_i + 4, start_i + 1, start_i + 5]:
                            inner_check(start_i, i+1, nono_list,
                                        start_indices=[next_i])

                    elif start_i == 7 or start_i == 11:
                        if next_i in [start_i - 5, start_i - 4, start_i - 1, start_i + 3, start_i + 4]:
                            inner_check(start_i, i+1, nono_list,
                                        start_indices=[next_i])

                    else:
                        if next_i > start_i - 6 and next_i < start_i + 2 and next_i != start_i-2:
                            inner_check(start_i, i+1, nono_list,
                                        start_indices=[next_i])

    inner_check(0, 0)
    if wonnered:
        print('Valid word')
        submitted_words.append(guess)
        return

    print('Not a valid word!')


# Asking for player input and whether game should continue
playing = True
while playing:
    user_input = input('Word: ')
    check(user_input.upper())
    continue_playing = input('Continue playing? (y/n)')
    if continue_playing == 'y':
        playing = True
        print_board()
        # Reseting win variable
        wonnered = False
    elif continue_playing == 'n':
        playing = False
    else:
        print_board()
        print("Only 'y' and 'n' are acceptable inputs.\n Continuing game.")
        wonnered = False
