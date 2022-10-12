import copy

class Node:
    def __init__(self, f, puzzle):
        self.f = f
        self.puzzle = puzzle


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


def compare(puzzle1, puzzle2):
    differences = 0
    for i in range(len(puzzle1)):
        for j in range(len(puzzle1[0])):
            if puzzle1[i][j] != puzzle2[i][j]:
                differences += 1
    return differences


def blank_finder(puzzle):
    rows = len(puzzle)
    columns = len(puzzle[0])

    blanks = []
    for i in range(rows):
        for j in range(columns):
            if puzzle[i][j] == "-":
                blanks.append([i, j])
    return blanks


def one_move(puzzle, blank_location):
    outputs = []

    # move left
    if blank_location[1] != 0:
        puzzle_left_copy = copy.deepcopy(puzzle)
        puzzle_left_copy[blank_location[0]][blank_location[1]] = puzzle_left_copy[blank_location[0]][
            blank_location[1] - 1]
        puzzle_left_copy[blank_location[0]][blank_location[1] - 1] = "-"

        outputs.append(puzzle_left_copy)

    # move right
    if blank_location[1] != len(puzzle[0]) - 1:
        puzzle_right_copy = copy.deepcopy(puzzle)

        puzzle_right_copy[blank_location[0]][blank_location[1]] = puzzle_right_copy[blank_location[0]][
            blank_location[1] + 1]
        puzzle_right_copy[blank_location[0]][blank_location[1] + 1] = "-"
        outputs.append(puzzle_right_copy)

    # move up
    if blank_location[0] != 0:
        puzzle_up_copy = copy.deepcopy(puzzle)

        puzzle_up_copy[blank_location[0]][blank_location[1]] = puzzle_up_copy[blank_location[0] - 1][blank_location[1]]
        puzzle_up_copy[blank_location[0] - 1][blank_location[1]] = "-"
        outputs.append(puzzle_up_copy)

    # move down
    if blank_location[0] != len(puzzle)-1:
        puzzle_down_copy = copy.deepcopy(puzzle)

        puzzle_down_copy[blank_location[0]][blank_location[1]] = puzzle_down_copy[blank_location[0] + 1][
            blank_location[1]]
        puzzle_down_copy[blank_location[0] + 1][blank_location[1]] = "-"
        outputs.append(puzzle_down_copy)

    return outputs


# function to print a given puzzle row by row
def print_puzzle(puzzle):
    for row in puzzle:
        print(" ".join(row))



def moves(puzzle, blank_locations):
    outputs = []

    for blank_location in blank_locations:
        moved_puzzles = one_move(puzzle, blank_location)
        outputs += moved_puzzles

    return outputs


tree = []
checked = []

def solve(starter, goal, depth=0):
    checked.append(starter)
    print_puzzle(starter)
    print("  |  ")
    print("  |  ")
    print("  V  ")

    blanks = blank_finder(starter)
    results = moves(starter, blanks)

    for result in results:
        if result in checked:
            continue
        h = compare(result, goal)
        if h == 0:
            return
        # f = h + depth
        node = Node(depth + h, result)

        tree.append(node)

    tree.sort(key=lambda x: x.f)
    solve(tree[0].puzzle, goal, depth + 1)


starter, goal = get_input()
solve(starter, goal)
