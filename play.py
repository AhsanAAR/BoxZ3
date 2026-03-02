import z3 as z
from z3 import *
from collections import defaultdict
import matplotlib.pyplot as plt

def all_smt(s, initial_terms):
    def block_term(s, m, t):
        s.add(t != m.eval(t, model_completion=True))
    def fix_term(s, m, t):
        s.add(t == m.eval(t, model_completion=True))
    def all_smt_rec(terms):
        if sat == s.check():
           m = s.model()
           yield m
           for i in range(len(terms)):
               s.push()
               block_term(s, m, terms[i])
               for j in range(i):
                   fix_term(s, m, terms[j])
               yield from all_smt_rec(terms[i:])
               s.pop()   
    yield from all_smt_rec(list(initial_terms))

def all_models(solver, vars):
    """
    Enumerate all models for the given solver and list/dict of variables.
    solver: a z3.Solver() with constraints already added
    vars: iterable of z3 variables
    """
    models = []

    while solver.check() == sat:
        m = solver.model()

        models.append({str(v): m[v] for v in vars})

        # Build a blocking clause for the current model
        block = []
        for v in vars:
            mv = m[v]
            # For Int, Bool, BitVec: use inequality
            block.append(v != mv)
        solver.add(Or(block))

    return models

import matplotlib.pyplot as plt

# Data
# N = [4, 5, 6, 7, 8, 9, 10]
# uniquely_solvable = [984, 982, 956, 963, 893, 874, 815]
# human_solvable = [984, 975, 922, 799, 379, 108, 13]

# # Create the plot
# plt.figure(figsize=(10, 6))
# plt.plot(N, uniquely_solvable, marker='o', linewidth=2, markersize=8, 
#          label='Uniquely Solvable', color='#3b82f6')
# plt.plot(N, human_solvable, marker='o', linewidth=2, markersize=8, 
#          label='Human-Solvable', color='#ef4444')

# # Customize the plot
# plt.xlabel('N', fontsize=14, fontweight='bold')
# plt.ylabel('Count', fontsize=14, fontweight='bold')
# plt.title('Solvability vs N', fontsize=16, fontweight='bold')
# plt.legend(fontsize=12)
# plt.grid(True, alpha=0.3)
# plt.xticks(N)
# plt.ylim(0, 1000)

# # Add some styling
# plt.tight_layout()

# # Save the plot
# plt.savefig('solvability_plot.png', dpi=300, bbox_inches='tight')

# # Display the plot
# plt.show()

# s = z.Solver()
# val = [2,4]
# vars = [z.Int(f"x_{i}") for i in range(len(val))]

# for i in range(len(val)):
#     s.add(z.Or(vars[i] == 0, vars[i] == val[i]))

# y = 5
# s.add(sum(vars) == y)
# if s.check() == z.sat:
#     print("ok")
# else:
#     print("not ok")

# while s.check() == z.sat:
#     print(all_smt(s, arr))
    # m = s.model()
    # print(s.model())

    # h = [z.Not(v == m[v]) for v in arr]
    # print(h)
    # s.add(z.Or(*h))

import matplotlib.pyplot as plt
import numpy as np

with open("experiment2.txt", "r") as file:
    answers = []
    values = []

    for line in file:
        s = line.split()
        answers.append(s[-2])
        values.append(int(s[-1]))  # convert to int!

    plt.plot(values)
    # plt.gca().invert_yaxis()

    # Fix: set evenly spaced ticks
    plt.yticks(range(min(values), max(values) + 1, 5))  # every 5 units, adjust as needed

    plt.xlabel('Iterations')
    plt.ylabel('Hints')
    plt.grid(True)
    plt.savefig('plot.png')