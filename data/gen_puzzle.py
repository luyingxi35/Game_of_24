import json
import random
from itertools import permutations

def solvable(numbers):
    if len(numbers) != 4:
        return False
    
    EPSILON = 1e-6

    def dfs(cards):
        if len(cards) == 1:
            return abs(cards[0] - 24) < EPSILON

        for i in range(len(cards)):
            for j in range(i + 1, len(cards)):
                a, b = cards[i], cards[j]
                rest = [cards[k] for k in range(len(cards)) if k != i and k != j]

                new_nums = []
                new_nums.append(a + b)
                new_nums.append(a - b)
                new_nums.append(b - a)
                new_nums.append(a * b)
                if abs(b) > EPSILON:
                    new_nums.append(a / b)
                if abs(a) > EPSILON:
                    new_nums.append(b / a)

                for new_num in new_nums:
                    if dfs(rest + [new_num]):
                        return True

        return False
    
    for perm in permutations(numbers):
        if dfs(list(perm)):
            return True
    return False

def generate_puzzle(n, lower = 1, upper = 13):
    valid_sets = []
    seen = set()

    while len(valid_sets) < n:
        numbers = [random.randint(lower, upper) for _ in range(4)]
        numbers.sort()
        key = tuple(numbers)

        if key in seen:
            continue
        seen.add(key)

        if solvable(numbers):
            valid_sets.append(numbers)

    return valid_sets

if __name__ == '__main__':
    puzzles = generate_puzzle(1100)
    train = puzzles[:1000]
    test = puzzles[1000:]

    with open('train_puzzles_2.json', 'w') as f:
        json.dump(train, f)

    with open('test_puzzles_2.json', 'w') as f:
        json.dump(test, f)