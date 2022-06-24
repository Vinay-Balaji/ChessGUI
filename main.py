import pygame as p
import chessboard
import attack
import display

# Initialize Pygame's attributes and display a 360 x 360 pixel GUI screen
p.init()
chessboard_display = p.display.set_mode((360, 360))
chessboard = chessboard.Chessboard()
dis = display.Display(chessboard_display, chessboard)

# Initialize all possible moves at the beginning of the game. This variable will later be altered
# as more moves are made and the number of possible moves are limited by checks
allowed_attacks = chessboard.get_allowed_attacks()

# Initializing a tuple which gets the user's first two clicks and represents the tile the user
# selected on the board. The list receives two tiles representing a move the user wants to make.
curr_tile = ()
tiles = []

# Instantiating variables that will keep track of whether the game is over, whether a valid move is made,
# or the number of times the user clicked on the board.
end_game = False
allowed_attack_performed = False
max_selections = 2

# Dictionary loaded in with chess piece images and assigned to a specific chess piece name.
# Helps with naming where the specific pieces go on the chessboard matrix
chess_piece_images = {"WhiteKing": p.image.load("images/WhiteKing.png"), "WhiteQueen": p.image.load("images/WhiteQueen.png"),
             "WhiteBishop": p.image.load("images/WhiteBishop.png"), "WhiteHorse": p.image.load("images/WhiteHorse.png"),
             "WhiteRook": p.image.load("images/WhiteRook.png"), "WhitePawn": p.image.load("images/WhitePawn.png"),
             "BlackKing": p.image.load("images/BlackKing.png"), "BlackQueen": p.image.load("images/BlackQueen.png"),
             "BlackBishop": p.image.load("images/BlackBishop.png"), "BlackHorse": p.image.load("images/BlackHorse.png"),
             "BlackRook": p.image.load("images/BlackRook.png"), "BlackPawn": p.image.load("images/BlackPawn.png")}


def calc_mouse_pos(x_click, y_click):
    """
    Calculates the position of a mouse click relative to the GUI display and returns the approximate
    position of a mouse click stored in a tuple. The position of the mouse click is relative to the
    top left corner of the display.
    :param x_click: x-coordinate of the click
    :param y_click: y-coordinate of the click
    :return: relative position of the mouse click on the chessboard
    """
    pos = (x_click // 45, y_click // 45)
    return pos


def clear_selection(item1, item2):
    """
    This function clears the values stored in the tuple (item1) and list (item2)
    :param item1:
    :param item2:
    :return:
    """
    item1 = ()
    item2[:] = []
    return item1, item2


# These next few lines are general pygame code to startup a GUI and get input from the user
display_on = True
while display_on:
    dis.display_Chessboard(chess_piece_images)
    for event in p.event.get():
        if event.type == p.MOUSEBUTTONDOWN:
            # Loop continues until the game is over
            if end_game == False:
                mouse_pos = p.mouse.get_pos()
                # This if statement tests if the user clicked on the same tile twice, else statement gets the row and
                # col of the tile selected and appends it to a list
                if curr_tile == (calc_mouse_pos(mouse_pos[1], mouse_pos[0])):
                    clear_selection(curr_tile, tiles)
                else:
                    curr_tile = (calc_mouse_pos(mouse_pos[1], mouse_pos[0]))
                    tiles.append(curr_tile)

                # If the user clicked twice conduct the move if the move is allowed and clear the selection.
                # Lastly update the variable that detects if an allowed move was made
                if len(tiles) == max_selections:
                    actual_move = attack.Attack(tiles[0], tiles[1], chessboard.matrix)
                    for i in range(len(allowed_attacks)):
                        if actual_move.row_tile1 == allowed_attacks[i].row_tile1 and actual_move.row_tile2 == allowed_attacks[
                            i].row_tile2 and actual_move.col_tile1 == allowed_attacks[i].col_tile1 and actual_move.col_tile2 == \
                                allowed_attacks[i].col_tile2:
                            chessboard.perform_attack(allowed_attacks[i])
                            clear_selection(curr_tile, tiles)
                            allowed_attack_performed = True
                        else:
                            tiles = [curr_tile]

        # General pygame application command which quits the application
        if event.type == p.QUIT:
            display_on = False

    # Once a move is made, get all possible moves that are allowed and reset the
    # variable which checks whether an allowed move was made
    if allowed_attack_performed:
        allowed_attacks = chessboard.get_allowed_attacks()
        allowed_attack_performed = False

    if chessboard.checkmate:
        end_game = True
        dis.drawText("Checkmate!")

    p.display.flip()