from solver_human import solver as human
import random
import argparse

def hints_solver(allowed_hints=0, msgs=False):
    with open('input.txt', 'r') as ansfile:
        N = int(ansfile.readline())
        ansfile.readline()
        ansfile.readline()
        ansfile.readline()
        ansfile.readline()

        ground_truth = []
        for r in range(N):
            ground_truth.append(list(map(int, ansfile.readline().split(',')))) 

    current_hints = 0
    hints = [[0 for _ in range(N)] for _ in range(N)]
    human_ans = -1

    while True:
        human_ans = human(msgs, True)

        if human_ans == 1:
            with open('hints.txt', 'w') as file:
                for r in hints:
                    file.write(f"{','.join(map(str,r))}\n")
            break

        if current_hints == allowed_hints:
            break

        with open('human_output.txt', 'r') as file:
            human_ans = []
            for _ in range(N):
                human_ans.append(list(map(int, file.readline().split(',')))) 
        
        random_r = random.randint(0,N-1)
        random_c = random.randint(0,N-1)

        while human_ans[random_r][random_c] != 0:
            random_r = random.randint(0,N-1)
            random_c = random.randint(0,N-1)        
        
        hints[random_r][random_c] = ground_truth[random_r][random_c]
        human_ans[random_r][random_c] = ground_truth[random_r][random_c]

        with open('human_input.txt', 'w') as file:
            for r in human_ans:
                file.write(f"{','.join(map(str,r))}\n")

        current_hints += 1
    
    return human_ans, current_hints

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates a random Box puzzle")
    parser.add_argument("h", type=int, help="Number of hints allowed")
    args = parser.parse_args()
        
    print(hints_solver(args.h, True))
    