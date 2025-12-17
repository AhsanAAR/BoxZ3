from generate import generate
from solver_human import solver
from collections import defaultdict

counter = defaultdict(int)

for _ in range(300):
    generate(7)
    counter[solver()] += 1

print(counter)
