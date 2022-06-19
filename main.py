import pygame as p
import board

# General Dimensions needed for the chess board
# Pixel size of each tile
# Number of Tiles
# Size of entire GUI
tile_dim = 45
num_tiles = 8
display_dim = 360

# Pygame Initialization of the Chessboard
# Calls Board class and assigns it chessboard object
p.init()
board_display = p.display.set_mode((display_dim, display_dim))
chessboard = board.Board()

# Next few lines of code loads in the uploading chess images and assigns it to a specific name in the images
# dictionary. This can help with naming where the specific pieces go as shown in board.py
cp_images = {"WhiteKing": p.image.load("images/WhiteKing.png"), "WhiteQueen": p.image.load("images/WhiteQueen.png"),
             "WhiteBishop": p.image.load("images/WhiteBishop.png"), "WhiteHorse": p.image.load("images/WhiteHorse.png"),
             "WhiteRook": p.image.load("images/WhiteRook.png"), "WhitePawn": p.image.load("images/WhitePawn.png"),
             "BlackKing": p.image.load("images/BlackKing.png"), "BlackQueen": p.image.load("images/BlackQueen.png"),
             "BlackBishop": p.image.load("images/BlackBishop.png"), "BlackHorse": p.image.load("images/BlackHorse.png"),
             "BlackRook": p.image.load("images/BlackRook.png"), "BlackPawn": p.image.load("images/BlackPawn.png")}


def display_Chessboard(board_display, chessboard):
    """
    The purpose of this function is to display the Chessboard
    :param board_display: This represents the generic 360 x 360 square
    :param chessboard: Variable that represents the board class
    :return:
    """
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 1:  # Algorithm that detects which squares are tan or tan4.
                p.draw.rect(board_display, p.Color("tan4"), p.Rect(col * tile_dim, row * tile_dim, tile_dim, tile_dim))
            else:
                p.draw.rect(board_display, p.Color("tan"), p.Rect(col * tile_dim, row * tile_dim, tile_dim, tile_dim))
            tile = chessboard.board[row][col]
            if tile != "empty":
                # Draws in chess png image
                board_display.blit(cp_images[tile], p.Rect(col * tile_dim, row * tile_dim, tile_dim, tile_dim))


# While loop that conducts pygame functions while the GUI is on
display_on = True
while display_on:
    for event in p.event.get():  # Gets events from the user
        if event.type == p.QUIT:  # Quits the pygame application
            display_on = False

    # Update the current chessboard to the display
    display_Chessboard(board_display, chessboard)
    p.display.flip()
