def human_solver(Box, partial_solution):
    current = partial_solution

    while True:
        solver = z3.Solver()
        add_constraints(solver, current, Box)

        next = solver.model()

        if undecided not in next:
            return True, next
        
        if next == current:
            return False, next
        
        current = next

def human_solvable(Box, N):
    blank_state = initialize_undecided(N)

    return human_solver(Box, blank_state)


def random_search(N):
    while True:
        puzzle = generate_box(N)
        solvable, _ = human_solvable(puzzle, N)

        if solvable:
            return True
        
def generate_uniquely_solvable_box(N):
    puzzle, answer = generate_box(N)
    no_of_sols = z3_solver(puzzle, N)

    while no_of_sols != 1:
        puzzle, answer = generate_box(N)
        no_of_sols = z3_solver(puzzle, N)
    
    return (puzzle, answer)

def random_search_with_uniqueness(N):
    while True:
        puzzle, answer = generate_uniquely_solvable_box(N)
        solvable, _ = human_solvable(puzzle, N)

        if solvable:
            return True
        
def human_solver_with_hints(Box, N, answer, allowed_hints):
    current_hints = 0
    hints = {}
    current_state = initialize_undecided(N)

    while True:
        solvable, next_state = human_solver(Box, current_state)

        if solvable:
            return (True, hints)
        
        if current_hints == allowed_hints:
            return (False, Null)
        
        new_hint = pick_random_hint(next_state, answer)
        hints.add(new_hint)

        current_state = apply_hint(new_hint, next_state)

        current_hints += 1
    
def generate_human_solvable_3(N, unique, threshold, hints_start):
    allowed_hints = hints_start

    while True:
        for i in range(threshold):
            puzzle, answer = generate_uniquely_solvable_box(N)

            solvable, hints = human_solver_with_hints(puzzle, N, answer, allowed_hints)

            if solvable:
                return (puzzle, answer, hints)
            
        allowed_hints += 1


def generate_human_solvable_3(N, terminating_condition, tries):
    allowed_hints = infinity

    solution_puzzle = Null
    solution_answer = Null
    solution_hints = Null
    
    while not terminating_condition():
        puzzle, answer = generate_box(N)
        
        for i in range(tries):
            if terminating_condition():
                break

            solvable, current_hints = human_solver_with_hints(puzzle, N, answer, allowed_hints)

            if solvable:
                solution_puzzle = puzzle
                solution_answer = answer
                solution_hints = current_hints

                allowed_hints = current_hints - 1
    
    return (solution_puzzle, solution_answer, solution_hints)
