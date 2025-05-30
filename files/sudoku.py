# -*- coding: utf-8 -*-
"""Sudoku.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DIZkwdsc6k_inOcmO9VH2rPp4t1199X1

# User Interface Sudoku
"""

import random

def create_empty_grid():
    """
    Generates a 9x9 Sudoku puzzle with randomly filled boxes based on difficulty.

    Args:
        difficulty (str): Difficulty level, gets to choose between 'Easy', 'Normal', or 'Hard'.

    Returns:
        list: A 9x9 grid (list) where empty box are filled.
    """
    # Creates an empty 9x9 grid
    grid = []
    for row in range(9):
        new_row = []
        for col in range(9):
            new_row.append(0)
        grid.append(new_row)
    return grid

def fill_diagonal_box(grid, start_row, start_col):
    """
    Fills a 3x3 box with the numbers 1-9

    Args:
        grid(list): Sudoku list to change
       start_row: Row of 3x3
        start_col: Column of 3x3

    Returns:
        None
    """
    numbers = list(range(1, 10))

    for row_set in range(3):
        for col_set in range(3):
            #Pick a random index from remaining numbers chosen
            random_index = random.randint(0, len(numbers) - 1)
            chosen_number = numbers[random_index]

            #Place number into grid
            grid[start_row + row_set][start_col + col_set] = chosen_number

            #Remove the chosen number
            numbers.pop(random_index)

def is_valid(grid, row, col, num):
    """
    Checks if the place at row and col are valid

    Args:
        row (int): The row index (0-8).
        col (int): The column index (0-8).
        num (int): The number to place (1-9).

    Returns:
        bool: True if valid, False otherwise
    """
    #Checks if the number exist in the given row and column
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False

    start_row = row - row % 3 #Using operators to calculate the starting row for 3x3
    start_col = col - col % 3 #USing operators to calculate the starting column for 3x3

    #Checks to see if the number exist in 3x3 grid
    for i in range(9):
        if grid[start_row + i// 3][start_col + i % 3] == num:
            return False
    return True

def remove_numbers(grid, difficulty):
    """
    Removes numbers while ensuring the puzzle has a unique solution.

    Args:
        grid(list of int): Fully solved Sudoku grid
        difficulty (str): 'Easy', 'Normal', or 'Hard'

    Returns:
        None: Modifies grid in place
    """
    difficulty_map = {
        "Easy": 35,
        "Normal": 45,
        "Hard": 55
    }

    # Number of cells to remove
    cells_to_remove = difficulty_map.get(difficulty, 45)
    attempts = 0

    while cells_to_remove > 0 and attempts < 1000:
        row = random.randint(0, 8)
        col = random.randint(0, 8)

        if grid[row][col] != 0:
            # Save the value
            backup = grid[row][col]
            grid[row][col] = 0

            # Make a deep copy for testing
            copy = [r[:] for r in grid]
            if count_solutions(copy) != 1:
                # Not a unique solution → restore
                grid[row][col] = backup
            else:
                cells_to_remove -= 1
        attempts += 1

def solve_grid(grid):
    """
    Solves the puzzle using backtracking to generate a valid Sudoku board, which doesn't allow for errors given conditions

    Args:
        grid(list of int): The Sudoku puzzle to solve

    Returns:
        bool: True if the grid is solvable, False if isn't.
    """
    for row in range(9):
        for col in range(9):
            #Finding an empty cell
            if grid[row][col] == 0:
                #Trying all possible number from 1-9
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num # Places the number
                    #Solves the rest of grid
                        if solve_grid(grid):
                            return True
                        #Undos the move if it doesn't lead to a solution
                        grid[row][col] = 0
                #If number can't be placed
                return False
    #If no empty cell is left, will deem it solved
    return True

def count_solutions(grid):
    """
    Counts how many valid solutions exist for a given grid using backtracking.

    Args:
        grid (list): The Sudoku grid.

    Returns:
        int: Number of solutions (up to 2).
    """
    count = 0
    #Calling back the solve grid function
    def solve(grid):
        nonlocal count
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(grid, row, col, num):
                            grid[row][col] = num
                            solve(grid)
                            grid[row][col] = 0
                    return
        count += 1
        if count > 1:
            return  # Stop early if more than one solution

    solve(grid)
    return count

def create_puzzle(difficulty):
    """
    Creates a sudoku puzzle based on difficulty selected.

    Args:
        difficulty(str) Difficulty level selected

    Returns:
        list: Sudoku puzzle with some numbers removed
    """
    grid = create_empty_grid()

    #Fill 3 diagonal boxes
    for box_start in [0, 3, 6]:
        fill_diagonal_box(grid, box_start, box_start)
    solve_grid(grid)
    remove_numbers(grid, difficulty)
    return grid

def print_grid(grid):
    """
    Prints the current Sudoku grid with '.' as empty boxes and filled boxes show their number.

    Args:
        None

    Returns:
        None
    """
    #Print top border
    print("-" * 21)

    for row in range(9):
        row_str = ""

        for col in range(9):
            #Adds vertical wall for every columns after column 2 and 5
            if col in [3, 6]:
                row_str += "| "
            #Prints '.' for empty boxes
            if grid[row][col] == 0:
                row_str +=". "
            else:
                row_str += str(grid[row][col]) + " "

        #Prints the current row
        print(row_str)

        #Adds a horizontal row for every 3 rows
        if row in [2, 5]:
            print("-" * 21)

    # Print bottom border
    print("-" * 21)

def user_input(grid):
    """
    Allows the user to input a number in an empty box and updates the grid.

    Args:
        grid (list): The current 9x9 grid.

    Returns:
        None
    """
    print("Enter row, column, and number to put into the grid.")
    print("Type 'quit' to exit to the main menu.")

    while True:
        user_input_str = input("Enter your choice (row column number): ")

        # Allow quitting
        if user_input_str == "quit":
            print("Exiting current puzzle")
            return  # Exit back to choose_difficulty
            #Creating empty list
        input_values = []
        #Splitting each input using spaces, to make it clearer
        space = ""

        ##Looping through each space
        for char in user_input_str:
            if char == ' ':
                #Adds number to list
                if space != "":
                    input_values.append(space)
                space = ""
            else:
                space += char #Adds to end of the list
        #Adds last part of input if that needed
        if space != "":
            input_values.append(space)
            #Checks if 3 values were input, else it won't work.
            if len(input_values) != 3:
                print("Invalid, please try again")
            else:
                #Converts to integer
                row = int(input_values[0])
                col = int(input_values[1])
                num = int(input_values[2])

                #Checks if the row, column, and number are all within the correct ranges.
                if row < 1 or row > 9:
                    print("Invalid row.")
                else:
                    if col < 1 or col > 9:
                        print("Invalid column.")
                    else:
                        if num < 1 or num > 9:
                            print("Invalid number")
                        else:
                            if grid[row - 1][col - 1] != 0:
                                print("Box is already filled, please choose a different number.")
                            else:
                                #Checks to see if the number is already in the row.
                                number_in_row = False
                                for column_check in range(9):
                                    if grid[row - 1][column_check] == num:
                                        number_in_row = True

                                #Checks to see if the number is already in the column.
                                number_in_col = False
                                for row_check in range(9):
                                    if grid[row_check][col - 1] == num:
                                        number_in_col = True

                                #Checks to see if the number is already in the 3x3 grid.
                                number_in_box = False
                                start_row = (row - 1) - (row - 1) % 3
                                start_col = (col - 1) - (col - 1) % 3

                                for box_row in range(3):
                                    for box_col in range(3):
                                        current_row = start_row + box_row
                                        current_col = start_col + box_col
                                        if grid[current_row][current_col] == num:
                                            number_in_box = True
                                #If the number already exist
                                if number_in_row or number_in_col or number_in_box:
                                    print("Invalid, already exist in row, column, or box.")
                                else:
                                    grid[row - 1][col - 1] = num
                                    print(f"{num} at row {row}, column {col}.")
                                    print_grid(grid)
                                    #When the user completes the puzzle
                                    if check_win(grid):
                                        print("Congrats! You've successfully completed this puzzle!")
                                        return

def check_win(grid):
    """
    Checks if the current Sudoku grid is complete and correctly filled

    Args:
        grid(list): 9x9 Sudoku grid

    Returns:
        bool: True if the puzzle is complete and valid, False if it isn't.
    """
    #Creating helper function to check if the list has number 1-9 with no repetitions
    def is_valid_group(group):
        return sorted(group) == list(range(1,10))

    #Checks for the row
    for row in grid:
        if not is_valid_group(row):
            return False

    #Checks for column
    for col in range(9):
        column = [grid[row][col] for row in range(9)]
        if not is_valid_group(column):
            return False

    #Checks for 3x3 box
    for start_row in [0, 3, 6]:
        for start_col in [0, 3, 6]:
            box = []
            for row in range(3):
                for col in range(3):
                    box.append(grid[start_row + row][start_col + col])
            if not is_valid_group(box):
                return False
    return True

def show_instructions():
    """
    Shows thorough guidelines on how to play the game.

    Args:
        None

    Returns:
        None
    """
    #Instructions on how to play this game, read carefully to understand
    print("\n--- Welcome to Sudoku! ---")
    print("\n Instructions:")
    print(" The grid is 9x9. Empty cells are shown as '.' ")
    print(" To fill a box, type three numbers seperated by spaces:")
    print(" -> row column number ")
    print(" -> Example 3 4 5 (puts 5 in row 3, column 4)")
    print(" Only use numbers from 1 to 9 ")
    print(" Type quit anytime to stop playing. ")

def choose_difficulty():
    """
    Main function that ask the user for the difficulty, creates the puzzle, and allows interaction.
    """
    #Initial conditions for the game
    play_again = "Yes"

    while play_again == "Yes" or play_again == "yes" or play_again == "YES":
        show_instructions()
        print("Please enter one of the following difficulties: Easy, Normal, or Hard.")
        #Setting condition
        valid_input = False
    #Loops until the user enters a valid difficulty
        while valid_input == False:
            #Asks user to enter difficulty
            difficulty = input("Enter the difficulty (Easy, Normal, Hard): ").capitalize()

            if difficulty == "Easy" or difficulty == "Normal" or difficulty == "Hard":
                valid_input = True

                #Creates the puzzle
                grid = create_puzzle(difficulty)
            #If it was created successfully
                if grid is not None:
                    print("This is the puzzle. In it, '.' represents empty boxes:")
                    print_grid(grid)
                    # Allow for user input in the puzzle, allowing for interaction
                    user_input(grid)
            else:
                print("Invalid input. Please type Easy, Normal, or Hard")
    #Asks if they want to play again
        print("\n Would you like to play again?")
        play_again = input("Type Yes to play again , or No to quit.")


choose_difficulty()