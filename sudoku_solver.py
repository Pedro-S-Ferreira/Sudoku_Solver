import pygame, sys

pygame.init()
pygame.display.set_caption("Sudoku Solver")

SIZE = widht, height = 577, 577
BLACK = 0, 0, 0
WHITE = 220, 220, 220
LIGHT_BLUE = 100, 100, 255
LIGHT_RED = 255, 100, 100
LIGHT_GREEN = 100, 200, 100
FONT = pygame.font.SysFont('arial', 50)

SCREEN = pygame.display.set_mode(SIZE)
SCREEN.fill(WHITE)

def game_to_real_coords_square(game_coords):
    return game_coords[0] * 64, game_coords[1] * 64, 64, 64

def game_to_pygame_Rect_coords(game_coords):
    return (game_coords[0] * 64, game_coords[1] * 64, 64, 64)

def game_to_real_coords_number(game_coords):
    return game_coords[0] * 64 + 20, game_coords[1] * 64 + 4

class Digit():
    def __init__(self, value, game_coords, cube_coords, original, solved, font_colour, poss_values):
        self.value = value
        self.game_coords = game_coords # 9x9 coords
        self.cube_coords = cube_coords # 3x3 coords, which smaller cube they're apart of
        self.original = original #If True, it wasn't guessed
        self.solved = solved # 0 if not, 1 if yes
        self.font_colour = font_colour
        self.poss_values = poss_values

    def draw(self):
        pygame.draw.rect(SCREEN, BLACK, game_to_real_coords_square(self.game_coords), 1)
        text = FONT.render(self.value, False, self.font_colour, WHITE)
        SCREEN.blit(text, game_to_real_coords_number(self.game_coords))

board_list = []

def reset_board():
    temp_list = []
    SCREEN.fill(WHITE) # Erase the board
    for x in range(9):
        temp_list.append([])
        for y in range(9):
            temp_list[x].append(Digit("0", (x, y), (int(x/3), int(y/3)),False, 0, BLACK, [str(x) for x in range(1, 10)]))
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

def digit_solver(digit):
    position = digit.game_coords
    if not board_list[position[0]][position[1]].value == "0": #Check that this square hasn't been solved.
        return board_list[position[0]][position[1]].value

    for y in range(9): #Check numbers in rows
        if board_list[position[0]][y].value in digit.poss_values:
            try:
                digit.poss_values.remove(board_list[position[0]][y].value)
            except:
                continue

    for x in range(9): #Check numbers in collumns
        if board_list[x][position[1]].value in digit.poss_values:
            try:
                digit.poss_values.remove(board_list[x][position[1]].value)
            except:
                continue

    for x in range(9): #Check numbers in correspondant cube
        for y in range(9):
            if (int(board_list[x][y].game_coords[0] / 3), int(board_list[x][y].game_coords[1] / 3)) == (digit.cube_coords[0], digit.cube_coords[1]):
                if board_list[x][y].value in digit.poss_values:
                    try:
                        digit.poss_values.remove(board_list[x][y].value)
                    except:
                        continue
 
    if len(digit.poss_values) == 1:
        digit.font_colour = LIGHT_GREEN
        digit.solved = 1
        return digit.poss_values[0]
    
    
    test_poss_values = list(digit.poss_values)

    for x in range(9): #Check numbers in correspondant cube
        for y in range(9):
            if (int(board_list[x][y].game_coords[0] / 3), int(board_list[x][y].game_coords[1] / 3)) == (digit.cube_coords[0], digit.cube_coords[1]):
                if (board_list[x][y].game_coords[0], board_list[x][y].game_coords[1]) != (digit.game_coords[0], digit.game_coords[1]):
                    for value in board_list[x][y].poss_values:
                        try:
                            test_poss_values.remove(value)
                        except:
                            continue

    
    if len(test_poss_values) == 1:
        digit.poss_values = test_poss_values    

    if len(digit.poss_values) == 1:
        digit.font_colour = LIGHT_GREEN
        digit.solved = 1
        return digit.poss_values[0]

    #If, in any given smaller cube, one possible value is found on ONLY the lists of 3 adjecent digits (vertical or horizontal) we can be certain
    #that value will be in that collumn/row, meaning we can remove said value from the possible lists of all others digits in the same row/collumn
    #in the entire board
    for x in range(0, 7, 3): # As mini cubes are in a 3x3 arrangement
        for y in range(0, 7, 3):

            for value in board_list[x][y].poss_values:
                if value in (board_list[x + 1][y].poss_values + board_list[x + 2][y].poss_values): #Check matching value
                    if value not in (board_list[x][y + 1].poss_values + board_list[x + 1][y + 1].poss_values + board_list[x + 2][y + 1].poss_values + board_list[x][y + 2].poss_values + board_list[x + 1][y + 2].poss_values + board_list[x + 2][y + 2].poss_values): # Check that it isn't on any other to make this solution true
                        for z in range(9):
                            if z not in (x, x+1, x+2): #Doesn't remove the possible value from the place were certain it might be
                                try:
                                    board_list[z][y].poss_values.remove(value)
                                except:
                                    continue

            for value in board_list[x][y + 1].poss_values:                            
                if value in (board_list[x + 1][y + 1].poss_values + board_list[x + 2][y + 1].poss_values): #Check matching value
                    if value not in (board_list[x][y].poss_values + board_list[x + 1][y].poss_values + board_list[x + 2][y].poss_values + board_list[x][y + 2].poss_values + board_list[x + 1][y + 2].poss_values + board_list[x + 2][y + 2].poss_values): # Check that it isn't on any other to make this solution true
                        for z in range(9):
                            if z not in (x, x+1, x+2): #Doesn't remove the possible value from the place were certain it might be
                                try:
                                    board_list[z][y + 1].poss_values.remove(value)
                                except:
                                    continue

            for value in board_list[x][y + 2].poss_values:                        
                if value in (board_list[x + 1][y + 2].poss_values + board_list[x + 2][y + 2].poss_values): #Check matching value
                    if value not in (board_list[x][y + 1].poss_values + board_list[x + 1][y + 1].poss_values + board_list[x + 2][y + 1].poss_values + board_list[x][y].poss_values + board_list[x + 1][y].poss_values + board_list[x + 2][y].poss_values): # Check that it isn't on any other to make this solution true
                        for z in range(9):
                            if z not in (x, x+1, x+2): #Doesn't remove the possible value from the place were certain it might be
                                try:
                                    board_list[z][y + 2].poss_values.remove(value)
                                except:
                                    continue
                
            for value in board_list[x][y].poss_values: # This one could be mixed with the first square as they both use the same starting point
                if value in (board_list[x][y + 1].poss_values + board_list[x][y + 2].poss_values): #Check matching value
                    if value not in (board_list[x + 1][y].poss_values + board_list[x + 1][y + 1].poss_values + board_list[x + 1][y + 2].poss_values + board_list[x + 2][y].poss_values + board_list[x + 2][y + 1].poss_values + board_list[x + 2][y + 2].poss_values): # Check that it isn't on any other to make this solution true
                        for z in range(9):
                            if z not in (y, y+1, y+2): #Doesn't remove the possible value from the place were certain it might be
                                try:
                                    board_list[x][z].poss_values.remove(value)
                                except:
                                    continue

            for value in board_list[x + 1][y].poss_values:
                if value in (board_list[x + 1][y + 1].poss_values + board_list[x + 1][y + 2].poss_values): #Check matching value
                    if value not in (board_list[x][y].poss_values + board_list[x][y + 1].poss_values + board_list[x][y + 2].poss_values + board_list[x + 2][y].poss_values + board_list[x + 2][y + 1].poss_values + board_list[x + 2][y + 2].poss_values): # Check that it isn't on any other to make this solution true
                        for z in range(9):
                            if z not in (y, y+1, y+2): #Doesn't remove the possible value from the place were certain it might be
                                try:
                                    board_list[x + 1][z].poss_values.remove(value)
                                except:
                                    continue

            for value in board_list[x + 2][y].poss_values:
                if value in (board_list[x + 2][y + 1].poss_values + board_list[x + 2][y + 2].poss_values): #Check matching value
                    if value not in (board_list[x + 1][y].poss_values + board_list[x + 1][y + 1].poss_values + board_list[x + 1][y + 2].poss_values + board_list[x][y].poss_values + board_list[x][y + 1].poss_values + board_list[x][y + 2].poss_values): # Check that it isn't on any other to make this solution true
                        for z in range(9):
                            if z not in (y, y+1, y+2): #Doesn't remove the possible value from the place were certain it might be
                                try:
                                    board_list[x + 2][z].poss_values.remove(value)
                                except:
                                    continue

    if len(digit.poss_values) == 1:
        digit.font_colour = LIGHT_GREEN
        digit.solved = 1
        return digit.poss_values[0]
    else:
        print("It appears I can't solve this square yet, or that there are multiple solutions.")
        print("Here's a list of the possible values:", digit.poss_values)
        return "0"


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
        digit.poss_values = [str(x) for x in range(1, 10)]
    else:
        digit.font_colour = LIGHT_RED
    digit.draw()

board_list = reset_board()

while True:
    pygame.display.update()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #Assign a value
                for row in board_list:
                    for digit in row:
                        if pygame.Rect(game_to_pygame_Rect_coords(digit.game_coords)).collidepoint(event.pos):
                            digit.font_colour = LIGHT_BLUE
                            digit.draw()
                            pygame.display.update()
                            edit_digit(digit)

            if event.button == 3: #Attempt to solve the clicked square
                for row in board_list:
                    for digit in row:
                        if pygame.Rect(game_to_pygame_Rect_coords(digit.game_coords)).collidepoint(event.pos):
                            digit.value = digit_solver(digit)
                            digit.draw()
            
            if event.button == 2: #Attempt to solve the entire board
                total_solved = 0
                while total_solved != 81:
                    current_solved = total_solved    
                    for row in board_list:
                        for digit in row:
                            digit.value = digit_solver(digit)
                            digit.draw()
                            if digit.solved:
                                total_solved += 1
                                digit.solved = 0
                    if total_solved == current_solved:
                        print("Solved!", current_solved, total_solved)
                        break
            
        if event.type == pygame.KEYDOWN:

            if event.key == 114:
                board_list = reset_board() #Pressing "R" resets the board

            else:
                print(event.key) #Testing purposes

        if event.type == pygame.QUIT: sys.exit() #Exit the programm
