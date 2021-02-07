import pygame, sys

pygame.init()
pygame.display.set_caption("Sudoku Solver")

SIZE = widht, height = 577, 664
BLACK = 0, 0, 0
WHITE = 220, 220, 220
LIGHT_BLUE = 100, 100, 255
LIGHT_RED = 255, 100, 100
LIGHT_GREEN = 100, 200, 100
YELLOW = 255, 255, 0
FONT = pygame.font.SysFont("arial", 50)
FONT_BUTTON = pygame.font.SysFont("arial", 22)

SCREEN = pygame.display.set_mode(SIZE)
SCREEN.fill(WHITE)

def game_to_real_coords_square(game_coords):
    return game_coords[0] * 64, game_coords[1] * 64, 64, 64

def game_to_pygame_Rect_coords(game_coords):
    return (game_coords[0] * 64, game_coords[1] * 64, 64, 64)

def game_to_real_coords_number(game_coords):
    return game_coords[0] * 64 + 20, game_coords[1] * 64 + 4

class Digit():
    def __init__(self, value, game_coords, cube_coords, font_colour):
        self.value = value
        self.game_coords = game_coords # 9x9 coords
        self.cube_coords = cube_coords # 3x3 coords, which smaller square they're apart of
        self.font_colour = font_colour

    def draw(self):
        pygame.draw.rect(SCREEN, BLACK, game_to_real_coords_square(self.game_coords), 1)
        text = FONT.render(self.value, True, self.font_colour, WHITE)
        SCREEN.blit(text, game_to_real_coords_number(self.game_coords))

class Button():
    def __init__ (self, state, words, coords, failed):
        self.state = state
        self.words = words
        self.coords = coords
        self.failed = failed

    def draw(self):
        if not self.failed:
            if self.state == True:
                pygame.draw.rect(SCREEN, LIGHT_GREEN, self.coords)
            else:
                pygame.draw.rect(SCREEN, LIGHT_RED, self.coords)

            text = FONT_BUTTON.render(self.words, True, BLACK, WHITE)
            SCREEN.blit(text, (self.coords[0] + 40, self.coords[1] + 2))
        else:
            pygame.draw.rect(SCREEN, YELLOW, solve_button.coords)
            text_failed = FONT_BUTTON.render("Unsolvable Sudoku (Press 'R' to restart)", True, BLACK, WHITE)
            SCREEN.blit(text_failed, (solve_button.coords[0] + 40, solve_button.coords[1] + 2))
            
        pygame.draw.rect(SCREEN, BLACK, self.coords, 2)

board_list = []
show_workings = Button(False, "See algorithm (Slower)", (8, 585, 32, 32), False)
solve_button = Button(False, "Solve sudoku (Press 'R' to restart)", (8, 624, 32, 32), False)

def find_next(board_list):
    for row in range(9):
        for col in range(9):
            if board_list[row][col].value == "0":
                return row, col

    return None, None

def check_valid(board_list, row, col, test_value):
    
    for row_check in range(9): #Check for the same column
        if board_list[row_check][col].value == test_value:
            return False

    for col_check in range(9): #Check for the same row
        if board_list[row][col_check].value == test_value:
            return False

    for col_check in range(9): #Check for the same square
        for row_check in range(9):
            if (int(row_check / 3), int(col_check / 3)) == board_list[row][col].cube_coords:
                if board_list[row_check][col_check].value == test_value:
                    return False
    
    return True

def solve(board_list):
    row, col = find_next(board_list) 

    if row == None:
        return True

    for test_value in range(1, 10):
        if check_valid(board_list, row, col, str(test_value)):
            board_list[row][col].value = str(test_value)
            board_list[row][col].font_colour = LIGHT_GREEN
            if show_workings.state:
                board_list[row][col].draw()
                pygame.display.update()
            if solve(board_list):
                return True

        board_list[row][col].value = "0"
        board_list[row][col].font_colour = BLACK
        if show_workings.state:
            board_list[row][col].draw()
            pygame.display.update()

def reset_board():
    temp_list = []
    SCREEN.fill(WHITE) # Erase the board
    for x in range(9):
        temp_list.append([])
        for y in range(9):
            temp_list[x].append(Digit("0", (x, y), (int(x/3), int(y/3)), BLACK))
        for item in temp_list[x]: # Draw the board
            item.draw()
    # Draw the dividing lines
    pygame.draw.rect(SCREEN, BLACK, (190, 0, 4, 576))
    pygame.draw.rect(SCREEN, BLACK, (382, 0, 4, 576))
    pygame.draw.rect(SCREEN, BLACK, (0, 190, 576, 4))
    pygame.draw.rect(SCREEN, BLACK, (0, 382, 576, 4))

    return temp_list

def board_draw(board_list):
    SCREEN.fill(WHITE) # Erase the board
    for row in board_list:
        for digit in row:
            digit.draw()
    # Draw the dividing lines
    pygame.draw.rect(SCREEN, BLACK, (190, 0, 4, 576))
    pygame.draw.rect(SCREEN, BLACK, (382, 0, 4, 576))
    pygame.draw.rect(SCREEN, BLACK, (0, 190, 576, 4))
    pygame.draw.rect(SCREEN, BLACK, (0, 382, 576, 4))

def edit_digit(digit):
    print("Clicked on: " + str (digit.game_coords) + ". What do you want its new value to be? (Current value is " + str(digit.value) + ") ")
    gathering = True
    while gathering:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key in range(48, 58): #Check for numbers near F1 - F12 keys
                    digit.value = str(event.key - 48)
                    if str(event.key - 48) != 0:
                        digit.poss_values = list(str(event.key - 48)) #Make it so the list of possible values is the input itself
                    gathering = False #Stop the while loop

                elif event.key in range(1073741913, 1073741923): #Check for numbers in numbpad
                    if event.key in range(1073741913, 1073741922):
                        digit.value = str(event.key - 1073741912)
                        digit.poss_values = list(str(event.key - 1073741912)) #Make it so the list of possible values is the input itself
                        gathering = False #Stop the while loop
                    else:
                        digit.value = "0"
                        gathering = False #Stop the while loop

                else:
                    print("Invalid input, it must be a number.")
    if digit.value == "0":
        digit.font_colour = BLACK
    else:
        digit.font_colour = LIGHT_RED
    digit.draw()

board_list = reset_board()

while True:
    show_workings.draw()
    solve_button.draw()
    pygame.display.update()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #Assign a value
                for row in board_list: #Check if its pressing a digit
                    for digit in row:
                        if pygame.Rect(game_to_pygame_Rect_coords(digit.game_coords)).collidepoint(event.pos):
                            digit.font_colour = LIGHT_BLUE
                            digit.draw()
                            pygame.display.update()
                            edit_digit(digit)
                
                if pygame.Rect(show_workings.coords).collidepoint(event.pos): #Interacting with see algorithm button
                    if show_workings.state:
                        show_workings.state = False
                    else:
                        show_workings.state = True
                
                if pygame.Rect(solve_button.coords).collidepoint(event.pos): #Interacting with solve sudoku button
                    solve_button.state = True
                    solve(board_list)

                    for row in range(9):#Check that if it failed
                        for col in range(9):
                            if board_list[row][col].value == "0":
                                solve_button.failed = True
                                break
                    board_draw(board_list)
                    pygame.display.update()

        if event.type == pygame.KEYDOWN:

            if event.key == 114:
                board_list = reset_board() #Pressing "R" resets the board
                solve_button.state = False
                solve_button.failed = False

            else:
                print(event.key) #Testing purposes

        if event.type == pygame.QUIT: sys.exit() #Exit the programm
