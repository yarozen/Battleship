# coding=utf-8
import random
import os
import platform
import time
import sys
import pprint


def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def draw_board(g):
    print("""
      1 2 3 4 5 6 7 8 9 10
    A {} {} {} {} {} {} {} {} {} {}
    B {} {} {} {} {} {} {} {} {} {}
    C {} {} {} {} {} {} {} {} {} {}
    D {} {} {} {} {} {} {} {} {} {}
    E {} {} {} {} {} {} {} {} {} {}
    F {} {} {} {} {} {} {} {} {} {}
    G {} {} {} {} {} {} {} {} {} {}
    H {} {} {} {} {} {} {} {} {} {}
    I {} {} {} {} {} {} {} {} {} {}
    J {} {} {} {} {} {} {} {} {} {}
    """.format(
        g['A', 1], g['A', 2], g['A', 3], g['A', 4], g['A', 5], g['A', 6], g['A', 7], g['A', 8], g['A', 9], g['A', 10],
        g['B', 1], g['B', 2], g['B', 3], g['B', 4], g['B', 5], g['B', 6], g['B', 7], g['B', 8], g['B', 9], g['B', 10],
        g['C', 1], g['C', 2], g['C', 3], g['C', 4], g['C', 5], g['C', 6], g['C', 7], g['C', 8], g['C', 9], g['C', 10],
        g['D', 1], g['D', 2], g['D', 3], g['D', 4], g['D', 5], g['D', 6], g['D', 7], g['D', 8], g['D', 9], g['D', 10],
        g['E', 1], g['E', 2], g['E', 3], g['E', 4], g['E', 5], g['E', 6], g['E', 7], g['E', 8], g['E', 9], g['E', 10],
        g['F', 1], g['F', 2], g['F', 3], g['F', 4], g['F', 5], g['F', 6], g['F', 7], g['F', 8], g['F', 9], g['F', 10],
        g['G', 1], g['G', 2], g['G', 3], g['G', 4], g['G', 5], g['G', 6], g['G', 7], g['G', 8], g['G', 9], g['G', 10],
        g['H', 1], g['H', 2], g['H', 3], g['H', 4], g['H', 5], g['H', 6], g['H', 7], g['H', 8], g['H', 9], g['H', 10],
        g['I', 1], g['I', 2], g['I', 3], g['I', 4], g['I', 5], g['I', 6], g['I', 7], g['I', 8], g['I', 9], g['I', 10],
        g['J', 1], g['J', 2], g['J', 3], g['J', 4], g['J', 5], g['J', 6], g['J', 7], g['J', 8], g['J', 9], g['J', 10])
    )
    time.sleep(0.1)


def init_grid():
    g = {}
    for x in 'ABCDEFGHIJ':
        for y in range(1, 11):
            g[x, y] = empty
    return g


def find_available_spot_for_ship(ship_len, g):
    while True:
        direction = random.choice([(0, 1), (1, 0)])  # horizontal→(0, 1) vertical↓(1, 0)
        row = random.choice('ABCDEFGHIJ')  # choose row
        col = random.choice(range(1, 11))  # choose column
        can_position_ship = True
        for i in range(ship_len):
            try:
                if g[chr(ord(row) + i*direction[0]), col + i*direction[1]] == ship:
                    can_position_ship = False
                    break
            except KeyError:
                can_position_ship = False
                break
            for a, b in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                try:
                    if g[chr(ord(row) + a + i*direction[0]), col + b + i*direction[1]] == ship:
                        can_position_ship = False
                        break
                except KeyError:
                    pass
        if can_position_ship:
            ship_position = {}
            for i in range(ship_len):
                ship_position[(chr(ord(row) + i*direction[0]), col + i*direction[1])] = False
            return ship_position


def get_user_guess():
    while True:
        draw_board(my_board)
        draw_board(guess_board)
        try:
            user = str(input("Select Row and column (e.g. B8): "))
        except KeyboardInterrupt:
            sys.exit(0)
        try:
            row = user[0].upper()
            col = int(user[1:])
            if row in 'ABCDEFGHIJ' and col in range(1, 11):
                if guess_board[row, col] == empty:
                    return [row, col]
        except ValueError:
            pass
        except IndexError:
            pass


def check_if_hit_or_miss(row, col):
    if my_board[row, col] == ship:
        guess_board[row, col] = hit
        # print("Hit! you have another turn")
        for i in fleet:
            if (row, col) in fleet[i]:
                fleet[i][row, col] = True
                return i
    else:
        guess_board[row, col] = miss
        # print("Miss!, opponent's turn")
        return False


def check_if_ship_sunk(i):
    for part in fleet[i]:
        if fleet[i][part] is False:
            return False
    else:
        for part in fleet[i]:
            guess_board[part] = ship
        return True


def get_ships_coordinates():
    ships_position = {}
    for ship_name, ship_len in enumerate(ships, 1):
        ships_position[ship_name] = find_available_spot_for_ship(ship_len, my_board)
        position_ship_on_my_board(ships_position[ship_name])
    return ships_position


def position_ship_on_my_board(ship_coordinates):
    for square in ship_coordinates:
        my_board[square] = ship


empty = '·'
ship = '■'
hit = 'X'
miss = '~'
ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
my_board = init_grid()
guess_board = init_grid()
fleet = get_ships_coordinates()
fleet_sum = sum(fleet)
ships_sunk = 0
while ships_sunk < len(ships):
    #clear()
    # pprint.pprint(fleet)
    row, col = get_user_guess()
    ship_got_hit = check_if_hit_or_miss(row, col)
    if ship_got_hit is not False:
        if check_if_ship_sunk(ship_got_hit) is True:
            ships_sunk += 1
    else:
        pass
        # TODO switch turn
print("You Win!")
