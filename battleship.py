import argparse
import os
import platform
import random
import socket
import sys
from pickle import dumps, loads


class Player:
    ships_len = (4, 3, 3, 2, 2, 2, 1, 1, 1, 1)
    sym_ship = '●'
    sym_hit = '○'
    sym_miss = '~'
    sym_destroyed = '%'
    sym_empty = '·'

    def __init__(self, name):
        self.name = name
        self.fleet = {}
        self.game_board = self.__create_empty_board()
        self.guess_board = self.__create_empty_board()
        self.__position_ships_on_board()
        self.my_ships_destroyed = 0
        self.opponent_ships_destroyed = 0

    @staticmethod
    def __create_empty_board():
        temp = {}
        for x in 'ABCDEFGHIJ':
            for y in range(1, 11):
                temp[x, y] = __class__.sym_empty
        return temp

    @staticmethod
    def clear():
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

    def print_board(self, me, opponent):
        self.clear()
        for i in (self.game_board, self.guess_board):
            if i == self.game_board:
                print("{}\n{}".format(me, '-' * len(self.name)))
            else:
                print("{}\n{}".format(opponent, '-' * len(opponent)))
            print("""  1 2 3 4 5 6 7 8 9 10
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
                i['A', 1], i['A', 2], i['A', 3], i['A', 4], i['A', 5],
                i['A', 6], i['A', 7], i['A', 8], i['A', 9], i['A', 10],
                i['B', 1], i['B', 2], i['B', 3], i['B', 4], i['B', 5],
                i['B', 6], i['B', 7], i['B', 8], i['B', 9], i['B', 10],
                i['C', 1], i['C', 2], i['C', 3], i['C', 4], i['C', 5],
                i['C', 6], i['C', 7], i['C', 8], i['C', 9], i['C', 10],
                i['D', 1], i['D', 2], i['D', 3], i['D', 4], i['D', 5],
                i['D', 6], i['D', 7], i['D', 8], i['D', 9], i['D', 10],
                i['E', 1], i['E', 2], i['E', 3], i['E', 4], i['E', 5],
                i['E', 6], i['E', 7], i['E', 8], i['E', 9], i['E', 10],
                i['F', 1], i['F', 2], i['F', 3], i['F', 4], i['F', 5],
                i['F', 6], i['F', 7], i['F', 8], i['F', 9], i['F', 10],
                i['G', 1], i['G', 2], i['G', 3], i['G', 4], i['G', 5],
                i['G', 6], i['G', 7], i['G', 8], i['G', 9], i['G', 10],
                i['H', 1], i['H', 2], i['H', 3], i['H', 4], i['H', 5],
                i['H', 6], i['H', 7], i['H', 8], i['H', 9], i['H', 10],
                i['I', 1], i['I', 2], i['I', 3], i['I', 4], i['I', 5],
                i['I', 6], i['I', 7], i['I', 8], i['I', 9], i['I', 10],
                i['J', 1], i['J', 2], i['J', 3], i['J', 4], i['J', 5],
                i['J', 6], i['J', 7], i['J', 8], i['J', 9], i['J', 10])
            )

    def __position_ships_on_board(self):
        """
        Ships are placed so that no ship touches any other ship, not even diagonally.
        """
        for ship_num, ship_len in enumerate(self.ships_len, 1):
            self.fleet[ship_num] = {}
            while True:
                direction = random.choice([(0, 1), (1, 0)])  # horizontal→(0, 1) vertical↓(1, 0)
                row = random.choice('ABCDEFGHIJ')  # choose row
                col = random.choice(range(1, 11))  # choose column
                temp = {}
                for part in range(ship_len):
                    for a, b in [(0, 0), (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                        try:
                            if self.game_board[chr(ord(row) + part * direction[0] + a), col + part * direction[1] + b] \
                                    != __class__.sym_empty:
                                break
                        except KeyError:
                            if a == 0 and b == 0:
                                break
                    else:
                        temp[(chr(ord(row) + part * direction[0]), col + part * direction[1])] = False
                        continue
                    break
                else:
                    self.fleet[ship_num] = temp
                    for part in self.fleet[ship_num]:
                        self.game_board[part] = __class__.sym_ship
                    break

    def get_user_guess(self):
        while True:  # loop until user provides valid input (row=A-J, col=1-10, and that its an empty cell on board
            try:
                flush_input()  # clear all keystrokes made by user while waiting for opponent
                user = input("{}, Select Row and column (e.g. B8): ".format(self.name))  # get row and column from user
                row = user[0].upper()  # take first character and make it upper case
                col = int(user[1:])  # take the remaining characters and validate they are all digits
                if row in 'ABCDEFGHIJ' and col in range(1, 11):  # check row and col are in range
                    if self.guess_board[row, col] == __class__.sym_empty:  # check that this guess is on an empty cell
                        return row, col  # if all conditions are met return row and col
            except (ValueError, IndexError):
                pass
            except KeyboardInterrupt:
                print("\nBye!")
                sys.exit(0)

    def check_if_hit(self, row, col):
        if self.game_board[row, col] == __class__.sym_ship:
            return True
        return False

    @staticmethod
    def mark_on_board(row, col, hit, board_type):
        if hit:
            board_type[row, col] = __class__.sym_hit
        else:
            board_type[row, col] = __class__.sym_miss

    def mark_on_fleet(self, row, col):
        for ship in self.fleet:
            if (row, col) in self.fleet[ship]:
                self.fleet[ship][row, col] = True
                return ship

    def check_if_ship_destroyed(self, ship):
        for part in self.fleet[ship]:  # check if all parts of the ship got hit
            if self.fleet[ship][part] is False:  # if at least one part wasn't hit return false
                return False
        else:  # if all parts of ship got hit
            return True

    @staticmethod
    def mark_destroyed_ship_on_board(ship, board_type):
        for part in ship:
            board_type[part] = __class__.sym_destroyed
            for a, b in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                try:
                    if board_type[chr(ord(part[0]) + a), part[1] + b] == __class__.sym_empty:
                        board_type[chr(ord(part[0]) + a), part[1] + b] = __class__.sym_miss
                except KeyError:
                    pass


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)


def main():
    try:
        port = 5000

        # parsing arguments #
        parser = argparse.ArgumentParser()
        g = parser.add_mutually_exclusive_group()
        g.add_argument('-c', dest='server_ip', help='Run as Client')
        g.add_argument('-s', dest='server', action='store_true', help='Run as Server')
        args = parser.parse_args()
        if args.server is False and args.server_ip is None:
            parser.error("at least one flag is required")
        ##########

        # handle connection #
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if args.server:
            s.bind(("0.0.0.0", port))
            s.listen(1)
            print('Waiting for opponent to join me at {}:{}'.format(get_ip_address(), port))
            s, addr = s.accept()
            print('Received connection: {}:{}'.format(addr[0], addr[1]))
            my_turn = False
        else:
            s.connect((args.server_ip, port))
            my_turn = True
        ##########

        # get players name and print initial board #
        my_name = input("Enter your name: ")  # get my name
        s.send(dumps(my_name))  # send my name to opponent
        opponent_name = loads(s.recv(1024))  # receive opponent's name
        p = Player(my_name)  # create instance of my player
        p.print_board(my_name, opponent_name)  # print initial boards
        ##########

        # ongoing game #
        while True:  # main game loop
            if my_turn:  # if it is my turn
                row, col = p.get_user_guess()  # get my guess
                s.send(dumps((row, col)))  # send my guess to opponent
                hit = loads(s.recv(1024))  # get opponent's feedback on my guess (hit or miss)
                if hit:  # if I hit one of the opponent's ships
                    msg = "You guessed {}{} - HIT".format(row, col)
                    p.mark_on_board(row, col, True, p.guess_board)  # mark the hit on my guess board
                    ship_destroyed = (loads(s.recv(1024)))  # get opponent notification if I destroyed a ship
                    if ship_destroyed:  # if I destroyed opponent's ship
                        p.mark_destroyed_ship_on_board(ship_destroyed, p.guess_board)  # reveal ship on my guess board
                        p.opponent_ships_destroyed += 1  # increment my opponent's destroyed ship counter
                        if p.opponent_ships_destroyed == len(p.ships_len):  # if all opponent's ships are destroyed
                            break  # stop game main loop
                else:  # if I missed
                    msg = "You guessed {}{} - MISS".format(row, col)
                    p.mark_on_board(row, col, False, p.guess_board)  # mark miss on my guess board
                    my_turn = False  # switch turns
            else:  # if its opponent's turn
                print("Waiting for {} to send his guess".format(opponent_name))  # prompt waiting for opponent
                row, col = loads(s.recv(1024))  # receive guessed row and column from opponent
                if p.check_if_hit(row, col):  # if opponent hit one of my ships
                    msg = "{} guessed {}{} - HIT".format(opponent_name, row, col)
                    s.send(dumps(True))  # notify opponent he hit one of my ships
                    p.mark_on_board(row, col, True, p.game_board)  # mark hit on my game board
                    ship_that_got_hit = p.mark_on_fleet(row, col)  # check which one of my ships got hit
                    if p.check_if_ship_destroyed(ship_that_got_hit):  # if the ship that got hit was destroyed
                        s.send(dumps(p.fleet[ship_that_got_hit]))  # notify coordinates of destroyed a ship to opponent
                        p.mark_destroyed_ship_on_board(p.fleet[ship_that_got_hit],
                                                       p.game_board)  # reveal ship on game board
                        p.my_ships_destroyed += 1  # increment ship destroyed counter
                        if p.my_ships_destroyed == len(p.ships_len):  # if all my ships are destroyed
                            break  # stop game main loop
                    else:  # if the ship that got hit wasn't destroyed
                        s.send(dumps(False))  # notify opponent that the hit didn't destroy a ship
                else:  # if opponent missed
                    msg = "{} guessed {}{} - MISS".format(opponent_name, row, col)
                    s.send(dumps(False))  # notify opponent that he missed
                    p.mark_on_board(row, col, False, p.game_board)  # mark the miss on my game board
                    my_turn = True  # switch turn to opponent
            p.print_board(my_name, opponent_name)  # print updated boards after each turn
            print(msg)
        ##########

        # declare winner #
        p.print_board(my_name, opponent_name)  # print final game board
        if p.my_ships_destroyed > p.opponent_ships_destroyed:  # if opponent destroyed more ships than me
            print("{} is the winner!".format(opponent_name))  # declare opponent as the winner
        else:  # if I destroyed more ships than opponent
            print("{} is the winner!".format(my_name))  # declare me as the winner
        ##########
    except KeyboardInterrupt:
        print("\nBye!")
    except (EOFError, ConnectionAbortedError, ConnectionResetError):
        print("\nopponent has disconnected")
    except ConnectionRefusedError:
        print("Either opponent didn't start server or a network problem")


if __name__ == '__main__':
    main()
