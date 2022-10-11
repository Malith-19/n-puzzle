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


starter, goal = get_input()

print(starter,"\n",goal)
print(compare(starter, goal))
