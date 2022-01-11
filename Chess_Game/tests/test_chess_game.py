import unittest
import sys
sys.path.insert(0, '..')  # need to add parent directory for chess_engine to be visible
import settings
from chess_gui import *
from chess_engine import *


class TestChessGame(unittest.TestCase):

    def setUp(self) -> None:
        self.__game_state = GameState('w') # object to be used for calling methods from chess_engine

    def tearDown(self) -> None:
        del self.__game_state

    def test_move_piece(self):
        self.assertIsNone(self.__game_state.move_piece((0, 0), (1, 1)))

    def test_get_move_count(self):
        self.assertIsInstance(self.__game_state.get_move_count(), int)

    # make sure something that is out of the board is None
    def test_is_valid_piece(self):
        self.assertIsNone(self.__game_state.get_piece(153, 123))

    def test_get_piece(self):
        self.assertIsInstance(self.__game_state.get_piece(0, 0), Rook)

    def test_get_valid_moves(self):
        self.assertIsInstance(self.__game_state.get_valid_moves((1, 0)), list)

    def test_undo_move(self):
        self.assertIsNone(self.__game_state.undo_move(), None)

    def test_check_for_check(self):
        self.assertIsInstance(self.__game_state.check_for_check((7, 4), Player.PLAYER_WHITE), list)

    def test_handle_white_castling(self):
        king = King("k", 7, 4, Player.PLAYER_WHITE)
        self.assertIsNone(self.__game_state.handle_white_castling(king, Player.EMPTY, (7, 4), (7, 2)))

if __name__ == '__main__':
    unittest.main()
