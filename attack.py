class Attack():
    """
    This class represents a chess piece attack on the board.
    It's parameters represent the tile the piece started, the
    end tile, and the chessboard itself.
    """
    def __init__(self, tile1, tile2, chessboard_matrix):
        """
        Initializes variables needed to perform an attack
        on the chessboard - gets the first tile's and second tile's
        location and pieces on those tiles.
        :param tile1: represents the first tile selected by the user
        :param tile2: represents the second tile selected by the user
        :param chessboard_matrix: matrix that holds piece locations
        """
        self.row_tile1 = tile1[0]
        self.col_tile1 = tile1[1]
        self.row_tile2 = tile2[0]
        self.col_tile2 = tile2[1]
        self.attacking_chess_piece = chessboard_matrix[self.row_tile1][self.col_tile1]
        self.attacked_chess_piece = chessboard_matrix[self.row_tile2][self.col_tile2]