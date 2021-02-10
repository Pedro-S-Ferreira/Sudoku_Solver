import pygame, sys

pygame.init()
pygame.display.set_caption("Checkers")

SIZE = width, height = 512, 600
BLACK = 0, 0, 0
LIGHT_GREEN = 128, 200, 128
GREEN = 0, 255, 0
RED = 255, 0, 0
DARK_RED = 150, 0, 0
WHITE = 255, 255, 255
DARK_WHITE = 150, 150, 150
BROWN = 255, 255, 100
FONT_BUTTON = pygame.font.SysFont("arial", 22)

SCREEN = pygame.display.set_mode(SIZE)

def coords_to_circle(x, y):
    return [x * 64 + 32, y * 64 + 32]

def coords_to_square(x, y):
    return [x * 64, y * 64]

class Square:
    def __init__(self, colour, draw_coords, real_coords, piece):
        self.colour = colour
        self.draw_coords = draw_coords
        self.real_coords = real_coords
        self.piece = piece #0 means no piece, #WHITE means a white piece is there, #RED means a red piece is there      
    
    def draw(self):
        pygame.draw.rect(SCREEN, self.colour, self.draw_coords)

class Piece:
    def __init__(self, colour, draw_centre, coords, king):
        self.colour = colour
        self.draw_centre = draw_centre
        self.coords = coords
        self.king = king
    
    def update_draw_centre(self):
        self.draw_centre = coords_to_circle(self.coords)
    
    def draw(self):
            pygame.draw.circle(SCREEN, self.colour, self.draw_centre, 24)

    def available_moves(self):
        moves = []
        remove = []

        if self.colour in (RED, DARK_RED, DARK_WHITE):
            if self.coords[0] > 0:
                moves.append([self, self.coords[0] - 1, self.coords[1] + 1])
            if self.coords[0] < 7:
                moves.append([self, self.coords[0] + 1, self.coords[1] + 1])
        
        if self.colour in (WHITE, DARK_RED, DARK_WHITE):
            if self.coords[0] > 0:
                moves.append([self, self.coords[0] - 1, self.coords[1] - 1])
            if self.coords[0] < 7:
                moves.append([self, self.coords[0] + 1, self.coords[1] - 1])

        for move in moves: #To verify all moves are valid
            for square in dark_squares:
                if [move[1], move[2]] == square.real_coords and square.piece in (RED, WHITE): #Piece being moved is white
                    remove.append(move)
        for move in remove: #The remove list is needed as we can't remove items from a list as we're iterating it.
            moves.remove(move)
        for move in moves:
            pygame.draw.circle(SCREEN, BROWN, (move[1] * 64 + 32, move[2] * 64 + 32), 12)
        return moves

    def available_captures(self):
        moves = []
        remove = []

        if self.colour in (RED, DARK_RED):
            if self.coords[0] > 0:
                for square in dark_squares:
                    if square.real_coords == [self.coords[0] - 1, self.coords[1] + 1] and square.piece == WHITE:
                        moves.append([self, self.coords[0] - 2, self.coords[1] + 2, square])
            if self.coords[0] < 7:
                for square in dark_squares:
                    if square.real_coords == [self.coords[0] + 1, self.coords[1] + 1] and square.piece == WHITE:
                        moves.append([self, self.coords[0] + 2, self.coords[1] + 2, square])

        if self.colour == DARK_WHITE:
            if self.coords[0] > 0:
                for square in dark_squares:
                    if square.real_coords == [self.coords[0] - 1, self.coords[1] + 1] and square.piece == RED:
                        moves.append([self, self.coords[0] - 2, self.coords[1] + 2, square])
            if self.coords[0] < 7:
                for square in dark_squares:
                    if square.real_coords == [self.coords[0] + 1, self.coords[1] + 1] and square.piece == RED:
                        moves.append([self, self.coords[0] + 2, self.coords[1] + 2, square])

        if self.colour in (WHITE, DARK_WHITE):
            if self.coords[0] > 0:
                for square in dark_squares:
                    if square.real_coords == [self.coords[0] - 1, self.coords[1] - 1] and square.piece == RED:
                        moves.append([self, self.coords[0] - 2, self.coords[1] - 2, square])
            if self.coords[0] < 7:
                for square in dark_squares:
                    if square.real_coords == [self.coords[0] + 1, self.coords[1] - 1] and square.piece == RED:
                        moves.append([self, self.coords[0] + 2, self.coords[1] - 2, square])

        if self.colour == DARK_RED:
            if self.coords[0] > 0:
                for square in dark_squares:
                    if square.real_coords == [self.coords[0] - 1, self.coords[1] - 1] and square.piece == WHITE:
                        moves.append([self, self.coords[0] - 2, self.coords[1] - 2, square])
            if self.coords[0] < 7:
                for square in dark_squares:
                    if square.real_coords == [self.coords[0] + 1, self.coords[1] - 1] and square.piece == WHITE:
                        moves.append([self, self.coords[0] + 2, self.coords[1] - 2, square])

        for move in moves: #To verify all moves are valid
            for square in dark_squares:
                if [move[1], move[2]] == square.real_coords and square.piece in (RED, WHITE): #Piece being moved is white
                    remove.append(move)
        for move in remove: #The remove list is needed as we can't remove items from a list as we're iterating it.
            moves.remove(move)
        for move in moves:
            pygame.draw.circle(SCREEN, BROWN, (move[1] * 64 + 32, move[2] * 64 + 32), 16)
        return moves

class Button():
    def __init__ (self, state, words, coords, failed):
        self.state = state
        self.words = words
        self.coords = coords
        self.failed = failed
    
    def draw(self):
        pygame.draw.rect(SCREEN, LIGHT_GREEN, (self.coords[0], self.coords[1], 250, 36))# Since the text is AA, pressing the button multiple times would have a strange effect, hence the need to erase it before drawing it again.
        if not self.failed:
            if self.state:
                pygame.draw.rect(SCREEN, GREEN, self.coords)
            else:
                pygame.draw.rect(SCREEN, RED, self.coords)

            text = FONT_BUTTON.render(self.words, True, BLACK)
            SCREEN.blit(text, (self.coords[0] + 40, self.coords[1] + 6))
        else:
            pygame.draw.rect(SCREEN, YELLOW, solve_button.coords)
            
        pygame.draw.rect(SCREEN, BLACK, self.coords, 2)

class Indicator():
    def __init__(self, piece_colour, centre_coords, remaining):
        self.piece_colour = piece_colour
        self.centre_coords = centre_coords
        self.remaining = remaining
    
    def draw(self):
        remaining = "x" + str(self.remaining)
        pygame.draw.circle(SCREEN, self.piece_colour, self.centre_coords)

dark_squares = []# The only squares drawn were black ones as they're the only playable ones anyway. 
                #The background is white. The squares are found in a list, in order, from top to bottom, left to right

restart_button = Button(True, "Press to restart.", (10, 522, 32, 32), False)

for collumn in range(0, 4):
    for row in range(1, 9, 2):
        dark_squares.append(Square(BLACK, (collumn * 128, row * 64, 64, 64), [2 * collumn, row], False))
    for row in range(0, 8, 2):
        dark_squares.append(Square(BLACK, (collumn * 128 + 64, row * 64, 64, 64), [2 * collumn + 1, row], False))

def board_draw():
    for item in dark_squares:
        item.draw()
    #Draw borders
    pygame.draw.rect(SCREEN, BLACK, (0, 0, 512, 1))
    pygame.draw.rect(SCREEN, BLACK, (0, 512, 512, 1))
    pygame.draw.rect(SCREEN, BLACK, (0, 0, 1, 512))
    pygame.draw.rect(SCREEN, BLACK, (511, 0, 1, 512))
    #Draw bits below
    restart_button.draw()

def board_reset():
    pieces = []

    for square in dark_squares:
        if square.real_coords[1] <= 2:
            pieces.append(Piece(RED, [square.real_coords[0] * 64 + 32, square.real_coords[1] * 64 + 32], square.real_coords, 0))
            square.piece = RED
        elif square.real_coords[1] >= 5:
            pieces.append(Piece(WHITE, [square.real_coords[0] * 64 + 32, square.real_coords[1] * 64 + 32], square.real_coords, 0))
            square.piece = WHITE
        else:
            square.piece = 0
    
    for piece in pieces:
        piece.draw()

    return pieces, (WHITE, DARK_WHITE)

def pieces_draw(pieces):#This function draws the pieces, checks and makes them kings and checks to see if the game is over yet
    red = []
    white = []
    for piece in pieces:
        if piece.coords[1] == 7 and piece.colour == RED:
            piece.king = True
            piece.colour = DARK_RED
        elif piece.coords[1] == 0 and piece.colour == WHITE:
            piece.king = True
            piece.colour = DARK_WHITE
        if piece.colour in (RED, DARK_RED):
            red.append(piece)
        if piece.colour in (WHITE, DARK_WHITE):
            white.append(piece)
        piece.draw()
    if len(red) == 0:
        print("Game Over. White wins! Press \"R\" to play again.")
        return 1
    elif len(white) == 0:
        print("Game Over. Red wins! Press \"R\" to play again.")
        return 2

SCREEN.fill(LIGHT_GREEN)
board_draw()
pieces, play = board_reset()
print("White to play.")

while True:
    pygame.display.update()

    cursor_coords = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    for event in pygame.event.get():                
        if event.type == pygame.MOUSEBUTTONDOWN:
            for piece in pieces: #Check if the cursor is hovering over a piece
                if cursor_coords[0] >= piece.draw_centre[0] - 32 and cursor_coords[0] <= piece.draw_centre[0] + 32 and cursor_coords[1] >= piece.draw_centre[1] - 32 and cursor_coords[1] <= piece.draw_centre[1] + 32 and piece.colour in play:
                    board_draw()
                    pieces_draw(pieces)
                    moves = piece.available_moves() + piece.available_captures()
                    #restart_button.state = False
                    #restart_button.draw()
            try:
                for move in moves:
                    if cursor_coords[0] > coords_to_square(move[1], move[2])[0] and cursor_coords[1] > coords_to_square(move[1], move[2])[1] and cursor_coords[0] < coords_to_square(move[1], move[2])[0] + 64 and cursor_coords[1] < coords_to_square(move[1], move[2])[1] + 64:
                        for square in dark_squares: #Make it so the square the piece is about to leave knows it no longuer has a piece
                            if square.real_coords == move[0].coords:
                                square.piece = 0
                                board_draw()#board_draw() is needed instead of simply square_draw() as the other indication of possible movement (small purple circle), if present, also needs to be erased
                                restart_button.state = False
                                restart_button.draw()
                        
                        move[0].coords = [move[1], move[2]] #Give the piece new coordinates and draw it in its new place
                        move[0].draw_centre = coords_to_circle(move[1], move[2])
                        try:
                            for piece in pieces:
                                if piece.coords == move[3].real_coords:
                                    pieces.remove(piece)
                                    move[3].piece = 0
                        except:
                            pass
                        pieces_draw(pieces)
                        moves = []
                        if not pieces_draw(pieces):
                            if play == (WHITE, DARK_WHITE):
                                play = (RED, DARK_RED)
                                print("Red to play.")
                            elif play == (RED, DARK_RED):
                                play = (WHITE, DARK_WHITE)
                                print("White to play.")
                        else:
                            play = (0, 0)# It has to be a list and not just False so line 198 doesn't return an error.

                        for square in dark_squares: #Make it so the square the piece is now on knows it has a piece
                            if square.real_coords == move[0].coords:
                                if move[0].colour in (RED, DARK_RED):
                                    square.piece = RED
                                elif move[0].colour in (WHITE, DARK_WHITE):
                                    square.piece = WHITE

            except:
                pass

            if pygame.Rect(restart_button.coords).collidepoint(event.pos):
                board_draw()
                pieces, play = board_reset()
                restart_button.state = True
                restart_button.draw()
        
        if event.type == pygame.KEYDOWN: #By pressing R, we can restart the game
            if event.key == pygame.K_r:
                board_draw()
                pieces = board_reset()

        if event.type == pygame.QUIT: sys.exit()
