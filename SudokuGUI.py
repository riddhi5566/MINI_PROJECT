from sudokutools import valid, solve, find_empty, generate_board
from copy import deepcopy
from sys import exit
import pygame
import time
import random

pygame.init()


class Board:
    def __init__(self, window):
       
        # Generate a new Sudoku board and create a solved version of it.
        self.board = generate_board()
        self.solvedBoard = deepcopy(self.board)
        solve(self.solvedBoard)
        # Create a 2D list of Tile objects to represent the Sudoku board.
        self.tiles = [
            [Tile(self.board[firstVar][secondVar], window, firstVar * 60, secondVar * 60) for secondVar in range(9)]
            for firstVar in range(9)
        ]
        self.window = window

    def draw_board(self):

        for firstVar in range(9):
            for secondVar in range(9):
                # Draw vertical lines every three columns.
                if secondVar % 3 == 0 and secondVar != 0:
                    pygame.draw.line(
                        self.window,
                        (0, 0, 0),
                        (secondVar // 3 * 180, 0),
                        (secondVar // 3 * 180, 540),
                        4,
                    )
                # Draw horizontal lines every three rows.
                if firstVar % 3 == 0 and firstVar != 0:
                    pygame.draw.line(
                        self.window,
                        (0, 0, 0),
                        (0, firstVar // 3 * 180),
                        (540, firstVar // 3 * 180),
                        4,
                    )
                # Draw the Tile object on the board.
                self.tiles[firstVar][secondVar].draw((0, 0, 0), 1)

                # Display the Tile value if it is not 0 (empty).
                if self.tiles[firstVar][secondVar].value != 0:
                    self.tiles[firstVar][secondVar].display(
                        self.tiles[firstVar][secondVar].value, (21 + secondVar * 60, 16 + firstVar * 60), (0, 0, 0)
                    )
        # Draw a horizontal line at the bottom of the board.
        pygame.draw.line(
            self.window,
            (0, 0, 0),
            (0, (firstVar + 1) // 3 * 180),
            (540, (firstVar + 1) // 3 * 180),
            4,
        )

    def deselect(self, tile):
       
        for firstVar in range(9):
            for secondVar in range(9):
                if self.tiles[firstVar][secondVar] != tile:
                    self.tiles[firstVar][secondVar].selected = False

    def redraw(self, keys, wrong, time):
       
        self.window.fill((255, 255, 255))  # fill the window with white
        self.draw_board()  # draw the Sudoku board
        for firstVar in range(9):
            for secondVar in range(9):
                if self.tiles[secondVar][firstVar].selected:
                    # highlight selected tiles in green
                    self.tiles[secondVar][firstVar].draw((50, 205, 50), 4)
                elif self.tiles[firstVar][secondVar].correct:
                    # highlight correct tiles in dark green
                    self.tiles[secondVar][firstVar].draw((34, 139, 34), 4)
                elif self.tiles[firstVar][secondVar].incorrect:
                    # highlight incorrect tiles in red
                    self.tiles[secondVar][firstVar].draw((255, 0, 0), 4)

        if len(keys) != 0:
            for value in keys:
                # display the potential values for each tile
                self.tiles[value[0]][value[1]].display(
                    keys[value],
                    (21 + value[0] * 60, 16 + value[1] * 60),
                    (128, 128, 128),
                )

        if wrong > 0:
            # display the current wrong count as an "X" icon and a number
            font = pygame.font.SysFont("Bauhaus 93", 30)
            text = font.render("X", True, (255, 0, 0))
            self.window.blit(text, (10, 554))

            font = pygame.font.SysFont("Bahnschrift", 40)
            text = font.render(str(wrong), True, (0, 0, 0))
            self.window.blit(text, (32, 542))

        # display the current time elapsed as a number
        font = pygame.font.SysFont("Bahnschrift", 40)
        text = font.render(str(time), True, (0, 0, 0))
        self.window.blit(text, (388, 542))
        pygame.display.flip()  # update the game window

    def visualSolve(self, wrong, time):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()  # exit the game if the user clicks the close button

        empty = find_empty(self.board)
        if not empty:
            return True  # the board is solved if there are no empty tiles left

        for nums in range(9):
            if valid(self.board, (empty[0], empty[1]), nums + 1):
                # fill in the current empty tile with a valid number
                self.board[empty[0]][empty[1]] = nums + 1
                self.tiles[empty[0]][empty[1]].value = nums + 1
                self.tiles[empty[0]][empty[1]].correct = True
                pygame.time.delay(63)  # delay to slow down the solving animation
                self.redraw(
                    {}, wrong, time
                )  # redraw the game window with the updated board

                if self.visualSolve(wrong, time):
                    return True  # recursively solve the rest of the board if the current move is valid

                # if the current move is not valid, reset the tile and highlight it as incorrect
                self.board[empty[0]][empty[1]] = 0
                self.tiles[empty[0]][empty[1]].value = 0
                self.tiles[empty[0]][empty[1]].incorrect = True
                self.tiles[empty[0]][empty[1]].correct = False
                pygame.time.delay(63)  # delay to slow down the solving animation
                self.redraw(
                    {}, wrong, time
                )  # redraw the game window with the updated board

    def hint(self, keys):

        while True:
            firstVar = random.randint(0, 8)
            secondVar = random.randint(0, 8)
            if self.board[firstVar][secondVar] == 0:
                if (secondVar, firstVar) in keys:
                    del keys[(secondVar, firstVar)]
                # fill in the selected empty tile with the correct number
                self.board[firstVar][secondVar] = self.solvedBoard[firstVar][secondVar]
                self.tiles[firstVar][secondVar].value = self.solvedBoard[firstVar][secondVar]
                return True
            elif self.board == self.solvedBoard:
                return False  # the board is already solved, so no hint can be provided.


class Tile:
    def __init__(
        self,
        value,
        window,
        x1,
        y1,
    ):


        self.value = value
        self.window = window
        self.rect = pygame.Rect(x1, y1, 60, 60)
        self.selected = False
        self.correct = False
        self.incorrect = False

    def draw(self, color, thickness):
       

        pygame.draw.rect(self.window, color, self.rect, thickness)

    def display(
        self,
        value,
        position,
        color,
    ):
        

        font = pygame.font.SysFont("lato", 45)
        text = font.render(str(value), True, color)
        self.window.blit(text, position)

    def clicked(self, mousePos):


        if self.rect.collidepoint(mousePos):
            self.selected = True
        return self.selected


def main():
    # Set up the pygame window
    screen = pygame.display.set_mode((540, 590))
    screen.fill((255, 255, 255))
    pygame.display.set_caption("Sudoku Solver")
    icon = pygame.image.load("D:\MINI PROJECT_1\MINI_PROJECT/assets/thumbnail.png")
    pygame.display.set_icon(icon)

    # Display "Generating Random Grid" text while generating a random grid
    font = pygame.font.SysFont("Bahnschrift", 40)
    text = font.render("Generating", True, (0, 0, 0))
    screen.blit(text, (175, 245))

    font = pygame.font.SysFont("Bahnschrift", 40)
    text = font.render("Random Grid", True, (0, 0, 0))
    screen.blit(text, (156, 290))
    pygame.display.flip()

    # Initialize variables
    wrong = 0
    board = Board(screen)
    selected = (-1, -1)
    keyDict = {}
    solved = False
    startTime = time.time()

    # Loop until the sudoku is solved
    while not solved:
        # Get elapsed time and format it to display in the window
        elapsed = time.time() - startTime
        passedTime = time.strftime("%H:%M:%S", time.gmtime(elapsed))

        # Check if the sudoku is solved
        if board.board == board.solvedBoard:
            solved = True

        # Handle events
        for event in pygame.event.get():
            elapsed = time.time() - startTime
            passedTime = time.strftime("%H:%M:%S", time.gmtime(elapsed))
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                # Check if a Tile is clicked
                mousePos = pygame.mouse.get_pos()
                for firstVar in range(9):
                    for secondVar in range(9):
                        if board.tiles[firstVar][secondVar].clicked(mousePos):
                            selected = (firstVar, secondVar)
                            board.deselect(board.tiles[firstVar][secondVar])
            elif event.type == pygame.KEYDOWN:
                # Handle key presses
                if board.board[selected[1]][selected[0]] == 0 and selected != (-1, -1):
                    if event.key == pygame.K_1:
                        keyDict[selected] = 1

                    if event.key == pygame.K_2:
                        keyDict[selected] = 2

                    if event.key == pygame.K_3:
                        keyDict[selected] = 3

                    if event.key == pygame.K_4:
                        keyDict[selected] = 4

                    if event.key == pygame.K_5:
                        keyDict[selected] = 5

                    if event.key == pygame.K_6:
                        keyDict[selected] = 6

                    if event.key == pygame.K_7:
                        keyDict[selected] = 7

                    if event.key == pygame.K_8:
                        keyDict[selected] = 8

                    if event.key == pygame.K_9:
                        keyDict[selected] = 9
                    elif (
                        event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE
                    ):
                        if selected in keyDict:
                            board.tiles[selected[1]][selected[0]].value = 0
                            del keyDict[selected]
                    elif event.key == pygame.K_RETURN:
                        if selected in keyDict:
                            if (
                                keyDict[selected]
                                != board.solvedBoard[selected[1]][selected[0]]
                            ):
                                wrong += 1
                                board.tiles[selected[1]][selected[0]].value = 0
                                del keyDict[selected]
                                # break

                            board.tiles[selected[1]][selected[0]].value = keyDict[
                                selected
                            ]
                            board.board[selected[1]][selected[0]] = keyDict[selected]
                            del keyDict[selected]

                # Handle hint key
                if event.key == pygame.K_h:
                    board.hint(keyDict)

                # Handle space key
                if event.key == pygame.K_SPACE:
                    # Deselect all tiles and clear keyDict
                    for firstVar in range(9):
                        for secondVar in range(9):
                            board.tiles[firstVar][secondVar].selected = False
                    keyDict = {}

                    # Solve the sudoku visually and reset all tile correctness
                    elapsed = time.time() - startTime
                    passedTime = time.strftime("%H:%M:%S", time.gmtime(elapsed))
                    board.visualSolve(wrong, passedTime)
                    for firstVar in range(9):
                        for secondVar in range(9):
                            board.tiles[firstVar][secondVar].correct = False
                            board.tiles[firstVar][secondVar].incorrect = False

                    # Set solved to True after solving the sudoku:
                    solved = True

        board.redraw(keyDict, wrong, passedTime)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


main()
pygame.quit()
