from src.functions import seq_square
from time import time

def run_sequential(num_to_test):
    """Starts the sequential portion of the program.

    Args:
        num_to_test (float): Number of numbers to compute squares for.

    Returns:
        seq_time (float): Total time it took to run the sequential program.
    """
    seq_start = time()

    results = []

    for num in range(1, num_to_test + 1):
        results.append(seq_square(num))

    print(f"Total Number Of Squares Calculated: {len(results)}")
    print(f"Highest Square Calculated: {results[-1]}")

    seq_end = time()
    seq_time = seq_end - seq_start

    print(f"Total Sequential Time Taken: {seq_time}")
    return seq_time