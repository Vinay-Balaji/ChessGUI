import attack


class Chessboard:
    def __init__(self):
        """
        Initializes player turns, possible attacks, and piece
        a matrix that holds the locations of pieces on the chessboard.
        """
        self.player1_turn = True
        self.player2_turn = False
        self.all_attacks = []
        self.checkmate = False
        self.king_paths = [(1, 1), (0, 1), (1, 0), (0, -1), (-1, 1), (-1, 0), (1, -1), (-1, -1)]
        self.bishop_paths = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.rook_paths = [(1, 0), (0, 1), (0, -1), (-1, 0)]
        self.knight_paths = [(2, 1), (1, 2), (1, -2), (-2, 1), (-1, 2), (2, -1), (-2, -1), (-1, -2)]
        self.matrix = [
            ["BlackRook", "BlackHorse", "BlackBishop", "BlackQueen", "BlackKing", "BlackBishop", "BlackHorse",
             "BlackRook"],
            ["BlackPawn", "BlackPawn", "BlackPawn", "BlackPawn", "BlackPawn", "BlackPawn", "BlackPawn", "BlackPawn"],
            ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
            ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
            ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
            ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
            ["WhitePawn", "WhitePawn", "WhitePawn", "WhitePawn", "WhitePawn", "WhitePawn", "WhitePawn", "WhitePawn"],
            ["WhiteRook", "WhiteHorse", "WhiteBishop", "WhiteQueen", "WhiteKing", "WhiteBishop", "WhiteHorse",
             "WhiteRook"]
        ]

    def swap_turns(self):
        """
        Swaps player 1 and player 2 turns
        :return: None
        """
        self.player1_turn = self.player2_turn
        self.player2_turn = not self.player2_turn

    def get_piece_pos(self, piece_name):
        """
        Gets the position of a chess piece on the
        chessboard matrix
        :param piece_name: string of chess piece name
        :return: list of row and column
        """
        # Iterate through matrix and check if chess piece name
        # matches the value on the current tile
        for row in range(0, 8):
            for col in range(0, 8):
                if self.matrix[row][col] == piece_name:
                    pos = [row, col]
                    return pos

    def perform_attack(self, attack):
        """
        Perform a chess piece attack and update the chessboard matrix
        :param attack: attack object
        :return: None
        """
        # Empty first tile selected by user and move selected chess piece
        # to second tile
        self.matrix[attack.row_tile1][attack.col_tile1] = "empty"
        self.matrix[attack.row_tile2][attack.col_tile2] = attack.attacking_chess_piece
        self.all_attacks.append(attack)

        # Check if piece attacking is a pawn and if it is at the end of the chessboard.
        # If it is, promote the pawn to a Queen
        if (attack.attacking_chess_piece == 'WhitePawn' and attack.row_tile2 == 0) or (
                attack.attacking_chess_piece == 'BlackPawn' and attack.row_tile2 == 7):
            self.matrix[attack.row_tile2][attack.col_tile2] = attack.attacking_chess_piece[:5] + "Queen"
        self.swap_turns()

    def last_attack(self):
        """
        Helper function for checking checkmate - gets the last attack made on the chessboard
        :return: None
        """
        # Gets the most recent attack, deletes it, and brings back the chess piece and attacked
        # chess piece
        last_attack = self.all_attacks[-1]
        del self.all_attacks[-1]
        self.matrix[last_attack.row_tile1][last_attack.col_tile1] = last_attack.attacking_chess_piece
        self.matrix[last_attack.row_tile2][last_attack.col_tile2] = last_attack.attacked_chess_piece

    def check(self):
        """
        Checks if there is a white king or black king check on the chessboard
        :return: True if there is a check, False otherwise
        """
        # Get positions of each king in terms of row and column on the
        # chessboard matrix
        white_king_pos = self.get_piece_pos("WhiteKing")
        black_king_pos = self.get_piece_pos("BlackKing")

        # To check for white check, switch to player 2 turn to get their
        # attacks. For each of their attacks determine if any of their moves result in
        # them possibly attacking the king
        if self.player1_turn:
            self.swap_turns()
            player2_attack = self.get_attacks()
            self.swap_turns()
            for i in player2_attack:
                if i.row_tile2 == white_king_pos[0] and i.col_tile2 == white_king_pos[1]:
                    return True
            return False

        # Do the same as above for player 1 attacks to determine if black king is in check
        if self.player2_turn:
            self.swap_turns()
            player1_attack = self.get_attacks()
            self.swap_turns()
            for i in player1_attack:
                if i.row_tile2 == black_king_pos[0] and i.col_tile2 == black_king_pos[1]:
                    return True
            return False

    def get_allowed_attacks(self):
        """
        Get a player's list of allowed attacks that would not result in
        them leaving their own king exposed for an opponent attack
        :return: a list of allowed attacks, or if there are no allowed
        attacks return True if in checkmate, False if not
        """
        # Get all the potential moves that the current player can make
        attacks = self.get_attacks()

        # For every attack in the list, swap the player turns and determine if the
        # initial player's king is in check. If it is, remove that attack from
        # the list of potential moves and go back to the last attack made on the chessboard
        for i in range(len(attacks) - 1, -1, -1):
            self.perform_attack(attacks[i])
            self.swap_turns()
            if self.check():
                attacks.remove(attacks[i])
            self.last_attack()

        # If there are no attacks left, check if the king is in check. If so,
        # it is checkmate and the game is over. If not, there isn't a
        # checkmate and the game continues
        if len(attacks) == 0:
            if self.check():
                self.checkmate = True
        else:
            self.checkmate = False
        return attacks

    def get_attacks(self):
        """
        Gets all the attacks for all of a player's pieces regardless if they
        result in check or not for their own king.
        :return: a list of attacks
        """
        # Initialize a list of attacks and for each position on the chessboard
        # matrix, get all the current player's pieces' attacks.
        attacks = []
        for row in range(8):
            for col in range(8):
                if (self.matrix[row][col][:5] == 'White' and self.player1_turn) or (
                        self.matrix[row][col][:5] == 'Black' and self.player2_turn):
                    if self.matrix[row][col][5] == 'P':
                        self.pawn_attacks(row, col, attacks)
                    elif self.matrix[row][col][5] == 'R':
                        self.rook_attacks(row, col, attacks)
                    elif self.matrix[row][col][5] == 'H':
                        self.knight_attacks(row, col, attacks)
                    elif self.matrix[row][col][5] == 'B':
                        self.bishop_attacks(row, col, attacks)
                    elif self.matrix[row][col][5] == 'Q':
                        self.queen_attacks(row, col, attacks)
                    elif self.matrix[row][col][5] == 'K':
                        self.king_attacks(row, col, attacks)
        return attacks

    def pawn_attacks(self, row, col, attacks):
        """
        Gets all the pawn attacks
        :param row: current row of pawn piece
        :param col: current column of pawn piece
        :param attacks: list of potential attacks
        :return: None
        """
        # Need to split the logic in terms of white and black pawns for row
        # manipulation and attacking white or black pieces
        if self.player1_turn:
            # Check if the tile one tile to the left and one tile ahead is a
            # black piece and the column value is not less than 0. If so append the attack
            if col - 1 >= 0 and self.matrix[row - 1][col - 1][:5] == 'Black':
                attacks.append(attack.Attack((row, col), (row - 1, col - 1), self.matrix))
            # Check if the tile one tile to the right and one tile ahead is a
            # black piece and the column value is not greater than 7. If so append the attack
            if col + 1 <= 7 and self.matrix[row - 1][col + 1][:5] == 'Black':
                attacks.append(attack.Attack((row, col), (row - 1, col + 1), self.matrix))
            # Check if the tile one tile to ahead is empty. If so append the attack
            if self.matrix[row - 1][col][:] == "empty":
                attacks.append(attack.Attack((row, col), (row - 1, col), self.matrix))
                # Check if the tile two tiles ahead is empty. If so append the attack
                if row == 6 and self.matrix[row - 2][col] == "empty":
                    attacks.append(attack.Attack((row, col), (row - 2, col), self.matrix))
            # Do not need to check for row values since if they get to the end of the chessboard
            # the pawn should be promoted through pawn promotion
        # Similar logic as white pawns but different row manipulation
        if self.player2_turn:
            if col - 1 >= 0 and self.matrix[row + 1][col - 1][:5] == "White":
                attacks.append(attack.Attack((row, col), (row + 1, col - 1), self.matrix))
            if col + 1 <= 7 and self.matrix[row + 1][col + 1][:5] == "White":
                attacks.append(attack.Attack((row, col), (row + 1, col + 1), self.matrix))
            if self.matrix[row + 1][col][:] == "empty":
                attacks.append(attack.Attack((row, col), (row + 1, col), self.matrix))
                if row == 1 and self.matrix[row + 2][col] == "empty":
                    attacks.append(attack.Attack((row, col), (row + 2, col), self.matrix))

    def rook_attacks(self, row, col, attacks):
        """
        Gets all the rook attacks
        :param row: current row of rook piece
        :param col: current column of rook piece
        :param attacks: list of potential attacks
        :return: None
        """
        # Iterates through each rook path defined in the init method and multiplies
        # the respective row or column value in the rook path list with a value
        # from 1 to 8
        for path in self.rook_paths:
            for i in range(1, 8):
                possible_col = (i * path[1]) + col
                possible_row = (i * path[0]) + row
                # If the row and column values are within the chessboard continue
                if 0 <= possible_row < 8:
                    if 0 <= possible_col < 8:
                        # Checks if the rook is attacking the appropriate team, and if so append attack
                        if ("White" == self.matrix[possible_row][possible_col][:5] and self.player2_turn) or (
                                "Black" == self.matrix[possible_row][possible_col][:5] and self.player1_turn):
                            attacks.append(attack.Attack((row, col), (possible_row, possible_col), self.matrix))
                            break
                        # Checks if the rook is attacking an empty tile, and if so append attack
                        elif self.matrix[possible_row][possible_col] == "empty":
                            attacks.append(attack.Attack((row, col), (possible_row, possible_col), self.matrix))
                        # Need to break so that function can continue to next iteration
                        else:
                            break
                    else:
                        break
                else:
                    break

    def knight_attacks(self, row, col, attacks):
        """
        Gets all the knight attacks
        :param row: current row of knight piece
        :param col: current column of knight piece
        :param attacks: list of potential attacks
        :return: None
        """
        # Iterates through each knight path defined in the init method and adds
        # the respective row or column value in the knight path list to the current row
        # and column
        for path in self.knight_paths:
            possible_row = path[0] + row
            possible_col = path[1] + col
            # If the row and column values are within the chessboard continue
            if 0 <= possible_row < 8:
                if 0 <= possible_col < 8:
                    # Checks if the knight is attacking the appropriate team, and if so append attack
                    if (self.matrix[possible_row][possible_col][:5] != "White" and self.player1_turn) or (
                            self.matrix[possible_row][possible_col][:5] != "Black" and self.player2_turn):
                        attacks.append(attack.Attack((row, col), (possible_row, possible_col), self.matrix))
                    # Do not need to check if the tile is empty since the knight can jump other pieces

    def bishop_attacks(self, row, col, attacks):
        """
        Gets all the bishop attacks
        :param row: current row of bishop piece
        :param col: current column of bishop piece
        :param attacks: list of potential attacks
        :return: None
        """
        # Iterates through each bishop path defined in the init method and multiplies
        # the respective row or column value in the bishop path list with a value
        # from 1 to 8
        for paths in self.bishop_paths:
            for i in range(1, 8):
                possible_row = (i * paths[0]) + row
                possible_col = (i * paths[1]) + col
                # If the row and column values are within the chessboard continue
                if 0 <= possible_row < 8:
                    if 0 <= possible_col < 8:
                        # Checks if the bishop is attacking an empty tile, and if so append attack
                        if self.matrix[possible_row][possible_col][:] == "empty":
                            attacks.append(attack.Attack((row, col), (possible_row, possible_col), self.matrix))
                        # Checks if the bishop is attacking the appropriate team, and if so append attack
                        elif (self.matrix[possible_row][possible_col][:5] == "Black" and self.player1_turn) or (
                                self.matrix[possible_row][possible_col][:5] == "White" and self.player2_turn):
                            attacks.append(attack.Attack((row, col), (possible_row, possible_col), self.matrix))
                            break
                        # Need to break so that function can continue to next iteration
                        else:
                            break
                    else:
                        break
                else:
                    break

    def queen_attacks(self, row, col, attacks):
        """
        Gets all the queen attacks
        :param row: current row of queen piece
        :param col: current column of queen piece
        :param attacks: list of potential attacks
        :return: None
        """
        # Since the queen moves are the bishop and rook moves combined,
        # calls those functions to get attacks
        self.bishop_attacks(row, col, attacks)
        self.rook_attacks(row, col, attacks)

    def king_attacks(self, row, col, attacks):
        """
        Gets all the king attacks
        :param row: current row of king piece
        :param col: current column of king piece
        :param attacks: list of potential attacks
        :return: None
        """
        # Iterates through each king path defined in the init method and adds
        # the respective row or column value in the king path list to the current row
        # and column
        for path in self.king_paths:
            possible_row = path[0] + row
            possible_col = path[1] + col
            # If the row and column values are within the chessboard continue
            if 0 <= possible_row < 8:
                if 0 <= possible_col < 8:
                    # Checks if the king is attacking the appropriate team, and if so append attack
                    if (self.matrix[possible_row][possible_col][:5] != "White" and self.player1_turn) or (
                            self.matrix[possible_row][possible_col][:5] != "Black" and self.player2_turn):
                        attacks.append(attack.Attack((row, col), (possible_row, possible_col), self.matrix))
                    # Do not need to check if the tiles are empty since the king can only
                    # move one tile at a time