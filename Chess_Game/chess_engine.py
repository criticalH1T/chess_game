"""
This module contains the GameState and ChessMove classes
Facilitates the following:
- Instantiating the pieces and board
- Finding legal moves
- Handling moving of pieces
- Handling castling and pawn promotion logic
- Checking if king is in check
- Undoing moves
"""

from Piece import Rook, Knight, Bishop, Queen, King, Pawn
from enums import Player
import csv

'''
r  c     0           1           2           3           4           5           6           7 
0   [(r=0, c=0), (r=0, c=1), (r=0, c=2), (r=0, c=3), (r=0, c=4), (r=0, c=5), (r=0, c=6), (r=0, c=7)]
1   [(r=1, c=0), (r=1, c=1), (r=1, c=2), (r=1, c=3), (r=1, c=4), (r=1, c=5), (r=1, c=6), (r=1, c=7)]
2   [(r=2, c=0), (r=2, c=1), (r=2, c=2), (r=2, c=3), (r=2, c=4), (r=2, c=5), (r=2, c=6), (r=2, c=7)]
3   [(r=3, c=0), (r=3, c=1), (r=3, c=2), (r=3, c=3), (r=3, c=4), (r=3, c=5), (r=3, c=6), (r=3, c=7)]
4   [(r=4, c=0), (r=4, c=1), (r=4, c=2), (r=4, c=3), (r=4, c=4), (r=4, c=5), (r=4, c=6), (r=4, c=7)]
5   [(r=5, c=0), (r=5, c=1), (r=5, c=2), (r=5, c=3), (r=5, c=4), (r=5, c=5), (r=5, c=6), (r=5, c=7)]
6   [(r=6, c=0), (r=6, c=1), (r=6, c=2), (r=6, c=3), (r=6, c=4), (r=6, c=5), (r=6, c=6), (r=6, c=7)]
7   [(r=7, c=0), (r=7, c=1), (r=7, c=2), (r=7, c=3), (r=7, c=4), (r=7, c=5), (r=7, c=6), (r=7, c=7)]
'''


class GameState:
    # Initialize 2D array to represent the chess board
    def __init__(self, bottom_color):
        # The board is a 2D array
        self.white_captives = []
        self.black_captives = []
        self.move_log = []
        self.white_turn = True
        self.checkmate = False
        self.stalemate = False
        self.bottom_color = bottom_color  # used to see if white or black will be on the bottom of the board
        self.board = []

        self._is_check = False
        # Has king not moved, has Rook1(col=0) not moved, has Rook2(col=7) not moved
        self.white_king_can_castle = [True, True, True]
        self.black_king_can_castle = [True, True, True]

        '''
        Reading from csv file
        '''
        self.white_pieces = []
        self.black_pieces = []
        # using absolute paths so the unittests can run
        with open("C:\\AUBG\\2021 Fall Semester\\COS 340\\Chess_Game\\pieces\\white_pieces.csv", "r") as \
                white_pieces_file:
            reader = csv.reader(white_pieces_file)
            for row in reader:
                self.white_pieces.append(row)
        with open("C:\\AUBG\\2021 Fall Semester\\COS 340\\Chess_Game\\pieces\\black_pieces.csv", "r") as \
                black_pieces_file:
            reader = csv.reader(black_pieces_file)
            for row in reader:
                self.black_pieces.append(row)

        if self.bottom_color == 'w':

            # Initialize White Pieces  - 1 indicates left piece, 2 indicates right piece (from our perspective)
            white_rook_1 = Rook('r', 7, 0, Player.PLAYER_WHITE)
            white_rook_2 = Rook('r', 7, 7, Player.PLAYER_WHITE)
            white_knight_1 = Knight('n', 7, 1, Player.PLAYER_WHITE)
            white_knight_2 = Knight('n', 7, 6, Player.PLAYER_WHITE)
            white_bishop_1 = Bishop('b', 7, 2, Player.PLAYER_WHITE)
            white_bishop_2 = Bishop('b', 7, 5, Player.PLAYER_WHITE)
            white_queen = Queen('q', 7, 3, Player.PLAYER_WHITE)
            white_king = King('k', 7, 4, Player.PLAYER_WHITE)
            white_pawn_1 = Pawn('p', 6, 0, Player.PLAYER_WHITE)
            white_pawn_2 = Pawn('p', 6, 1, Player.PLAYER_WHITE)
            white_pawn_3 = Pawn('p', 6, 2, Player.PLAYER_WHITE)
            white_pawn_4 = Pawn('p', 6, 3, Player.PLAYER_WHITE)
            white_pawn_5 = Pawn('p', 6, 4, Player.PLAYER_WHITE)
            white_pawn_6 = Pawn('p', 6, 5, Player.PLAYER_WHITE)
            white_pawn_7 = Pawn('p', 6, 6, Player.PLAYER_WHITE)
            white_pawn_8 = Pawn('p', 6, 7, Player.PLAYER_WHITE)

            self._white_king_location = [7, 4]

            # self.white_pieces = [white_rook_1, white_rook_2, white_knight_1, white_knight_2, white_bishop_1,
            #                      white_bishop_2,
            #                      white_queen, white_king, white_pawn_1, white_pawn_2, white_pawn_3, white_pawn_4,
            #                      white_pawn_5,
            #                      white_pawn_6, white_pawn_7, white_pawn_8]
            # Initialize Black pieces
            black_rook_1 = Rook('r', 0, 0, Player.PLAYER_BLACK)
            black_rook_2 = Rook('r', 0, 7, Player.PLAYER_BLACK)
            black_knight_1 = Knight('n', 0, 1, Player.PLAYER_BLACK)
            black_knight_2 = Knight('n', 0, 6, Player.PLAYER_BLACK)
            black_bishop_1 = Bishop('b', 0, 2, Player.PLAYER_BLACK)
            black_bishop_2 = Bishop('b', 0, 5, Player.PLAYER_BLACK)
            black_queen = Queen('q', 0, 3, Player.PLAYER_BLACK)
            black_king = King('k', 0, 4, Player.PLAYER_BLACK)
            black_pawn_1 = Pawn('p', 1, 0, Player.PLAYER_BLACK)
            black_pawn_2 = Pawn('p', 1, 1, Player.PLAYER_BLACK)
            black_pawn_3 = Pawn('p', 1, 2, Player.PLAYER_BLACK)
            black_pawn_4 = Pawn('p', 1, 3, Player.PLAYER_BLACK)
            black_pawn_5 = Pawn('p', 1, 4, Player.PLAYER_BLACK)
            black_pawn_6 = Pawn('p', 1, 5, Player.PLAYER_BLACK)
            black_pawn_7 = Pawn('p', 1, 6, Player.PLAYER_BLACK)
            black_pawn_8 = Pawn('p', 1, 7, Player.PLAYER_BLACK)

            self._black_king_location = [0, 4]

            # self.black_pieces = [black_rook_1, black_rook_2, black_knight_1, black_knight_2, black_bishop_1,
            #                      black_bishop_2,
            #                      black_queen, black_king, black_pawn_1, black_pawn_2, black_pawn_3, black_pawn_4,
            #                      black_pawn_5,
            #                      black_pawn_6, black_pawn_7, black_pawn_8]
            self.board = [
                [black_rook_1, black_knight_1, black_bishop_1, black_queen, black_king, black_bishop_2, black_knight_2,
                 black_rook_2],
                [black_pawn_1, black_pawn_2, black_pawn_3, black_pawn_4, black_pawn_5, black_pawn_6, black_pawn_7,
                 black_pawn_8],
                [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY,
                 Player.EMPTY],
                [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY,
                 Player.EMPTY],
                [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY,
                 Player.EMPTY],
                [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY,
                 Player.EMPTY],
                [white_pawn_1, white_pawn_2, white_pawn_3, white_pawn_4, white_pawn_5, white_pawn_6, white_pawn_7,
                 white_pawn_8],
                [white_rook_1, white_knight_1, white_bishop_1, white_queen, white_king, white_bishop_2, white_knight_2,
                 white_rook_2]
            ]

        else:
            # Initialize White pieces
            white_rook_1 = Rook('r', 0, 0, Player.PLAYER_WHITE)
            white_rook_2 = Rook('r', 0, 7, Player.PLAYER_WHITE)
            white_knight_1 = Knight('n', 0, 1, Player.PLAYER_WHITE)
            white_knight_2 = Knight('n', 0, 6, Player.PLAYER_WHITE)
            white_bishop_1 = Bishop('b', 0, 2, Player.PLAYER_WHITE)
            white_bishop_2 = Bishop('b', 0, 5, Player.PLAYER_WHITE)
            white_king = King('k', 0, 3, Player.PLAYER_WHITE)
            white_queen = Queen('q', 0, 4, Player.PLAYER_WHITE)
            white_pawn_1 = Pawn('p', 1, 0, Player.PLAYER_WHITE)
            white_pawn_2 = Pawn('p', 1, 1, Player.PLAYER_WHITE)
            white_pawn_3 = Pawn('p', 1, 2, Player.PLAYER_WHITE)
            white_pawn_4 = Pawn('p', 1, 3, Player.PLAYER_WHITE)
            white_pawn_5 = Pawn('p', 1, 4, Player.PLAYER_WHITE)
            white_pawn_6 = Pawn('p', 1, 5, Player.PLAYER_WHITE)
            white_pawn_7 = Pawn('p', 1, 6, Player.PLAYER_WHITE)
            white_pawn_8 = Pawn('p', 1, 7, Player.PLAYER_WHITE)

            self._white_king_location = [0, 3]

            # self.white_pieces = [white_rook_1, white_rook_2, white_knight_1, white_knight_2,
            #                      white_bishop_1, white_bishop_2,
            #                      white_king, white_queen, white_pawn_1, white_pawn_2, white_pawn_3, white_pawn_4,
            #                      white_pawn_5,
            #                      white_pawn_6, white_pawn_7, white_pawn_8]

            # Initialize Black Pieces
            black_rook_1 = Rook('r', 7, 0, Player.PLAYER_BLACK)
            black_rook_2 = Rook('r', 7, 7, Player.PLAYER_BLACK)
            black_knight_1 = Knight('n', 7, 1, Player.PLAYER_BLACK)
            black_knight_2 = Knight('n', 7, 6, Player.PLAYER_BLACK)
            black_bishop_1 = Bishop('b', 7, 2, Player.PLAYER_BLACK)
            black_bishop_2 = Bishop('b', 7, 5, Player.PLAYER_BLACK)
            black_king = King('k', 7, 3, Player.PLAYER_BLACK)
            black_queen = Queen('q', 7, 4, Player.PLAYER_BLACK)
            black_pawn_1 = Pawn('p', 6, 0, Player.PLAYER_BLACK)
            black_pawn_2 = Pawn('p', 6, 1, Player.PLAYER_BLACK)
            black_pawn_3 = Pawn('p', 6, 2, Player.PLAYER_BLACK)
            black_pawn_4 = Pawn('p', 6, 3, Player.PLAYER_BLACK)
            black_pawn_5 = Pawn('p', 6, 4, Player.PLAYER_BLACK)
            black_pawn_6 = Pawn('p', 6, 5, Player.PLAYER_BLACK)
            black_pawn_7 = Pawn('p', 6, 6, Player.PLAYER_BLACK)
            black_pawn_8 = Pawn('p', 6, 7, Player.PLAYER_BLACK)

            self._black_king_location = [7, 3]

            # self.black_pieces = [black_rook_1, black_rook_2, black_knight_1, black_knight_2,
            #                      black_bishop_1, black_bishop_2,
            #                      black_king, black_queen, black_pawn_1, black_pawn_2, black_pawn_3, black_pawn_4,
            #                      black_pawn_5,
            #                      black_pawn_6, black_pawn_7, black_pawn_8]
            self.board = [
                [white_rook_1, white_knight_1, white_bishop_1, white_king, white_queen, white_bishop_2, white_knight_2,
                 white_rook_2],
                [white_pawn_1, white_pawn_2, white_pawn_3, white_pawn_4, white_pawn_5, white_pawn_6, white_pawn_7,
                 white_pawn_8],
                [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY,
                 Player.EMPTY],
                [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY,
                 Player.EMPTY],
                [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY,
                 Player.EMPTY],
                [Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY, Player.EMPTY,
                 Player.EMPTY],
                [black_pawn_1, black_pawn_2, black_pawn_3, black_pawn_4, black_pawn_5, black_pawn_6, black_pawn_7,
                 black_pawn_8],
                [black_rook_1, black_knight_1, black_bishop_1, black_king, black_queen, black_bishop_2, black_knight_2,
                 black_rook_2]
            ]

    def get_move_count(self):
        """
        :return: move count
        """
        return len(self.move_log)

    def get_white_king_location(self):
        """
        returns white king's location
        """
        return self._white_king_location

    def get_black_king_location(self):
        """
        returns black king's location
        """
        return self._black_king_location

    def is_check(self):
        """
        if king is in check
        """
        return self._is_check

    def get_bottom_color(self):
        """
        returns color of pieces that are at bottom of board
        """
        return self.bottom_color

    def get_piece(self, row, col):
        """
        returns the piece at that square
        """
        if (0 <= row < 8) and (0 <= col < 8):
            return self.board[row][col]

    def is_valid_piece(self, row, col):
        """
        If there is a piece at this square, returns True, otherwise False
        """
        evaluated_piece = self.get_piece(row, col)
        return (evaluated_piece is not None) and (evaluated_piece != Player.EMPTY)

    def get_valid_moves(self, starting_square):
        """
        removes pins from valid moves (unless the pinned piece move can get rid of a check and checks is empty)
        removes move from valid moves if the move falls within a check piece's valid move
        if the moving piece is a king, the ending square cannot be in a check
        """

        current_row = starting_square[0]
        current_col = starting_square[1]

        if self.is_valid_piece(current_row, current_col):  # if it's a valid piece, get it's king
            valid_moves = []
            moving_piece = self.get_piece(current_row, current_col)
            if self.get_piece(current_row, current_col).is_player(Player.PLAYER_WHITE):
                king_location = self._white_king_location
            else:
                king_location = self._black_king_location
            # check for pieces that bring you in check, pieces that are pinned, and pieces that are pinning your pieces
            group = self.check_for_check(king_location, moving_piece.get_player())
            checking_pieces = group[0]
            pinned_pieces = group[1]
            # pinned_checks = group[2]
            initial_valid_piece_moves = moving_piece.get_valid_piece_moves(self)  # will take some moves out from this

            # immediate check
            if checking_pieces:
                for move in initial_valid_piece_moves:
                    can_move = True
                    for piece in checking_pieces:
                        # if we're moving the king while he is in check,
                        # make sure he doesn't move in a square where he will be check
                        if moving_piece.get_name() == "k":
                            temp = self.board[current_row][current_col]  # save it's position
                            self.board[current_row][current_col] = Player.EMPTY  # empty it's position
                            temp2 = self.board[move[0]][move[1]]  # one of king's valid moves
                            self.board[move[0]][move[1]] = temp  # move it, to check if it will be check
                            if not self.check_for_check(move, moving_piece.get_player())[0]:
                                pass  # if it isn't in check, it's good
                            else:
                                can_move = False  # if it is, then it can't move there
                            self.board[current_row][current_col] = temp  # put king back in it's place
                            self.board[move[0]][move[1]] = temp2
                        elif move == piece and len(checking_pieces) == 1 and moving_piece.get_name() != "k" and \
                                (current_row, current_col) not in pinned_pieces:
                            pass  # if our piece can capture the checking piece, then go ahead
                        elif move != piece and len(checking_pieces) == 1 and moving_piece.get_name() != "k" and \
                                (current_row, current_col) not in pinned_pieces:  # check if king will be check if moved
                            temp = self.board[move[0]][move[1]]
                            self.board[move[0]][move[1]] = moving_piece
                            self.board[current_row][current_col] = Player.EMPTY
                            if self.check_for_check(king_location, moving_piece.get_player())[0]:
                                can_move = False
                            self.board[current_row][current_col] = moving_piece
                            self.board[move[0]][move[1]] = temp
                        else:
                            can_move = False
                    if can_move:
                        valid_moves.append(move)
                self._is_check = True
            # pinned checks
            elif pinned_pieces and moving_piece.get_name() != "k":
                if starting_square not in pinned_pieces:
                    for move in initial_valid_piece_moves:
                        valid_moves.append(move)
                elif starting_square in pinned_pieces:
                    for move in initial_valid_piece_moves:

                        temp = self.board[move[0]][move[1]]
                        self.board[move[0]][move[1]] = moving_piece
                        self.board[current_row][current_col] = Player.EMPTY
                        if not self.check_for_check(king_location, moving_piece.get_player())[0]:
                            valid_moves.append(move)
                        self.board[current_row][current_col] = moving_piece
                        self.board[move[0]][move[1]] = temp
            else:
                if moving_piece.get_name() == "k":  # check if king will be check in moved square
                    for move in initial_valid_piece_moves:
                        temp = self.board[current_row][current_col]
                        temp2 = self.board[move[0]][move[1]]
                        self.board[current_row][current_col] = Player.EMPTY
                        self.board[move[0]][move[1]] = temp
                        if not self.check_for_check(move, moving_piece.get_player())[0]:
                            valid_moves.append(move)
                        self.board[current_row][current_col] = temp
                        self.board[move[0]][move[1]] = temp2
                else:
                    for move in initial_valid_piece_moves:
                        valid_moves.append(move)
            return valid_moves
        else:
            return None

    # 0 if white lost, 1 if black lost, 2 if stalemate, 3 if not game over
    def checkmate_stalemate_checker(self):
        """
        checks if game is still going on
        """
        all_white_moves = self.get_all_legal_moves(Player.PLAYER_WHITE)
        all_black_moves = self.get_all_legal_moves(Player.PLAYER_BLACK)
        if self.whose_turn() and not all_white_moves:
            return 0  # white lost, black won
        elif not self.whose_turn() and not all_black_moves:
            return 1  # black lost, white won
        elif not all_white_moves and not all_black_moves:
            return 2
        else:
            return 3

    def get_all_legal_moves(self, player):
        """
        returns all legal moves a player can make, used to check if game over in above function
        """
        _all_valid_moves = []
        for row in range(0, 8):
            for col in range(0, 8):
                if self.is_valid_piece(row, col) and self.get_piece(row, col).is_player(player):
                    valid_moves = self.get_valid_moves((row, col))
                    for move in valid_moves:
                        _all_valid_moves.append(((row, col), move))
        return _all_valid_moves

    def king_can_castle_left(self, player):
        """
        checks if the king can castle left
        different logic if white is on bottom or on top and vice versa
        returns boolean
        """
        if self.bottom_color == 'w':
            if player is Player.PLAYER_WHITE:
                return self.white_king_can_castle[0] and self.white_king_can_castle[1] and \
                       self.get_piece(7, 1) is Player.EMPTY and self.get_piece(7, 2) is Player.EMPTY and \
                       self.get_piece(7, 3) is Player.EMPTY and not self._is_check
            else:
                return self.black_king_can_castle[0] and self.black_king_can_castle[1] and \
                       self.get_piece(0, 1) is Player.EMPTY and self.get_piece(0, 2) is Player.EMPTY and \
                       self.get_piece(0, 3) is Player.EMPTY and not self._is_check
        else:
            if player is Player.PLAYER_WHITE:
                return self.white_king_can_castle[0] and self.white_king_can_castle[1] and \
                       self.get_piece(0, 1) is Player.EMPTY and self.get_piece(0, 2) is Player.EMPTY and \
                       not self._is_check
            else:
                return self.black_king_can_castle[0] and self.black_king_can_castle[1] and \
                       self.get_piece(7, 1) is Player.EMPTY and self.get_piece(7, 2) is Player.EMPTY and \
                       not self._is_check

    def king_can_castle_right(self, player):
        """
        checks if the king can castle left
        different logic if white is on bottom or on top and vice versa
        returns boolean
        """
        if self.bottom_color == 'w':
            if player is Player.PLAYER_WHITE:
                return self.white_king_can_castle[0] and self.white_king_can_castle[2] and \
                       self.get_piece(7, 6) is Player.EMPTY and self.get_piece(7, 5) is Player.EMPTY and not \
                       self._is_check
            else:
                return self.black_king_can_castle[0] and self.black_king_can_castle[2] and \
                       self.get_piece(0, 6) is Player.EMPTY and self.get_piece(0, 5) is Player.EMPTY and not \
                       self._is_check
        else:
            if player is Player.PLAYER_WHITE:
                return self.white_king_can_castle[0] and self.white_king_can_castle[2] and \
                       self.get_piece(0, 6) is Player.EMPTY and self.get_piece(0, 5) is Player.EMPTY and \
                       self.get_piece(0, 4) is Player.EMPTY and not self._is_check
            else:
                return self.black_king_can_castle[0] and self.black_king_can_castle[2] and \
                       self.get_piece(7, 6) is Player.EMPTY and self.get_piece(7, 5) is Player.EMPTY and \
                       self.get_piece(7, 4) is Player.EMPTY and not self._is_check

    def promote_pawn(self, starting_square, moved_piece, ending_square):
        """
        handles promotion of pawns
        user chooses what to promote to in terminal, then piece is instantiated and swapped with pawn
        """
        while True:
            new_piece_name = input("Change pawn to (r, n, b, q):\n")
            piece_classes = {"r": Rook, "n": Knight, "b": Bishop, "q": Queen}
            if new_piece_name in piece_classes:
                move = ChessMove(starting_square, ending_square, self, self._is_check)

                new_piece = piece_classes[new_piece_name](new_piece_name, ending_square[0],
                                                          ending_square[1], moved_piece.get_player())
                self.board[ending_square[0]][ending_square[1]] = new_piece
                self.board[moved_piece.get_row_number()][moved_piece.get_col_number()] = Player.EMPTY
                moved_piece.change_row_number(ending_square[0])
                moved_piece.change_col_number(ending_square[1])
                move.pawn_promotion_move(new_piece)
                self.move_log.append(move)
                break
            else:
                print("Please choose from these four: r, n, b, q.\n")

    def handle_white_castling(self, moving_piece, moved_to_piece, starting_square, ending_square):
        """
        handles the castling for white
        different logic when white is on top or bottom
        """
        next_square_row = ending_square[0]  # The integer row value of the ending square
        next_square_col = ending_square[1]  # The integer col value of the ending square
        if self.bottom_color == 'w':
            # left castling
            if moved_to_piece == Player.EMPTY and next_square_col == 2 and self.king_can_castle_left(
                    moving_piece.get_player()):
                move = ChessMove(starting_square, ending_square, self, self._is_check)
                move.castling_move((7, 0), (7, 3), self)
                self.move_log.append(move)
                # move rook
                self.get_piece(7, 0).change_col_number(3)

                self.board[7][3] = self.board[7][0]
                self.board[7][0] = Player.EMPTY

                self.white_king_can_castle[0] = False
                self.white_king_can_castle[1] = False
            # right castling
            elif moved_to_piece == Player.EMPTY and next_square_col == 6 and self.king_can_castle_right(
                    moving_piece.get_player()):
                move = ChessMove(starting_square, ending_square, self, self._is_check)
                move.castling_move((7, 7), (7, 5), self)
                self.move_log.append(move)
                # move rook
                self.get_piece(7, 7).change_col_number(5)

                self.board[7][5] = self.board[7][7]
                self.board[7][7] = Player.EMPTY

                self.white_king_can_castle[0] = False
                self.white_king_can_castle[2] = False
            else:
                move = ChessMove(starting_square, ending_square, self, self._is_check)
                self.move_log.append(move)
                self.white_king_can_castle[0] = False
            self._white_king_location = (next_square_row, next_square_col)
        else:
            if moved_to_piece == Player.EMPTY and next_square_col == 1 and self.king_can_castle_left(
                    moving_piece.get_player()):
                move = ChessMove(starting_square, ending_square, self, self._is_check)
                move.castling_move((0, 0), (0, 2), self)
                self.move_log.append(move)
                # move rook
                self.get_piece(0, 0).change_col_number(2)

                self.board[0][2] = self.board[0][0]
                self.board[0][0] = Player.EMPTY

                self.white_king_can_castle[0] = False
                self.white_king_can_castle[1] = False

            elif moved_to_piece == Player.EMPTY and next_square_col == 5 and self.king_can_castle_right(
                    moving_piece.get_player()):
                move = ChessMove(starting_square, ending_square, self, self._is_check)
                move.castling_move((0, 7), (0, 4), self)
                self.move_log.append(move)
                # move rook
                self.get_piece(0, 7).change_col_number(4)

                self.board[0][4] = self.board[0][7]
                self.board[0][7] = Player.EMPTY

                self.white_king_can_castle[0] = False
                self.white_king_can_castle[2] = False
            else:
                move = ChessMove(starting_square, ending_square, self, self._is_check)
                self.move_log.append(move)
                self.white_king_can_castle[0] = False
            self._white_king_location = (next_square_row, next_square_col)

    def handle_black_castling(self, moving_piece, moved_to_piece, starting_square, ending_square):
        """
        handles the castling for black
        different logic when black is on top or bottom
        """
        next_square_row = ending_square[0]  # The integer row value of the ending square
        next_square_col = ending_square[1]  # The integer col value of the ending square
        # if black is at the top
        if self.bottom_color == 'w':
            if moved_to_piece == Player.EMPTY and next_square_col == 2 and self.king_can_castle_left(
                    moving_piece.get_player()):
                move = ChessMove(starting_square, ending_square, self, self._is_check)
                move.castling_move((0, 0), (0, 3), self)
                self.move_log.append(move)

                self.get_piece(0, 0).change_col_number(3)
                # move rook
                self.board[0][3] = self.board[0][0]
                self.board[0][0] = Player.EMPTY

                self.black_king_can_castle[0] = False
                self.black_king_can_castle[1] = False

            elif moved_to_piece == Player.EMPTY and next_square_col == 6 and self.king_can_castle_right(
                    moving_piece.get_player()):
                move = ChessMove(starting_square, ending_square, self, self._is_check)
                move.castling_move((0, 7), (0, 5), self)
                self.move_log.append(move)

                self.get_piece(0, 7).change_col_number(5)

                # move rook
                self.board[0][5] = self.board[0][7]
                self.board[0][7] = Player.EMPTY

                self.black_king_can_castle[0] = False
                self.black_king_can_castle[2] = False
            else:
                move = ChessMove(starting_square, ending_square, self, self._is_check)
                self.move_log.append(move)
                self.black_king_can_castle[0] = False
            self._black_king_location = (next_square_row, next_square_col)
        # if black is at the bottom
        else:
            if moved_to_piece == Player.EMPTY and next_square_col == 1 and self.king_can_castle_left(
                    moving_piece.get_player()):
                move = ChessMove(starting_square, ending_square, self, self._is_check)
                move.castling_move((7, 0), (7, 2), self)
                self.move_log.append(move)

                self.get_piece(7, 0).change_col_number(2)
                # move rook
                self.board[7][2] = self.board[7][0]
                self.board[7][0] = Player.EMPTY

                self.black_king_can_castle[0] = False
                self.black_king_can_castle[1] = False
            elif moved_to_piece == Player.EMPTY and next_square_col == 5 and self.king_can_castle_right(
                    moving_piece.get_player()):
                move = ChessMove(starting_square, ending_square, self, self._is_check)
                move.castling_move((7, 7), (7, 4), self)
                self.move_log.append(move)

                self.get_piece(7, 7).change_col_number(4)

                # move rook
                self.board[7][4] = self.board[7][7]
                self.board[7][7] = Player.EMPTY

                self.black_king_can_castle[0] = False
                self.black_king_can_castle[2] = False
            else:
                move = ChessMove(starting_square, ending_square, self, self._is_check)
                self.move_log.append(move)
                self.black_king_can_castle[0] = False
            self._black_king_location = (next_square_row, next_square_col)

    # Move a piece
    def move_piece(self, starting_square, ending_square):
        """
        handles moving of a piece, some special conditions apply for king, rook and pawn
        if we're moving the king to a square where he can castle and he is allowed to castle, then handle castling
        if we're moving the rook, the set the player's castling rights to false for that side
        if pawn is being promoted, promote_pawn handles it and we don't have to move there
        this is why I used the 'temp' variable as a flag in order not to move empty square to promoted square
        if temp is True, which means we haven't done a promotion, then move piece
        add move to move_log which will serve for undoing moves
        returns: None
        """
        current_square_row = starting_square[0]  # The integer row value of the starting square
        current_square_col = starting_square[1]  # The integer col value of the starting square
        next_square_row = ending_square[0]  # The integer row value of the ending square
        next_square_col = ending_square[1]  # The integer col value of the ending square

        # if valid piece and (white turn and white moving) or (black turn and black moving)
        if self.is_valid_piece(current_square_row, current_square_col) and \
                (((self.whose_turn() and self.get_piece(current_square_row, current_square_col).is_player(
                    Player.PLAYER_WHITE)) or
                  (not self.whose_turn() and self.get_piece(current_square_row, current_square_col).is_player(
                      Player.PLAYER_BLACK)))):

            # The chess piece at the starting square
            moving_piece = self.get_piece(current_square_row, current_square_col)

            valid_moves = self.get_valid_moves(starting_square)

            temp = True

            if ending_square in valid_moves:
                moved_to_piece = self.get_piece(next_square_row, next_square_col)
                if moving_piece.get_name() == "k":
                    if moving_piece.is_player(Player.PLAYER_WHITE):
                        self.handle_white_castling(moving_piece, moved_to_piece, starting_square, ending_square)
                    else:
                        self.handle_black_castling(moving_piece, moved_to_piece, starting_square, ending_square)
                elif moving_piece.get_name() == "r":
                    if moving_piece.is_player(Player.PLAYER_WHITE) and current_square_col == 0:
                        self.white_king_can_castle[1] = False
                    elif moving_piece.is_player(Player.PLAYER_WHITE) and current_square_col == 7:
                        self.white_king_can_castle[2] = False
                    elif moving_piece.is_player(Player.PLAYER_BLACK) and current_square_col == 0:
                        self.white_king_can_castle[1] = False
                    elif moving_piece.is_player(Player.PLAYER_BLACK) and current_square_col == 7:
                        self.white_king_can_castle[2] = False
                    self.move_log.append(ChessMove(starting_square, ending_square, self, self._is_check))
                elif moving_piece.get_name() == "p":
                    # Promoting white pawn
                    if moving_piece.is_player(Player.PLAYER_WHITE):
                        if self.bottom_color == 'w' and next_square_row == 0:
                            self.promote_pawn(starting_square, moving_piece, ending_square)
                            temp = False
                        elif self.bottom_color == 'b' and next_square_row == 7:
                            self.promote_pawn(starting_square, moving_piece, ending_square)
                            temp = False
                    # Promoting black pawn
                    if moving_piece.is_player(Player.PLAYER_BLACK):
                        if self.bottom_color == 'w' and next_square_row == 7:
                            self.promote_pawn(starting_square, moving_piece, ending_square)
                            temp = False
                        elif self.bottom_color == 'b' and next_square_row == 0:
                            self.promote_pawn(starting_square, moving_piece, ending_square)
                            temp = False
                    # Moving pawn forward by two
                    if abs(next_square_row - current_square_row) == 2 and current_square_col == next_square_col:
                        self.move_log.append(ChessMove(starting_square, ending_square, self, self._is_check))
                    # moving forward by one or taking a piece
                    else:
                        self.move_log.append(ChessMove(starting_square, ending_square, self, self._is_check))
                else:
                    self.move_log.append(ChessMove(starting_square, ending_square, self, self._is_check))

                if temp:
                    moving_piece.change_row_number(next_square_row)
                    moving_piece.change_col_number(next_square_col)
                    self.board[next_square_row][next_square_col] = self.board[current_square_row][current_square_col]
                    self.board[current_square_row][current_square_col] = Player.EMPTY

                self.white_turn = not self.white_turn

            else:
                pass

    def undo_move(self):
        """
        handles reversing a move, does so by taking last move from move_log and doing it backwards
        handles special cases such as restoring castling rights and pawn demotions
        if it comes back to the first move, will print 'Back to the beginning!'
        """
        if self.move_log:
            undoing_move = self.move_log.pop()
            if undoing_move.castled is True:
                self.board[undoing_move.starting_square_row][
                    undoing_move.starting_square_col] = undoing_move.moving_piece
                self.board[undoing_move.ending_square_row][undoing_move.ending_square_col] = undoing_move.removed_piece
                self.get_piece(undoing_move.starting_square_row, undoing_move.starting_square_col).change_row_number(
                    undoing_move.starting_square_row)
                self.get_piece(undoing_move.starting_square_row, undoing_move.starting_square_col).change_col_number(
                    undoing_move.starting_square_col)

                self.board[undoing_move.rook_starting_square[0]][
                    undoing_move.rook_starting_square[1]] = undoing_move.moving_rook
                self.board[undoing_move.rook_ending_square[0]][undoing_move.rook_ending_square[1]] = Player.EMPTY
                undoing_move.moving_rook.change_row_number(undoing_move.rook_starting_square[0])
                undoing_move.moving_rook.change_col_number(undoing_move.rook_starting_square[1])
                if undoing_move.moving_piece is Player.PLAYER_WHITE:
                    if undoing_move.rook_starting_square[1] == 0:
                        self.white_king_can_castle[0] = True
                        self.white_king_can_castle[1] = True
                    elif undoing_move.rook_starting_square[1] == 7:
                        self.white_king_can_castle[0] = True
                        self.white_king_can_castle[2] = True
                else:
                    if undoing_move.rook_starting_square[1] == 0:
                        self.black_king_can_castle[0] = True
                        self.black_king_can_castle[1] = True
                    elif undoing_move.rook_starting_square[1] == 7:
                        self.black_king_can_castle[0] = True
                        self.black_king_can_castle[2] = True
            elif undoing_move.pawn_promoted is True:
                self.board[undoing_move.starting_square_row][
                    undoing_move.starting_square_col] = undoing_move.moving_piece
                self.get_piece(undoing_move.starting_square_row, undoing_move.starting_square_col).change_row_number(
                    undoing_move.starting_square_row)
                self.get_piece(undoing_move.starting_square_row, undoing_move.starting_square_col).change_col_number(
                    undoing_move.starting_square_col)

                self.board[undoing_move.ending_square_row][undoing_move.ending_square_col] = undoing_move.removed_piece
                if undoing_move.removed_piece != Player.EMPTY:
                    self.get_piece(undoing_move.ending_square_row, undoing_move.ending_square_col).change_row_number(
                        undoing_move.ending_square_row)
                    self.get_piece(undoing_move.ending_square_row, undoing_move.ending_square_col).change_col_number(
                        undoing_move.ending_square_col)
            else:
                self.board[undoing_move.starting_square_row][
                    undoing_move.starting_square_col] = undoing_move.moving_piece
                self.get_piece(undoing_move.starting_square_row, undoing_move.starting_square_col).change_row_number(
                    undoing_move.starting_square_row)
                self.get_piece(undoing_move.starting_square_row, undoing_move.starting_square_col).change_col_number(
                    undoing_move.starting_square_col)

                self.board[undoing_move.ending_square_row][undoing_move.ending_square_col] = undoing_move.removed_piece
                if undoing_move.removed_piece != Player.EMPTY:
                    self.get_piece(undoing_move.ending_square_row, undoing_move.ending_square_col).change_row_number(
                        undoing_move.ending_square_row)
                    self.get_piece(undoing_move.ending_square_row, undoing_move.ending_square_col).change_col_number(
                        undoing_move.ending_square_col)

            self.white_turn = not self.white_turn

            if undoing_move.moving_piece.get_name() == "k" and undoing_move.moving_piece.get_player() is \
                    Player.PLAYER_WHITE:
                self._white_king_location = (undoing_move.starting_square_row, undoing_move.starting_square_col)
            elif undoing_move.moving_piece.get_name() == "k" and undoing_move.moving_piece.get_player() is \
                    Player.PLAYER_BLACK:
                self._black_king_location = (undoing_move.starting_square_row, undoing_move.starting_square_col)

            return undoing_move
        else:
            print("Back to the beginning!")

    # true if white, false if black
    def whose_turn(self):
        """
        returns current turn
        """
        return self.white_turn

    def check_for_check(self, king_location, player):
        """
        check for immediate check
        - check 8 directions and 8 knight squares
        check for pins
        - whatever blocked from above is a pin
        - if immediate check, change check value to true
        - list valid moves to prevent check but not remove pin
        - if there are no valid moves to prevent check, checkmate
        """
        self._is_check = False
        _checks = []
        _pins = []
        _pins_check = []

        king_location_row = king_location[0]
        king_location_col = king_location[1]

        up = down = left = right = 1

        # Left of the king
        _possible_pin = ()
        while king_location_col - left >= 0 and self.get_piece(king_location_row, king_location_col - left) is not None:
            if self.is_valid_piece(king_location_row, king_location_col - left) and \
                    self.get_piece(king_location_row, king_location_col - left).is_player(player) and \
                    self.get_piece(king_location_row, king_location_col - left).get_name() != "k":
                if not _possible_pin:
                    _possible_pin = (king_location_row, king_location_col - left)
                else:
                    break
            elif self.is_valid_piece(king_location_row, king_location_col - left) and \
                    not self.get_piece(king_location_row, king_location_col - left).is_player(player):
                if _possible_pin:
                    temp = self.board[_possible_pin[0]][_possible_pin[1]]
                    self.board[_possible_pin[0]][_possible_pin[1]] = Player.EMPTY
                    if (king_location_row, king_location_col) in \
                            self.get_piece(king_location_row, king_location_col - left).get_valid_piece_takes(self):
                        _pins.append(_possible_pin)
                        _pins_check.append((king_location_row, king_location_col - left))
                    self.board[_possible_pin[0]][_possible_pin[1]] = temp
                else:
                    if (king_location_row, king_location_col) in \
                            self.get_piece(king_location_row, king_location_col - left).get_valid_piece_takes(self):
                        # self._is_check = True
                        _checks.append((king_location_row, king_location_col - left))
                break
            left += 1

        # right of the king
        _possible_pin = ()
        while king_location_col + right < 8 and self.get_piece(king_location_row,
                                                               king_location_col + right) is not None:
            if self.is_valid_piece(king_location_row, king_location_col + right) and \
                    self.get_piece(king_location_row, king_location_col + right).is_player(player) and \
                    self.get_piece(king_location_row, king_location_col + right).get_name() != "k":
                if not _possible_pin:
                    _possible_pin = (king_location_row, king_location_col + right)
                else:
                    break
            elif self.is_valid_piece(king_location_row, king_location_col + right) and \
                    not self.get_piece(king_location_row, king_location_col + right).is_player(player):
                if _possible_pin:
                    temp = self.board[_possible_pin[0]][_possible_pin[1]]
                    self.board[_possible_pin[0]][_possible_pin[1]] = Player.EMPTY
                    if (king_location_row, king_location_col) in \
                            self.get_piece(king_location_row, king_location_col + right).get_valid_piece_takes(self):
                        _pins.append(_possible_pin)
                        _pins_check.append((king_location_row, king_location_col + right))
                    self.board[_possible_pin[0]][_possible_pin[1]] = temp
                else:
                    if (king_location_row, king_location_col) in \
                            self.get_piece(king_location_row, king_location_col + right).get_valid_piece_takes(self):
                        # self._is_check = True
                        _checks.append((king_location_row, king_location_col + right))
                break
            right += 1

        # below the king
        _possible_pin = ()
        while king_location_row + down < 8 and self.get_piece(king_location_row + down, king_location_col) is not None:
            if self.is_valid_piece(king_location_row + down, king_location_col) and \
                    self.get_piece(king_location_row + down, king_location_col).is_player(player) and \
                    self.get_piece(king_location_row + down, king_location_col).get_name() != "k":
                if not _possible_pin:
                    _possible_pin = (king_location_row + down, king_location_col)
                else:
                    break
            elif self.is_valid_piece(king_location_row + down, king_location_col) and \
                    not self.get_piece(king_location_row + down, king_location_col).is_player(player):
                if _possible_pin:
                    temp = self.board[_possible_pin[0]][_possible_pin[1]]
                    self.board[_possible_pin[0]][_possible_pin[1]] = Player.EMPTY
                    if (king_location_row, king_location_col) in \
                            self.get_piece(king_location_row + down, king_location_col).get_valid_piece_takes(self):
                        _pins.append(_possible_pin)
                        _pins_check.append((king_location_row + down, king_location_col))
                    self.board[_possible_pin[0]][_possible_pin[1]] = temp
                else:
                    if (king_location_row, king_location_col) in \
                            self.get_piece(king_location_row + down, king_location_col).get_valid_piece_takes(self):
                        # self._is_check = True
                        _checks.append((king_location_row + down, king_location_col))
                break
            down += 1

        # above the king
        _possible_pin = ()
        while king_location_row - up >= 0 and self.get_piece(king_location_row - up, king_location_col) is not None:
            if self.is_valid_piece(king_location_row - up, king_location_col) and \
                    self.get_piece(king_location_row - up, king_location_col).is_player(player) and \
                    self.get_piece(king_location_row - up, king_location_col).get_name() != "k":
                if not _possible_pin:
                    _possible_pin = (king_location_row - up, king_location_col)
                else:
                    break
            elif self.is_valid_piece(king_location_row - up, king_location_col) and \
                    not self.get_piece(king_location_row - up, king_location_col).is_player(player):
                if _possible_pin:
                    temp = self.board[_possible_pin[0]][_possible_pin[1]]
                    self.board[_possible_pin[0]][_possible_pin[1]] = Player.EMPTY
                    if (king_location_row, king_location_col) in \
                            self.get_piece(king_location_row - up, king_location_col).get_valid_piece_takes(self):
                        _pins.append(_possible_pin)
                        _pins_check.append((king_location_row - up, king_location_col))
                    self.board[_possible_pin[0]][_possible_pin[1]] = temp
                else:
                    if (king_location_row, king_location_col) in \
                            self.get_piece(king_location_row - up, king_location_col).get_valid_piece_takes(self):
                        # self._is_check = True
                        _checks.append((king_location_row - up, king_location_col))
                break
            up += 1

        # left up
        up = 1
        left = 1
        _possible_pin = ()
        while king_location_col - left >= 0 and king_location_row - up >= 0 and \
                self.get_piece(king_location_row - up, king_location_col - left) is not None:
            if self.is_valid_piece(king_location_row - up, king_location_col - left) and \
                    self.get_piece(king_location_row - up, king_location_col - left).is_player(player) and \
                    self.get_piece(king_location_row - up, king_location_col - left).get_name() != "k":
                if not _possible_pin:
                    _possible_pin = (king_location_row - up, king_location_col - left)
                else:
                    break
            elif self.is_valid_piece(king_location_row - up, king_location_col - left) and \
                    not self.get_piece(king_location_row - up, king_location_col - left).is_player(player):
                if _possible_pin:
                    temp = self.board[_possible_pin[0]][_possible_pin[1]]
                    self.board[_possible_pin[0]][_possible_pin[1]] = Player.EMPTY
                    if (king_location_row, king_location_col) in \
                            self.get_piece(king_location_row - up, king_location_col - left).get_valid_piece_takes(
                                self):
                        _pins.append(_possible_pin)
                        _pins_check.append((king_location_row - up, king_location_col - left))
                    self.board[_possible_pin[0]][_possible_pin[1]] = temp
                else:
                    if (king_location_row, king_location_col) in \
                            self.get_piece(king_location_row - up, king_location_col - left).get_valid_piece_takes(
                                self):
                        # self._is_check = True
                        _checks.append((king_location_row - up, king_location_col - left))
                break
            left += 1
            up += 1

        # right up
        up = 1
        right = 1
        _possible_pin = ()
        while king_location_col + right < 8 and king_location_row - up >= 0 and \
                self.get_piece(king_location_row - up, king_location_col + right) is not None:
            if self.is_valid_piece(king_location_row - up, king_location_col + right) and \
                    self.get_piece(king_location_row - up, king_location_col + right).is_player(player) and \
                    self.get_piece(king_location_row - up, king_location_col + right).get_name() != "k":
                if not _possible_pin:
                    _possible_pin = (king_location_row - up, king_location_col + right)
                else:
                    break
            elif self.is_valid_piece(king_location_row - up, king_location_col + right) and \
                    not self.get_piece(king_location_row - up, king_location_col + right).is_player(player):
                if _possible_pin:
                    temp = self.board[_possible_pin[0]][_possible_pin[1]]
                    self.board[_possible_pin[0]][_possible_pin[1]] = Player.EMPTY
                    if (king_location_row, king_location_col) in \
                            self.get_piece(king_location_row - up, king_location_col + right).get_valid_piece_takes(
                                self):
                        _pins.append(_possible_pin)
                        _pins_check.append((king_location_row - up, king_location_col + right))
                    self.board[_possible_pin[0]][_possible_pin[1]] = temp
                else:
                    if (king_location_row, king_location_col) in \
                        self.get_piece(king_location_row - up,
                                       king_location_col + right).get_valid_piece_takes(self):
                        # self._is_check = True
                        _checks.append((king_location_row - up, king_location_col + right))
                break
            right += 1
            up += 1

        # left down
        down = 1
        left = 1
        _possible_pin = ()
        while king_location_col - left >= 0 and king_location_row + down < 8 and \
                self.get_piece(king_location_row + down, king_location_col - left) is not None:
            if self.is_valid_piece(king_location_row + down, king_location_col - left) and \
                    self.get_piece(king_location_row + down, king_location_col - left).is_player(player) and \
                    self.get_piece(king_location_row + down, king_location_col - left).get_name() != "k":
                if not _possible_pin:
                    _possible_pin = (king_location_row + down, king_location_col - left)
                else:
                    break
            elif self.is_valid_piece(king_location_row + down, king_location_col - left) and \
                    not self.get_piece(king_location_row + down, king_location_col - left).is_player(player):
                if _possible_pin:
                    temp = self.board[_possible_pin[0]][_possible_pin[1]]
                    self.board[_possible_pin[0]][_possible_pin[1]] = Player.EMPTY
                    if (king_location_row, king_location_col) in \
                            self.get_piece(king_location_row + down,
                                           king_location_col - left).get_valid_piece_takes(self):
                        _pins.append(_possible_pin)
                        _pins_check.append((king_location_row + down, king_location_col - left))
                    self.board[_possible_pin[0]][_possible_pin[1]] = temp
                else:
                    if (king_location_row, king_location_col) in \
                            self.get_piece(king_location_row + down,
                                           king_location_col - left).get_valid_piece_takes(self):
                        # self._is_check = True
                        _checks.append((king_location_row + down, king_location_col - left))
                break
            left += 1
            down += 1

        # right down
        down = 1
        right = 1
        _possible_pin = ()
        while king_location_col + right < 8 and king_location_row + down < 8 and \
                self.get_piece(king_location_row + down, king_location_col + right) is not None:
            if self.is_valid_piece(king_location_row + down, king_location_col + right) and \
                    self.get_piece(king_location_row + down, king_location_col + right).is_player(player) and \
                    self.get_piece(king_location_row + down, king_location_col + right).get_name() != "k":
                if not _possible_pin:
                    _possible_pin = (king_location_row + down, king_location_col + right)
                else:
                    break
            elif self.is_valid_piece(king_location_row + down, king_location_col + right) and \
                    not self.get_piece(king_location_row + down, king_location_col + right).is_player(player):
                if _possible_pin:
                    temp = self.board[_possible_pin[0]][_possible_pin[1]]
                    self.board[_possible_pin[0]][_possible_pin[1]] = Player.EMPTY
                    if (king_location_row, king_location_col) in \
                            self.get_piece(king_location_row + down,
                                           king_location_col + right).get_valid_piece_takes(self):
                        _pins.append(_possible_pin)
                        _pins_check.append((king_location_row + down, king_location_col + right))
                    self.board[_possible_pin[0]][_possible_pin[1]] = temp
                else:
                    if (king_location_row, king_location_col) in \
                            self.get_piece(king_location_row + down,
                                           king_location_col + right).get_valid_piece_takes(self):
                        # self._is_check = True
                        _checks.append((king_location_row + down, king_location_col + right))
                break
            right += 1
            down += 1

        # knights
        row_change = [-2, -2, -1, -1, +1, +1, +2, +2]
        col_change = [-1, +1, -2, +2, -2, +2, +1, -1]
        for i in range(0, 8):
            if self.is_valid_piece(king_location_row + row_change[i], king_location_col + col_change[i]) and \
                    not self.get_piece(king_location_row + row_change[i], king_location_col + col_change[i]).is_player(
                        player):
                if (king_location_row, king_location_col) in self.get_piece(king_location_row + row_change[i],
                                                                            king_location_col + col_change[
                                                                                i]).get_valid_piece_takes(self):
                    # self._is_check = True
                    _checks.append((king_location_row + row_change[i], king_location_col + col_change[i]))
        return [_checks, _pins, _pins_check]


class ChessMove:
    def __init__(self, starting_square, ending_square, game_state, in_check):
        self.starting_square_row = starting_square[0]
        self.starting_square_col = starting_square[1]
        self.moving_piece = game_state.get_piece(self.starting_square_row, self.starting_square_col)
        self.in_check = in_check

        self.ending_square_row = ending_square[0]
        self.ending_square_col = ending_square[1]
        if game_state.is_valid_piece(self.ending_square_row, self.ending_square_col):
            self.removed_piece = game_state.get_piece(self.ending_square_row, self.ending_square_col)
        else:
            self.removed_piece = Player.EMPTY

        # serve to restore castling rights in undo_move()
        self.castled = False
        self.rook_starting_square = None
        self.rook_ending_square = None
        self.moving_rook = None

        self.pawn_promoted = False
        self.replacement_piece = None

    def castling_move(self, rook_starting_square, rook_ending_square, game_state):
        self.castled = True
        self.rook_starting_square = rook_starting_square
        self.rook_ending_square = rook_ending_square
        self.moving_rook = game_state.get_piece(rook_starting_square[0], rook_starting_square[1])

    def pawn_promotion_move(self, new_piece):
        self.pawn_promoted = True
        self.replacement_piece = new_piece

    def get_moving_piece(self):
        return self.moving_piece
