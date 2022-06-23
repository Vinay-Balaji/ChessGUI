import pygame as p


class Display():
    """
    This class represents all the display functionalities
    of the chess GUI using pygame
    """

    def __init__(self, chessboard_display, chessboard):
        """
        Initializes pygame modules, chessboard display, and the chessboard itself
        :param chessboard_display: display of chessboard using pygame
        :param chessboard: chessboard object
        """
        p.init()
        self.chessboard_display = chessboard_display
        self.chessboard = chessboard

    def display_Chessboard(self, images_dictionary):
        """
        The purpose of this function is to display the Chessboard
        :param images_dictionary: Represents the dictionary of images assigned to
        each chess piece
        :return: displays the chessboard
        """
        tile_count = 1
        for row in range(8):
            tile_count += 1
            for col in range(8):
                # Algorithm that detects which squares should be tan or tan4 to create
                # checkerboard pattern.
                if tile_count % 2 == 1:
                    p.draw.rect(self.chessboard_display, p.Color("tan4"), p.Rect(col * 45, row * 45, 45, 45))
                else:
                    p.draw.rect(self.chessboard_display, p.Color("tan"), p.Rect(col * 45, row * 45, 45, 45))
                if self.chessboard.matrix[row][col] != "empty":
                    # Draws in chess png image for each tile according to board
                    # display matrix values.
                    self.chessboard_display.blit(images_dictionary[self.chessboard.matrix[row][col]],
                                                 p.Rect(col * 45, row * 45, 45, 45))
                tile_count += 1