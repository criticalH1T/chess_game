"""
settings module
"""

import pygame as py

# WIDTH = HEIGHT = 512  # width and height of the chess board 125, 135, 150, 53, 108, 166
# DIMENSION = 8  # the dimensions of the chess board
# SQ_SIZE = HEIGHT // DIMENSION  # the size of each of the squares in the board (64 px)
IMAGES = {}  # dictionary of {name:image} pairs for the chess pieces
colors = [py.Color(232, 235, 239), py.Color(42, 80, 120)]  # white and light blue
DIMENSION = 8  # could not parse to int from config.ini, so I left it here
OFFSET = 128  # this is the extension on the bottom that shows player to move and move count
