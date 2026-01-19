def save_input(id):
    with open("input.txt", "r") as src, open(f"saved_{id}.txt", "a") as dest:
        dest.write(src.read())

def grid_to_binary(grid):
    return "".join(str(val) for row in grid for val in row)
