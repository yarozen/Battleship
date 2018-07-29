# coding=utf-8
import random
import os
import platform
import sys
import socket


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def draw_board(g):
    return ("""
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


def init_grid():
    g = {}
    for x in 'ABCDEFGHIJ':
        for y in range(1, 11):
            g[x, y] = symbols('empty')
    return g


def find_available_spot_for_ship(ship_len, g):
    while True:
        direction = random.choice([(0, 1), (1, 0)])  # horizontal→(0, 1) vertical↓(1, 0)
        row = random.choice('ABCDEFGHIJ')  # choose row
        col = random.choice(range(1, 11))  # choose column
        can_position_ship = True
        for i in range(ship_len):
            try:
                if g[chr(ord(row) + i*direction[0]), col + i*direction[1]] == symbols('ship'):
                    can_position_ship = False
                    break
            except KeyError:
                can_position_ship = False
                break
            for a, b in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                try:
                    if g[chr(ord(row) + a + i*direction[0]), col + b + i*direction[1]] == symbols('ship'):
                        can_position_ship = False
                        break
                except KeyError:
                    pass
        if can_position_ship:
            ship_position = {}
            for i in range(ship_len):
                ship_position[(chr(ord(row) + i*direction[0]), col + i*direction[1])] = False
            return ship_position


def get_user_guess(board, guess_board, my_turn, c):
    while True:
        if my_turn:
            print(draw_board(board))
            print(draw_board(guess_board))
        else:
            c.send(draw_board(board).replace('\n', '\r\n').encode())
            c.send(draw_board(guess_board).replace('\n', '\r\n').encode())
        try:
            if my_turn:
                user = str(input("Select Row and column (e.g. B8): "))
            else:
                c.send("Select Row and column (e.g. B8): ".encode())
                user = ""
                while '\n' not in user:
                    user += c.recv(1024).decode()
                user = user.strip()
        except KeyboardInterrupt:
            sys.exit(0)
        try:
            row = user[0].upper()
            col = int(user[1:])
            if row in 'ABCDEFGHIJ' and col in range(1, 11):
                if guess_board[row, col] == symbols('empty'):
                    return [row, col]
        except ValueError:
            pass
        except IndexError:
            pass


def check_if_hit_or_miss(board, guess_board, fleet, row, col):
    if board[row, col] == symbols('ship'):
        guess_board[row, col] = symbols('hit')
        # print("Hit! you have another turn")
        for i in fleet:
            if (row, col) in fleet[i]:
                fleet[i][row, col] = True
                return i
    else:
        guess_board[row, col] = symbols('miss')
        # print("Miss!, opponent's turn")
        return False


def check_if_ship_sunk(guess_board, fleet, i):
    for part in fleet[i]:  # check if all parts of the ship got hit
        if fleet[i][part] is False:  # if at least one part wasn't hit return false
            return False
    else:  # if all parts of ship got hit
        for part in fleet[i]:  # reveal ship on guess board (replace the hit symbol with the ship symbol)
            guess_board[part] = symbols('ship')
            # mark squares around revealed ship as miss on guess board (because ships cannot be adjacent to each other)
            for a, b in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                try:
                    if guess_board[chr(ord(part[0]) + a), part[1] + b] != symbols('ship'):
                        guess_board[chr(ord(part[0]) + a), part[1] + b] = symbols('miss')
                except KeyError:
                    pass
        return True


def get_ships_coordinates(ships, board):
    ships_position = {}
    for ship_name, ship_len in enumerate(ships, 1):
        ships_position[ship_name] = find_available_spot_for_ship(ship_len, board)
        board = position_ship_on_my_board(board, ships_position[ship_name])
    return board, ships_position


def position_ship_on_my_board(board, ship_coordinates):
    for square in ship_coordinates:
        board[square] = symbols('ship')
    return board


def wait_for_opponent_to_connect():
    host = get_ip_address()
    port = 5000
    s = socket.socket()
    s.bind((host, port))
    s.listen(1)
    print("Welcome to BATTLESHIP!\r\n"
          "Waiting for opponent to join me at {}:{} ...".format(host, port))
    c, addr = s.accept()
    print("opponent just connected from {}".format(addr))
    c.send(b"Welcome to BATTLESHIP!\r\n")
    # c.recv(1024)
    return c


def symbols(action):
    switcher = {
        # 'ship':  '■',
        # 'empty': '·',
        # 'hit':   'X',
        # 'miss':  '~',
        'ship': '*',
        'empty': '.',
        'hit': 'x',
        'miss': '~',
    }
    return switcher.get(action)


def main():
    ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    ###
    my_board = init_grid()
    my_guess_board = init_grid()
    my_board, my_fleet = get_ships_coordinates(ships, my_board)
    my_ships_sunk = 0
    ###
    opponent_board = init_grid()
    opponent_guess_board = init_grid()
    opponent_board, opponent_fleet = get_ships_coordinates(ships, opponent_board)
    opponent_ships_sunk = 0
    ###
    my_turn = True
    c = wait_for_opponent_to_connect()
    c.send(draw_board(opponent_board).replace('\n', '\r\n').encode(encoding='UTF-8'))
    c.send(draw_board(opponent_guess_board).replace('\n', '\r\n').encode(encoding='UTF-8'))
    while my_ships_sunk < len(ships) and opponent_ships_sunk < len(ships):
        if my_turn:
            row, col = get_user_guess(my_board, my_guess_board, my_turn, c)
            ship_got_hit = check_if_hit_or_miss(opponent_board, my_guess_board, opponent_fleet, row, col)
            if ship_got_hit:
                if check_if_ship_sunk(my_guess_board, opponent_fleet, ship_got_hit):
                    opponent_ships_sunk += 1
            else:
                my_turn = False
        else:
            row, col = get_user_guess(opponent_board, opponent_guess_board, my_turn, c)
            ship_got_hit = check_if_hit_or_miss(my_board, opponent_guess_board, my_fleet, row, col)
            if ship_got_hit:
                if check_if_ship_sunk(opponent_guess_board, my_fleet, ship_got_hit):
                    my_ships_sunk += 1
            else:
                my_turn = True
    print("You Win!")


if __name__ == '__main__':
    main()
