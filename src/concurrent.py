from concurrent.futures import ProcessPoolExecutor, as_completed
from os import cpu_count
from src.functions import pool_square, chunker
from time import time

def run_pool(num_to_test): 
    """
    Executes multiprocessing using ProcessPoolExecutor to calculate squares of numbers.

    This function splits the range of numbers from 1 to `num_to_test` into chunks,
    and submits each chunk to a separate process using `ProcessPoolExecutor`.
    The function waits for all chunks to complete, aggregates the results, and
    prints the total and maximum value.

    Args:
        num_to_test (int): The maximum number to calculate the square for (inclusive).

    Returns:
        None
    """
    multi_pool_start = time()

    num_of_cores = cpu_count()
    data = [i for i in range(1, num_to_test + 1)]
    chunks = chunker(data, num_of_cores)

    num_results = []

    with ProcessPoolExecutor(max_workers=num_of_cores) as executor:
        futures = [executor.submit(pool_square, chunk) for chunk in chunks]
        for future in as_completed(futures):
            num_results.extend(future.result())

    print(f"Total Number Of Squares Calculated: {len(num_results)}")
    print(f"Highest Square Calculated: {max(num_results)}")

    multi_pool_end = time()
    multi_pool_time = multi_pool_end - multi_pool_start

    print(f"ProcessPoolExecutor Time Taken: {multi_pool_time}")