import itertools
import json
import random
import solve
import pruning

# Load puzzles from the JSON file
def load_puzzles(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        puzzles = json.load(f)
    return puzzles

# Generate Chain of Thought Data
def generate_long_cot_data(numbers):
    return solve.solve(numbers)

# Generate a full dataset with Long CoT from json
def generate_long_cot_dataset_from_puzzles(puzzle_file):
    dataset = []
    puzzles = load_puzzles(puzzle_file) 
    cards = []

    for numbers in puzzles:
        question = f"{numbers}"
        solution, log = generate_long_cot_data(numbers)
        log = pruning.compress_search_logs(log, 10)

        solution_str = "".join(solution)
        log_str = "".join(log)

        # Construct the training data
        data_point = {
            "instruction": "Solve the 24-point game problem.",
            "input": question,
            "output": f"{log_str}",
            "history": [],
        }
        dataset.append(data_point)

    return dataset

# Save the dataset to a JSON file
if __name__ == "__main__":
    dataset = generate_long_cot_dataset_from_puzzles("train_puzzles.json")  
    with open("train_data.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)
    print("Long CoT dataset generated: train_data.json")