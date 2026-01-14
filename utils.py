def save_input(id):
    with open("input.txt", "r") as src, open(f"saved_{id}.txt", "a") as dest:
        dest.write(src.read())
