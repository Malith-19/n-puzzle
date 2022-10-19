from copy import deepcopy
import random


class Node:
    def __init__(self, f, puzzle, parent, move):
        self.f = f
        self.puzzle = puzzle
        self.parent = parent
        self.move = move


# function to generate a random n puzzle
def generate_random_puzzle(size, blanks):
    puzzle = [str(i) for i in range(1, size * size - blanks + 1)]  # adding numbers to list
    puzzle += ["-" for i in range(blanks)]  # adding blanks to list
    random.shuffle(puzzle)

    puzzle_2d = []
    for i in range(size):
        puzzle_2d.append(puzzle[i * size:(i + 1) * size])

    goal = random_move(puzzle_2d)

    return puzzle_2d,goal

def random_move(puzzle):
    moves = random.randint(1,10)
    goal = deepcopy(puzzle)
    for i in range(moves):
        blank_locations = blank_finder(goal)
        moving_blank = blank_locations[random.randint(0,len(blank_locations)-1)]
        move_type = random.randint(0,3)

        if move_type == 0:
            move = move_left(goal,moving_blank)
            if move:
                goal = move[0]

        elif move_type == 1:
            move = move_right(goal,moving_blank)
            if move:
                goal = move[0]

        elif move_type == 2:
            move = move_up(goal,moving_blank)
            if move:
                goal = move[0]

        else:
            move = move_up(goal,moving_blank)
            if move:
                goal = move[0]

    return goal


# getting puzzle from a given file
def text_to_puzzle(filename):
    puzzle = []
    try:
        with open(filename, "r") as file:
            for line in file:
                puzzle.append(line.split())
    except FileNotFoundError:
        print(filename, "not founded please try again!")
        return
    except:
        print("Error occurred please try again!")
        return

    return puzzle


# getting input via filenames
def get_input():
    filenames = input("Enter the start configuration filename comma separated by goal configuration filename: ").split(
        ",")
    start_configuration_filename = filenames[0]
    goal_configuration_filename = filenames[1]

    starting_puzzle = text_to_puzzle(start_configuration_filename)
    goal_puzzle = text_to_puzzle(goal_configuration_filename)

    if starting_puzzle and goal_puzzle:
        return starting_puzzle, goal_puzzle

    return get_input()


# comparing puzzles using misplaced tiles
def compare_misplaced(puzzle1, puzzle2):
    differences = 0
    for i in range(len(puzzle1)):
        for j in range(len(puzzle1[0])):
            if puzzle1[i][j] != puzzle2[i][j]:
                differences += 1
    return differences


# function to get the index of the given element in a puzzle
def get_index(puzzle, size, element):
    for i in range(size):
        for j in range(size):
            if puzzle[i][j] == element:
                return [i, j]


# comparing puzzles using manhatten distance
def compare_manhattan(puzzle1, puzzle2):
    size = len(puzzle1)
    manhattan_difference = 0
    for i in range(size):
        for j in range(size):
            element = puzzle1[i][j]
            if element == "-":
                continue
            other_puzzle_location = get_index(puzzle2, size, element)
            manhattan_difference += abs(i - other_puzzle_location[0]) + abs(j - other_puzzle_location[1])
    return manhattan_difference


# finding the blank locations in a puzzle
def blank_finder(puzzle):
    rows = len(puzzle)
    columns = len(puzzle[0])

    blanks = []
    for i in range(rows):
        for j in range(columns):
            if puzzle[i][j] == "-":
                blanks.append([i, j])
    return blanks


def move_left(puzzle,blank_location):
    if blank_location[1] != 0:
        puzzle_left_copy = deepcopy(puzzle)
        move = "(" + puzzle_left_copy[blank_location[0]][
            blank_location[1] - 1] + ",right)"
        puzzle_left_copy[blank_location[0]][blank_location[1]] = puzzle_left_copy[blank_location[0]][
            blank_location[1] - 1]
        puzzle_left_copy[blank_location[0]][blank_location[1] - 1] = "-"
        return [puzzle_left_copy,move]


def move_right(puzzle,blank_location):
    if blank_location[1] != len(puzzle[0]) - 1:
        puzzle_right_copy = deepcopy(puzzle)
        move = "(" + puzzle_right_copy[blank_location[0]][
            blank_location[1] + 1] + ",left)"
        puzzle_right_copy[blank_location[0]][blank_location[1]] = puzzle_right_copy[blank_location[0]][
            blank_location[1] + 1]
        puzzle_right_copy[blank_location[0]][blank_location[1] + 1] = "-"
        return [puzzle_right_copy, move]

def move_up(puzzle,blank_location):
    if blank_location[0] != 0:
        puzzle_up_copy = deepcopy(puzzle)
        move = "(" + puzzle_up_copy[blank_location[0] - 1][blank_location[1]] + ",down)"
        puzzle_up_copy[blank_location[0]][blank_location[1]] = puzzle_up_copy[blank_location[0] - 1][blank_location[1]]
        puzzle_up_copy[blank_location[0] - 1][blank_location[1]] = "-"
        return [puzzle_up_copy, move]

def move_down(puzzle,blank_location):
    if blank_location[0] != len(puzzle) - 1:
        puzzle_down_copy = deepcopy(puzzle)
        move = "(" + puzzle_down_copy[blank_location[0] + 1][
            blank_location[1]] + ",up)"
        puzzle_down_copy[blank_location[0]][blank_location[1]] = puzzle_down_copy[blank_location[0] + 1][
            blank_location[1]]
        puzzle_down_copy[blank_location[0] + 1][blank_location[1]] = "-"
        return [puzzle_down_copy, move]
# function to do a one move in a puzzle.
def one_move(puzzle, blank_location):
    outputs = []

    # move left the blank
    movements = [move_left(puzzle,blank_location),move_right(puzzle,blank_location),move_up(puzzle,blank_location),move_down(puzzle,blank_location)]

    for move in movements:
        if move:
            outputs.append(move)

    return outputs


# function to print a given puzzle row by row
def print_puzzle(puzzle):
    for row in puzzle:
        print(" ".join(row))


# Function to move the all blanks to another position. But at one time only moving one blank.
def moves(puzzle, blank_locations):
    outputs = []

    for blank_location in blank_locations:
        moved_puzzles = one_move(puzzle, blank_location)
        outputs += moved_puzzles

    return outputs


# main solving function
def solve(starter, goal, depth=0):
    checked.append(starter.puzzle)

    blanks = blank_finder(starter.puzzle)
    results = moves(starter.puzzle, blanks)

    for result in results:
        puzzle = result[0]
        move = result[1]
        if puzzle in checked:
            continue
        # h = compare_misplaced(puzzle, goal) # getting misplaced tiles
        h = compare_manhattan(puzzle, goal) # getting manhattan distance
        # f = h + depth
        node = Node(depth + h, puzzle, starter, move)
        if h == 0:
            return node

        tree.append(node)
        checked.append(node)

    tree.sort(key=lambda x: x.f)
    return solve(tree.pop(0), goal, depth + 1)


# generating the path
def write_path(ending_node):
    if ending_node.parent:
        return write_path(ending_node.parent) + ", " + ending_node.move
    else:
        return ""


# driver code
tree = []
checked = []

# starter, goal = get_input()  # getting the starter and the goal puzzle
starter,goal = generate_random_puzzle(4,2)

print("Here is the starter puzzle")
print_puzzle(starter)

print("Here is the goal puzzle")
print_puzzle(goal)


starter_node = Node(0, starter, None, None)  # converting stater puzzle to node.

try:
    ending_node = solve(starter_node, goal)  # receiving ending(goal) puzzle as a node object which can back track to find
    # the path

    # printing the path to solve the puzzle
    print(write_path(ending_node))
except:
    print("Unsolvable")

