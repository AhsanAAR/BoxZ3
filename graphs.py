import matplotlib.pyplot as plt

# --- Data ---
n = [2, 3, 4, 5]

# Normal Cube
cube_uniquely_solvable = [951, 544, 100, 5]
cube_human_solvable    = [885, 290, 17, 0]

# Prime Variant
prime_uniquely_solvable = [977, 634, 254, 127]
prime_human_solvable    = [949, 438, 43, 1]

def annotate(ax, n, data, color, offset):
    for x, y in zip(n, data):
        ax.annotate(f'{y}', (x, y), textcoords='offset points', xytext=offset, ha='center', fontsize=9, color=color)

# --- Plot 1: Normal Cube ---
fig1, ax1 = plt.subplots(figsize=(8, 6))
ax1.plot(n, cube_uniquely_solvable, marker='o', linewidth=2, color='steelblue', label='Uniquely Solvable')
annotate(ax1, n, cube_uniquely_solvable, 'steelblue', (-15, 8))
ax1.plot(n, cube_human_solvable, marker='s', linewidth=2, color='orange', label='Human-Solvable')
annotate(ax1, n, cube_human_solvable, 'orange', (15, 8))
ax1.set_xlabel('N', fontsize=12)
ax1.set_ylabel('Count', fontsize=12)
ax1.set_title('Normal Cube: Uniquely Solvable vs Human-Solvable', fontsize=13)
ax1.legend(fontsize=11)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.set_xticks(n)
fig1.tight_layout()
fig1.savefig('plot_cube.png', dpi=150)

# --- Plot 2: Prime Variant ---
fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.plot(n, prime_uniquely_solvable, marker='o', linewidth=2, color='steelblue', label='Uniquely Solvable')
annotate(ax2, n, prime_uniquely_solvable, 'steelblue', (-15, 8))
ax2.plot(n, prime_human_solvable, marker='s', linewidth=2, color='orange', label='Human-Solvable')
annotate(ax2, n, prime_human_solvable, 'orange', (15, 8))
ax2.set_xlabel('N', fontsize=12)
ax2.set_ylabel('Count', fontsize=12)
ax2.set_title('Prime Variant: Uniquely Solvable vs Human-Solvable', fontsize=13)
ax2.legend(fontsize=11)
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.set_xticks(n)
fig2.tight_layout()
fig2.savefig('plot_prime.png', dpi=150)

# plt.show()