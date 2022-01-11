"""
This module contains the main method of the program, where the main loop of the game is contained
Facilitates the following:
- Loading the settings from a config.ini file (some other settings are imported from settings.py)
- Loading piece images, drawing board and pieces on it, highlighting squares when a piece is clicked
- Handling user clicks, and other input and displaying who won at the end of the game
"""
import pygame

import chess_engine
from configparser import ConfigParser
from settings import *
from enums import Player

file = 'config.ini'
config = ConfigParser()
config.read(file)

WIDTH = int(config['SCREEN']['WIDTH'])
HEIGHT = int(config['SCREEN']['HEIGHT']) + OFFSET  # 512 + 128 (OFFSET)
SQ_SIZE = int(config['BOARD']['SQ_SIZE'])


def load_images():
    """
    Load images for the chess pieces
    :return: None
    """
    for p in Player.PIECES:
        IMAGES[p] = py.transform.scale(py.image.load("images/" + p + ".png"), (SQ_SIZE, SQ_SIZE))


def draw_game_state(screen, game_state, valid_moves, square_selected):
    """
    Draw the whole game state
    :param screen: the pygame screen
    :param game_state: GameState object
    :param valid_moves: all the valid moves for the current piece
    :param square_selected: which square we are moving from
    :return:
    """
    draw_bottom_panel(screen, game_state)
    draw_squares(screen)
    check_if_check(screen, game_state)
    highlight_square(screen, game_state, valid_moves, square_selected)
    draw_pieces(screen, game_state)


def draw_bottom_panel(screen, game_state):
    """
    Serves to draw the bottom panel which contains the turn and move number
    :param screen: screen of the game
    :param game_state: current game_state (object of GameState)
    :return: None
    """
    py.draw.rect(screen, py.Color(209, 215, 222), py.Rect(0, HEIGHT - OFFSET, WIDTH, HEIGHT - OFFSET))

    turn = 'White' if game_state.whose_turn() else 'Black'
    move_count = str(game_state.get_move_count())
    font = py.font.SysFont("Helvetica", 32, True, False)

    turn_object = font.render(turn, False, py.Color("Black"))
    width, height = turn_object.get_size()
    x = (WIDTH - width) // 3.5
    y = (OFFSET - height) // 2 + (HEIGHT - OFFSET)
    screen.blit(turn_object, (x, y))

    move_object = font.render(move_count, False, py.Color("Black"))
    width, height = move_object.get_size()
    x = (WIDTH - width) // 1.5
    y = (OFFSET - height) // 2 + (HEIGHT - OFFSET)
    screen.blit(move_object, (x, y))


def draw_squares(screen):
    """
    Helper function to draw the game state, draws all squares
    :param screen: pygame screen
    :return: None
    """
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            py.draw.rect(screen, color, py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, game_state):
    """
    Helper function to draw the game state, draws all pieces on the board
    (the reason I don't draw the squares and pieces together is in order to be able to highlight JUST the squares)
    :param screen: pygame screen
    :param game_state: GameState object
    :return:
    """
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = game_state.get_piece(r, c)
            if piece is not None and piece != Player.EMPTY:
                screen.blit(IMAGES[piece.get_player() + "_" + piece.get_name()],
                            py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))  # example white_r


def draw_check(screen, text):
    """
    Draw "CHECK" at the bottom if a player is in check
    :param screen:
    :param text:
    :return:
    """
    font = py.font.SysFont("Helvetica", 32, True, False)
    checkmate_object = font.render(text, False, py.Color("Red"))

    width, height = checkmate_object.get_size()
    x = (WIDTH - width) // 2
    y = (OFFSET - height) // 2 + (HEIGHT - OFFSET // 1.5)
    screen.blit(checkmate_object, (x, y))


def highlight_check(screen, king_location):
    """
    Puts a red color on king's square if the king is in check
    """
    row = king_location[0]
    col = king_location[1]

    s = py.Surface((SQ_SIZE, SQ_SIZE))
    s.set_alpha(100)
    s.fill(py.Color("red"))
    screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

    draw_check(screen, "Check")


def check_if_check(screen, game_state):
    """
    Checks if the king of player (who is to move) is check
    :param screen: screen of the game
    :param game_state: current game state
    :return: None
    """
    if game_state.whose_turn():
        # if the list of checks is not empty, then white must be in check
        if game_state.check_for_check(game_state.get_white_king_location(), Player.PLAYER_WHITE)[0]:
            highlight_check(screen, game_state.get_white_king_location())
    else:
        if game_state.check_for_check(game_state.get_black_king_location(), Player.PLAYER_BLACK)[0]:
            highlight_check(screen, game_state.get_black_king_location())


def check_if_checkmate(screen, game_state, endgame):
    """
    Check if player is in checkmate
    :param screen: the screen of the game
    :param game_state: current game state
    :param endgame: holds value for state of game, if endgame == 3 then game is still going on
    :return: None
    """
    if endgame == 0:
        game_over = True
        draw_checkmate(screen, "Black wins.")
    elif endgame == 1:
        game_over = True
        draw_checkmate(screen, "White wins.")
    elif endgame == 2:
        game_over = True
        draw_checkmate(screen, "Stalemate.")


def draw_checkmate(screen, text):
    """
    Draws a box stating who won
    :param screen: screen of the board
    :param text: Black wins, White wins or Stalemate
    :return: None
    """
    s = py.Surface((128, 32))
    s.fill(py.Color(209, 215, 222))
    screen.blit(s, (216, 600))
    font = py.font.SysFont("Helvetica", 32, True, False)
    checkmate_object = font.render(text, False, py.Color("Red"))

    width, height = checkmate_object.get_size()
    x = (WIDTH - width) // 2
    y = (OFFSET - height) // 2 + (HEIGHT - OFFSET // 1.5)
    screen.blit(checkmate_object, (x, y))


def highlight_square(screen, game_state, valid_moves, square_selected):
    """
    Takes in the square selected and all it's the valid moves of the piece it holds
    Checks if the turn is the same as the piece color (example white to move and it's a white piece)
    Highlights the selected square in yellow and all legal moves in green
    :param screen: the pygame screen
    :param game_state: GameState object
    :param valid_moves:
    :param square_selected:
    :return: None
    """
    if square_selected != () and game_state.is_valid_piece(square_selected[0], square_selected[1]):
        row = square_selected[0]
        col = square_selected[1]

        # if (it's white's turn and white is moving) or (it's black's turn and black moving)
        if (game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_WHITE)) or \
                (not game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_BLACK)):
            # highlight selected square
            s = py.Surface((SQ_SIZE, SQ_SIZE))  # creating a new Surface
            s.set_alpha(100)  # setting transparency of highlight, takes in (0, 255)
            s.fill(py.Color("yellow"))
            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

            # highlight legal move squares
            s.fill(py.Color("green"))

            for move in valid_moves:
                screen.blit(s, (move[1] * SQ_SIZE, move[0] * SQ_SIZE))


# Main method where loop of the game runs
def main():
    # Check what color the first player wants to be
    while True:
        color = input("What color do you want to play as? (w or b)\n")
        if color == 'w' or color == 'b':
            break
        else:
            print("Enter w or b.\n")

    py.init()
    screen = py.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chess')
    game_state = chess_engine.GameState(color)
    load_images()
    running = True
    square_selected = ()  # keeps track of the last selected square
    player_clicks = []  # keeps track of player clicks (list of two tuples)
    valid_moves = []
    game_over = False

    while running:
        for e in py.event.get():
            if e.type == py.QUIT:
                running = False
            elif e.type == py.MOUSEBUTTONDOWN:
                if not game_over:
                    location = py.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if square_selected == (row, col):  # if player tries to move to square he is currently on
                        square_selected = ()
                        player_clicks = []
                    else:
                        # if player selects opposing piece (example if white to move, but selects black piece)
                        if game_state.is_valid_piece(row, col) and (((not game_state.whose_turn() and
                                game_state.get_piece(row, col).is_player(Player.PLAYER_WHITE)) or
                                (game_state.whose_turn() and
                                game_state.get_piece(row, col).is_player(Player.PLAYER_BLACK)))) and \
                                len(player_clicks) != 1:
                            square_selected = ()
                            player_clicks = []
                        else:
                            square_selected = (row, col)
                            player_clicks.append(square_selected)  # record that player has clicked
                    if len(player_clicks) == 2:
                        if (player_clicks[1][0], player_clicks[1][1]) not in valid_moves:
                            square_selected = ()
                            player_clicks = []
                            valid_moves = []
                        else:
                            game_state.move_piece((player_clicks[0][0], player_clicks[0][1]),
                                                  (player_clicks[1][0], player_clicks[1][1]))
                            square_selected = ()
                            player_clicks = []
                            valid_moves = []
                    else:
                        valid_moves = game_state.get_valid_moves((row, col))
                        if valid_moves is None:
                            valid_moves = []
            elif e.type == py.KEYDOWN:
                if e.key == py.K_r:  # pressing R resets the game
                    game_over = False
                    game_state = chess_engine.GameState(color)
                    valid_moves = []
                    square_selected = ()
                    player_clicks = []
                elif e.key == py.K_u:  # pressing U undoes the move
                    game_state.undo_move()
                    print(len(game_state.move_log))

        draw_game_state(screen, game_state, valid_moves, square_selected)
        endgame = game_state.checkmate_stalemate_checker()
        check_if_checkmate(screen, game_state, endgame)
        py.display.flip()  # refreshes the whole screen
