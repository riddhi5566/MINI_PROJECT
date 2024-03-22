

from random import randint, shuffle


def print_board(board):
    boardString = ""
    for firstVar in range(9):
        for secondVar in range(9):
            boardString += str(board[firstVar][secondVar]) + " "
            if (secondVar + 1) % 3 == 0 and secondVar != 0 and secondVar + 1 != 9:
                boardString += "| "

            if secondVar == 8:
                boardString += "\n"

            if secondVar == 8 and (firstVar + 1) % 3 == 0 and firstVar + 1 != 9:
                boardString += "- - - - - - - - - - - \n"
    print(boardString)


def find_empty(board):
   

    for firstVar in range(9):
        for secondVar in range(9):
            if board[firstVar][secondVar] == 0:
                return (firstVar, secondVar)
    return None


def valid(board, pos, num):
   

    for firstVar in range(9):
        if board[firstVar][pos[1]] == num:
            return False

    for secondVar in range(9):
        if board[pos[0]][secondVar] == num:
            return False

    start_i = pos[0] - pos[0] % 3
    start_j = pos[1] - pos[1] % 3
    for firstVar in range(3):
        for secondVar in range(3):
            if board[start_i + firstVar][start_j + secondVar] == num:
                return False
    return True


def solve(board):
  
    empty = find_empty(board)
    if not empty:
        return True

    for nums in range(1, 10):
        if valid(board, empty, nums):
            board[empty[0]][empty[1]] = nums

            if solve(board):  # recursive step
                return True
            board[empty[0]][empty[1]] = 0  # this number is wrong so we set it back to 0
    return False


def generate_board():
   

    board = [[0 for firstVar in range(9)] for secondVar in range(9)]

    # Fill the diagonal boxes
    for firstVar in range(0, 9, 3):
        nums = list(range(1, 10))
        shuffle(nums)
        for row in range(3):
            for col in range(3):
                board[firstVar + row][firstVar + col] = nums.pop()

    # Fill the remaining cells with backtracking
    def fill_cells(board, row, col):
       
        if row == 9:
            return True
        if col == 9:
            return fill_cells(board, row + 1, 0)

        if board[row][col] != 0:
            return fill_cells(board, row, col + 1)

        for num in range(1, 10):
            if valid(board, (row, col), num):
                board[row][col] = num

                if fill_cells(board, row, col + 1):
                    return True

        board[row][col] = 0
        return False

    fill_cells(board, 0, 0)

    # Remove a greater number of cells to create a puzzle with fewer firstVar numbers
    for _ in range(randint(55, 65)):
        row, col = randint(0, 8), randint(0, 8)
        board[row][col] = 0

    return board


if __name__ == "__main__":
    board = generate_board()
    print_board(board)
    solve(board)
    print_board(board)
