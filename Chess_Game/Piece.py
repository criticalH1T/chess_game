"""
This module contains the Piece class which is a base class for Rook, Knight, Bishop, Pawn, Queen and King
Facilitates the following:
- Each piece has it's own row, column, name and player to which it belongs to
- Finding all possible moves by combining all peaceful moves and all offensive moves found

Note: The class methods are redundant so I wrote docstrings on the first few because all
      other methods with the same name have the same functionality
"""

import abc
from enums import Player


class Piece:
    # Initialize the piece
    def __init__(self, name, row_number, col_number, player):
        self._name = name
        self.row_number = row_number
        self.col_number = col_number
        self._player = player

    # Get the x value
    def get_row_number(self):
        return self.row_number

    # Get the y value
    def get_col_number(self):
        return self.col_number

    # get the name
    def get_name(self):
        return self._name

    # which player the piece belongs to
    def get_player(self):
        return self._player

    # check if same player
    def is_player(self, player_checked):
        return self.get_player() == player_checked

    def change_row_number(self, new_row_number):
        self.row_number = new_row_number

    def change_col_number(self, new_col_number):
        self.col_number = new_col_number

    @abc.abstractmethod
    def get_valid_piece_takes(self, game_state):
        pass

    @abc.abstractmethod
    def get_valid_peaceful_moves(self, game_state):
        pass

    @abc.abstractmethod
    def get_valid_piece_moves(self, board):
        pass


# Rook (R)
class Rook(Piece):
    def __init__(self, name, row_number, col_number, player):
        super().__init__(name, row_number, col_number, player)
        self.has_moved = False  # to update castling rights

    def get_valid_peaceful_moves(self, game_state):
        """
        returns all moves that result in moving without taking piece
        """
        return self.traverse(game_state)[0]

    def get_valid_piece_takes(self, game_state):
        """
        returns all moves that result in taking a piece
        """
        return self.traverse(game_state)[1]

    def get_valid_piece_moves(self, game_state):
        """
        returns the result from the previous two functions
        """
        return self.get_valid_peaceful_moves(game_state) + self.get_valid_piece_takes(game_state)

    def traverse(self, game_state):
        """
        checks all legal moves for the rook
        """
        _peaceful_moves = []
        _piece_takes = []

        up = down = left = right = 1

        # Left of the Rook
        breaking_point = False
        while self.get_col_number() - left >= 0 and not breaking_point:
            W = (self.get_row_number(), self.get_col_number() - left)
            # when the square to the left is empty
            if game_state.get_piece(*W) is Player.EMPTY:
                _peaceful_moves.append(W)
                left += 1
            # when the square contains an opposing piece
            elif game_state.is_valid_piece(*W) and \
                    not game_state.get_piece(*W).is_player(self.get_player()):
                _piece_takes.append(W)
                breaking_point = True
            else:
                breaking_point = True

        # Right of the Rook
        breaking_point = False
        while self.get_col_number() + right < 8 and not breaking_point:
            E = (self.get_row_number(), self.get_col_number() + right)
            # when the square to the left is empty
            if game_state.get_piece(*E) is Player.EMPTY:
                _peaceful_moves.append(E)
                right += 1
            # when the square contains an opposing piece
            elif game_state.is_valid_piece(*E) and \
                    not game_state.get_piece(*E).is_player(self.get_player()):
                _piece_takes.append(E)
                breaking_point = True
            else:
                breaking_point = True

        # Below the Rook
        breaking_point = False
        while self.get_row_number() + down < 8 and not breaking_point:
            S = (self.get_row_number() + down, self.get_col_number())
            # when the square to the left is empty
            if game_state.get_piece(*S) is Player.EMPTY:
                _peaceful_moves.append(S)
                down += 1
            # when the square contains an opposing piece
            elif game_state.is_valid_piece(*S) and \
                    not game_state.get_piece(*S).is_player(self.get_player()):
                _piece_takes.append(S)
                breaking_point = True
            else:
                breaking_point = True

        # Above the Rook
        breaking_point = False
        while self.get_row_number() - up >= 0 and not breaking_point:
            N = (self.get_row_number() - up, self.get_col_number())
            # when the square to the left is empty
            if game_state.get_piece(*N) is Player.EMPTY:
                _peaceful_moves.append(N)
                up += 1
            # when the square contains an opposing piece
            elif game_state.is_valid_piece(*N) and \
                    not game_state.get_piece(*N).is_player(self.get_player()):
                _piece_takes.append(N)
                breaking_point = True
            else:
                breaking_point = True
        return _peaceful_moves, _piece_takes


# Knight (N)
class Knight(Piece):
    def __init__(self, name, row_number, col_number, player):
        super(Knight, self).__init__(name, row_number, col_number, player)
        self.row_change = [-2, -2, -1, -1, +1, +1, +2, +2]  # since the knight jumps, these are his row offsets
        self.col_change = [-1, +1, -2, +2, -2, +2, +1, -1]  # and these are his column offsets

    def get_valid_peaceful_moves(self, game_state):
        """
        returns all moves that result in moving without taking piece
        """
        _moves = []

        for i in range(0, 8):
            new_row = self.get_row_number() + self.row_change[i]
            new_col = self.get_col_number() + self.col_change[i]
            evaluating_square = game_state.get_piece(new_row, new_col)
            # when the square with new_row and new_col is empty
            if evaluating_square == Player.EMPTY:
                _moves.append((new_row, new_col))
        return _moves

    def get_valid_piece_takes(self, game_state):
        """
        returns all moves that result in taking a piece
        """
        _moves = []

        for i in range(0, 8):
            new_row = self.get_row_number() + self.row_change[i]
            new_col = self.get_col_number() + self.col_change[i]
            evaluating_square = game_state.get_piece(new_row, new_col)
            # when the square with new_row and new_col contains a valid piece and the player is different
            if game_state.is_valid_piece(new_row, new_col) and self.get_player() is not evaluating_square.get_player():
                _moves.append((new_row, new_col))
        return _moves

    def get_valid_piece_moves(self, game_state):
        return self.get_valid_peaceful_moves(game_state) + self.get_valid_piece_takes(game_state)


# Bishop
class Bishop(Piece):
    def __init__(self, name, row_number, col_number, player):
        super().__init__(name, row_number, col_number, player)

    def get_valid_piece_takes(self, game_state):
        return self.traverse(game_state)[1]

    def get_valid_peaceful_moves(self, game_state):
        return self.traverse(game_state)[0]

    def get_valid_piece_moves(self, game_state):
        return self.get_valid_piece_takes(game_state) + self.get_valid_peaceful_moves(game_state)

    def traverse(self, game_state):
        _peaceful_moves = []
        _piece_takes = []

        breaking_point = False
        up = 1
        down = 1
        left = 1
        right = 1
        while self.get_col_number() - left >= 0 and self.get_row_number() - up >= 0 and not breaking_point:
            NW = (self.get_row_number() - up, self.get_col_number() - left)  # NW relative position to current square
            # when the square is empty
            if game_state.get_piece(*NW) is Player.EMPTY:
                _peaceful_moves.append(NW)
                left += 1
                up += 1
            # when the square contains an opposing piece
            elif game_state.is_valid_piece(*NW) and \
                    not game_state.get_piece(*NW).is_player(
                        self.get_player()):
                _piece_takes.append(NW)
                breaking_point = True
            else:
                breaking_point = True

        # Right up of the bishop
        breaking_point = False
        up = 1
        left = 1
        while self.get_col_number() + right < 8 and self.get_row_number() - up >= 0 and not breaking_point:
            NE = (self.get_row_number() - up, self.get_col_number() + right)
            # when the square is empty
            if game_state.get_piece(*NE) is Player.EMPTY:
                _peaceful_moves.append(NE)
                right += 1
                up += 1
            # when the square contains an opposing piece
            elif game_state.is_valid_piece(*NE) and \
                    not game_state.get_piece(*NE).is_player(self.get_player()):
                _piece_takes.append(NE)
                breaking_point = True
            else:
                breaking_point = True

        # Down left of the bishop
        breaking_point = False
        up = 1
        right = 1
        while self.get_col_number() - left >= 0 and self.get_row_number() + down < 8 and not breaking_point:
            SW = (self.get_row_number() + down, self.get_col_number() - left)
            # when the square is empty
            if game_state.get_piece(*SW) is Player.EMPTY:
                _peaceful_moves.append(SW)
                down += 1
                left += 1
            # when the square contains an opposing piece
            elif game_state.is_valid_piece(*SW) and \
                    not game_state.get_piece(*SW).is_player(
                        self.get_player()):
                _piece_takes.append(SW)
                breaking_point = True
            else:
                breaking_point = True

        # Down right of the bishop
        breaking_point = False
        down = 1
        left = 1
        while self.get_col_number() + right < 8 and self.get_row_number() + down < 8 and not breaking_point:
            SE = (self.get_row_number() + down, self.get_col_number() + right)
            # when the square is empty
            if game_state.get_piece(*SE) is Player.EMPTY:
                _peaceful_moves.append(SE)
                down += 1
                right += 1
            # when the square contains an opposing piece
            elif game_state.is_valid_piece(*SE) and \
                    not game_state.get_piece(*SE).is_player(
                        self.get_player()):
                _piece_takes.append(SE)
                breaking_point = True
            else:
                breaking_point = True
        return _peaceful_moves, _piece_takes


# Pawn
class Pawn(Piece):
    def __init__(self, name, row_number, col_number, player):
        super(Pawn, self).__init__(name, row_number, col_number, player)

    def move_NW_NE(self, game_state, color):
        _moves = []
        NW = (self.get_row_number() - 1, self.get_col_number() - 1)
        # when the square to the NW (top left) of current has an opposing piece
        if game_state.is_valid_piece(*NW) and not game_state.get_piece(*NW).is_player(color):
            _moves.append(NW)
        NE = (self.get_row_number() - 1, self.get_col_number() + 1)
        # when the square to the NE (top right) of current has an opposing piece
        if game_state.is_valid_piece(*NE) and not game_state.get_piece(*NE).is_player(color):
            _moves.append(NE)
        return _moves

    def move_SW_SE(self, game_state, color):
        _moves = []
        SW = (self.get_row_number() + 1, self.get_col_number() - 1)
        # when the square to the SW (down left) of current has an opposing piece
        if game_state.is_valid_piece(*SW) and not game_state.get_piece(*SW).is_player(color):
            _moves.append(SW)
        SE = (self.get_row_number() + 1, self.get_col_number() + 1)
        # when the square to the SE (down right) of current has an opposing piece
        if game_state.is_valid_piece(*SE) and not game_state.get_piece(*SE).is_player(color):
            _moves.append(SE)
        return _moves

    def move_up(self, game_state):
        _moves = []
        N = (self.get_row_number() - 1, self.get_col_number())
        # when the square above is empty (from white's perspective, we're going up)
        if game_state.get_piece(*N) == Player.EMPTY:
            # when the pawn has not been moved yet
            if self.get_row_number() == 6 and game_state.get_piece(self.get_row_number() - 2,
                                                                   self.get_col_number()) == Player.EMPTY:
                _moves.append(N)  # one square above
                _moves.append((N[0] - 1, N[1]))  # two squares above
            # when the pawn has already moved
            else:
                _moves.append(N)
        return _moves

    def move_down(self, game_state):
        _moves = []
        S = (self.get_row_number() + 1, self.get_col_number())
        # when the square below is empty (from black's perspective, we're going down)
        if game_state.get_piece(*S) == Player.EMPTY:
            # when the pawn has not been moved yet
            if self.get_row_number() == 1 and game_state.get_piece(self.get_row_number() + 2,
                                                                   self.get_col_number()) == Player.EMPTY:
                _moves.append(S)  # one square below
                _moves.append((S[0] + 1, S[1]))  # two squares below
            # when the pawn has been moved
            else:
                _moves.append(S)
        return _moves

    def get_valid_peaceful_moves(self, game_state):
        _moves = []
        # when the pawn is a white piece
        if self.is_player(Player.PLAYER_WHITE):
            if game_state.get_bottom_color() == 'w':
                _moves.extend(self.move_up(game_state))
            else:
                _moves.extend(self.move_down(game_state))

        # when the pawn is a black piece
        elif self.is_player(Player.PLAYER_BLACK):
            if game_state.get_bottom_color() == 'w':
                _moves.extend(self.move_down(game_state))
            else:
                _moves.extend(self.move_up(game_state))
        return _moves

    def get_valid_piece_takes(self, game_state):
        _moves = []
        # when the pawn is a white piece
        if self.is_player(Player.PLAYER_WHITE):
            if game_state.get_bottom_color() == 'w':
                _moves.extend(self.move_NW_NE(game_state, self.get_player()))
            else:
                _moves.extend(self.move_SW_SE(game_state, self.get_player()))
        # when the pawn is a black piece
        elif self.is_player(Player.PLAYER_BLACK):
            if game_state.get_bottom_color() == 'w':
                _moves.extend(self.move_SW_SE(game_state, self.get_player()))
            else:
                _moves.extend(self.move_NW_NE(game_state, self.get_player()))
        return _moves

    def get_valid_piece_moves(self, game_state):
        return self.get_valid_peaceful_moves(game_state) + self.get_valid_piece_takes(game_state)


# Queen
class Queen(Rook, Bishop):
    """
    The queen can move in all directions that both the Rook and Bishop can
    This is why the Queen's valid moves will be the combination of the valid moves of the Rook and Bishop
    """
    def get_valid_peaceful_moves(self, game_state):
        return (Rook.get_valid_peaceful_moves(Rook(self.get_name(), self.get_row_number(), self.get_col_number(), self.get_player()), game_state) +
                Bishop.get_valid_peaceful_moves(Bishop(self.get_name(), self.get_row_number(), self.get_col_number(), self.get_player()), game_state))

    def get_valid_piece_takes(self, game_state):
        return (Rook.get_valid_piece_takes(Rook(self.get_name(), self.get_row_number(), self.get_col_number(), self.get_player()), game_state) +
                Bishop.get_valid_piece_takes(Bishop(self.get_name(), self.get_row_number(), self.get_col_number(), self.get_player()), game_state))

    def get_valid_piece_moves(self, game_state):
        return (Rook.get_valid_piece_moves(Rook(self.get_name(), self.get_row_number(), self.get_col_number(), self.get_player()), game_state) +
                Bishop.get_valid_piece_moves(Bishop(self.get_name(), self.get_row_number(), self.get_col_number(), self.get_player()), game_state))


# King
class King(Piece):
    def __init__(self, name, row_number, col_number, player):
        super(King, self).__init__(name, row_number, col_number, player)
        self.row_change = [-1, +0, +1, -1, +1, -1, +0, +1]  # can move one square in all directions, this is row offset
        self.col_change = [-1, -1, -1, +0, +0, +1, +1, +1]  # and this is column offset

    def get_valid_piece_takes(self, game_state):
        _moves = []

        for i in range(0, 8):
            new_row = self.get_row_number() + self.row_change[i]
            new_col = self.get_col_number() + self.col_change[i]
            evaluating_square = game_state.get_piece(new_row, new_col)
            # when the square with new_row and new_col contains a valid piece
            if game_state.is_valid_piece(new_row, new_col):
                # when the king is white and the piece near the king is black
                if self.is_player(Player.PLAYER_WHITE) and evaluating_square.is_player(Player.PLAYER_BLACK):
                    _moves.append((new_row, new_col))
                # when the king is black and the piece near the king is white
                elif self.is_player(Player.PLAYER_BLACK) and evaluating_square.is_player(Player.PLAYER_WHITE):
                    _moves.append((new_row, new_col))
        return _moves

    def get_valid_peaceful_moves(self, game_state):
        """
        returns all peaceful moves, checks for castling rights, if the king can castle to some side,
        his legal moves get extended with the appropriate square
        """
        _moves = []

        for i in range(0, 8):
            new_row = self.get_row_number() + self.row_change[i]
            new_col = self.get_col_number() + self.col_change[i]
            evaluating_square = game_state.get_piece(new_row, new_col)
            # when the square with new_row and new_col is empty
            if evaluating_square == Player.EMPTY:
                _moves.append((new_row, new_col))

        if game_state.king_can_castle_left(self.get_player()):
            if self.is_player(Player.PLAYER_WHITE):
                if game_state.get_bottom_color() == 'w':
                    _moves.append((7, 2))
                else:
                    _moves.append((0, 1))
            elif self.is_player(Player.PLAYER_BLACK):
                if game_state.get_bottom_color() == 'w':
                    _moves.append((0, 2))
                else:
                    _moves.append((7, 1))
        elif game_state.king_can_castle_right(self.get_player()):
            if self.is_player(Player.PLAYER_WHITE):
                if game_state.get_bottom_color() == 'w':
                    _moves.append((7, 6))
                else:
                    _moves.append((0, 5))
            elif self.is_player(Player.PLAYER_BLACK):
                if game_state.get_bottom_color() == 'w':
                    _moves.append((0, 6))
                else:
                    _moves.append((7, 5))
        return _moves

    def get_valid_piece_moves(self, game_state):
        return self.get_valid_peaceful_moves(game_state) + self.get_valid_piece_takes(game_state)
