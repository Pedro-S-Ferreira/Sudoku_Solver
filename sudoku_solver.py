import pygame, sys

pygame.init()
pygame.display.set_caption("Sudoku Solver")

SIZE = widht, height = 577, 577
BLACK = 0, 0, 0
WHITE = 220, 220, 220
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
    def __init__(self, value, game_coords, original, solved):
        self.value = value
        self.game_coords = game_coords
        self.original = original #If True, it wasn't guessed
        self.solved = solved # 0 if not, 1 if yes

    def draw(self):
        pygame.draw.rect(SCREEN, BLACK, game_to_real_coords_square(self.game_coords), 1)
        text = FONT.render(self.value, False, BLACK, WHITE)
        SCREEN.blit(text, game_to_real_coords_number(self.game_coords))

board_list = []

def reset_board():
    temp_list = []
    SCREEN.fill(WHITE) # Erase the board
    for x in range(9):
        temp_list.append([])
        for y in range(9):
            temp_list[x].append(Digit("0", (x, y), False, 0))
        for item in temp_list[x]: # Draw the board
            item.draw()
            text = FONT.render(item.value, False, BLACK, WHITE)
            SCREEN.blit(text, game_to_real_coords_number(item.game_coords))
        print(temp_list[x])
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
            if digit.value != "0":
                digit.solved = 1
            text = FONT.render(item.value, False, BLACK, WHITE)
            SCREEN.blit(text, game_to_real_coords_number(item.game_coords))

def digit_solver(position):
    if not board_list[position[0]][position[1]].value == "0": #Check that this square hasn't been solved.
        return board_list[position[0]][position[1]].value

    possible_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    cube_coords = [0, 0] #Temporary coordinates to then figure out in which cube it belongs to

    for y in range(9): #Check numbers in rows
        if board_list[position[0]][y].value in possible_list:
            try:
                possible_list.remove(board_list[position[0]][y].value)
            except:
                continue

    for x in range(9): #Check numbers in collumns
        if board_list[x][position[1]].value in possible_list:
            try:
                possible_list.remove(board_list[x][position[1]].value)
            except:
                continue
    
    cube_coords[0] = int(position[0] / 3)
    cube_coords[1] = int(position[1] / 3)

    for x in range(9): #Check numbers in correspondant cube
        for y in range(9):
            if int(board_list[x][y].game_coords[0] / 3) == cube_coords[0] and int(board_list[x][y].game_coords[1] / 3) == cube_coords[1]:
                if board_list[x][y].value in possible_list:
                    try:
                        possible_list.remove(board_list[x][y].value)
                    except:
                        continue

    if len(possible_list) == 1:
        return possible_list[0]
    else:
        print(possible_list)
        return "0"

board_list = reset_board()

while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #Assign a value
                for row in board_list:
                    for digit in row:
                        if pygame.Rect(game_to_pygame_Rect_coords(digit.game_coords)).collidepoint(event.pos):
                            digit.value = input("Clicked on: " + str (digit.game_coords) + ". What do you want its new value to be? (Current value is " + str(digit.value) + ") ")
                            digit.draw()

            if event.button == 3: #Attempt to solve the clicked square
                for row in board_list:
                    for digit in row:
                        if pygame.Rect(game_to_pygame_Rect_coords(digit.game_coords)).collidepoint(event.pos):
                            digit.value = digit_solver(digit.game_coords)
                            digit.draw()
            
            if event.button == 2: #Attempt to solve the entire board
                total_solved = 0
                while total_solved != 81:
                    current_solved = total_solved    
                    for row in board_list:
                        for digit in row:
                            digit.value = digit_solver(digit.game_coords)
                            digit.draw()
                            if digit.solved:
                                total_solved += 1
                    if total_solved == current_solved:
                        print("Sorry, couldn't solve it.")
                        break

        if event.type == pygame.QUIT: sys.exit() #Exit the programm