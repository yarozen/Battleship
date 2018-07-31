import random
import sys
import socket


class Player:
    ships_len = (4, 3, 3, 2, 2, 2, 1, 1, 1, 1)
    sym_ship = '@'
    sym_hit = 'x'
    sym_miss = '~'
    sym_destroyed = '%'
    sym_empty = '.'

    def __init__(self, name):
        self.name = name
        self.fleet = {}
        self.game_board = self.__create_empty_board()
        self.guess_board = self.__create_empty_board()
        self.__position_ships_on_board()
        self.ships_destroyed = 0

    @staticmethod
    def __create_empty_board():
        temp = {}
        for x in 'ABCDEFGHIJ':
            for y in range(1, 11):
                temp[x, y] = __class__.sym_empty
        return temp

    def print_board(self, me, opponent):
        for i in (self.game_board, self.guess_board):
            if i == self.game_board:
                print("{}\n{}".format(me, '-' * len(self.name)))
            else:
                print("{}\n{}".format(opponent, '-' * len(self.name)))
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
                            if self.game_board[chr(ord(row) + part*direction[0] + a), col + part*direction[1] + b] \
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
        while True:
            try:
                user = str(input("{}, Select Row and column (e.g. B8): ".format(self.name)))
                row = user[0].upper()
                col = int(user[1:])
                if row in 'ABCDEFGHIJ' and col in range(1, 11):
                    if self.guess_board[row, col] == __class__.sym_empty:
                        return [row, col]
            except ValueError:
                pass
            except IndexError:
                pass
            except KeyboardInterrupt:
                sys.exit(0)
    
    def check_if_hit(self, row, col):
        if self.game_board[row, col] == __class__.sym_ship:
            return True
        return False

    def mark_on_guess_board(self, row, col, symbol):
        self.guess_board[row, col] = symbol

    def mark_on_game_board(self, row, col, symbol):
        self.game_board[row, col] = symbol

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

    def mark_destroyed_ship_in_guess_board(self, ship):
        for part in ship:
            self.guess_board[part] = '%'
            for a, b in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                try:
                    if self.guess_board[chr(ord(part[0]) + a), part[1] + b] == __class__.sym_empty:
                        self.guess_board[chr(ord(part[0]) + a), part[1] + b] = __class__.sym_miss
                except KeyError:
                    pass

    def mark_destroyed_ship_in_game_board(self, ship):
        for part in ship:
            self.game_board[part] = '%'
            for a, b in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                try:
                    if self.game_board[chr(ord(part[0]) + a), part[1] + b] == __class__.sym_empty:
                        self.game_board[chr(ord(part[0]) + a), part[1] + b] = __class__.sym_miss
                except KeyError:
                    pass


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def main():
    ###
    if len(sys.argv) != 2 or sys.argv[1] != "client" and sys.argv[1] != "server":
        print("Usage: {} [client|server]".format(__file__))
        sys.exit(1)
    mode = sys.argv[1]
    port = 5000
    my_turn = True
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if mode == "server":
        s.bind(("0.0.0.0", port))
        s.listen(1)
        print('Waiting for opponent to join me at {}:{}'.format(get_ip_address(), port))
        s, addr = s.accept()
        print('Received connection: {}:{}'.format(addr[0], addr[1]))
        my_turn = False
    elif mode == "client":
        s.connect(("127.0.0.1", port))
    me = input("Enter your name: ")
    s.send(me.encode())
    opponent = s.recv(1024).decode()
    p = Player(me)
    p.print_board(me, opponent)
    while p.ships_destroyed < len(p.ships_len):
        if my_turn:
            row, col = p.get_user_guess()
            s.send("{},{}".format(row, col).encode())
            if s.recv(1024).decode() == "True":
                p.mark_on_guess_board(row, col, 'x')
            else:
                my_turn = False
        else:
            print("Waiting for {} to send his guess".format(opponent))
            row, col = s.recv(1024).decode().split(',')
            col = int(col)
            if p.check_if_hit(row, col):
                p.mark_on_game_board(row, col, 'x')
                ship = p.mark_on_fleet(row, col)
                if p.check_if_ship_destroyed(ship):
                    p.mark_destroyed_ship_in_game_board(p.fleet[ship])
                    print(p.fleet[ship])
                    p.ships_destroyed += 1
                s.send("True".encode())
            else:
                p.mark_on_game_board(row, col, '~')
                s.send("False".encode())
                my_turn = True
        p.print_board(me, opponent)
    print("{} is the winner!".format(cur.name))


if __name__ == '__main__':
    main()
