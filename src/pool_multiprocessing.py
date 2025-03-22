from multiprocessing import Pool, cpu_count
from src.functions import pool_square, chunker
from time import time

def run_pool_sync(num_to_test):
    """
    Run multiprocessing using pool.map for synchronous execution.

    This method splits the range of numbers into chunks and applies 
    the pool_square function to each chunk using pool.map, which blocks 
    until all tasks are complete.

    Args:
        num_to_test (int): The upper limit of numbers to square (starting from 1).

    Returns:
        float: The time taken to complete the multiprocessing task.
    """
    multi_pool_start = time()

    num_of_cores = cpu_count()
    data = [i for i in range(1, num_to_test + 1)]
    chunks = chunker(data, num_of_cores)

    with Pool(processes=num_of_cores) as pool:
        chunked_results = pool.map(pool_square, chunks)

    num_results = [num for chunk in chunked_results for num in chunk]

    print(f"Total Number Of Squares Calculated: {len(num_results)}")
    print(f"Highest Square Calculated: {num_results[-1]}")

    multi_pool_end = time()
    multi_pool_time = multi_pool_end - multi_pool_start

    print(f"Multiprocessing Loop Time Taken: {multi_pool_time}")
    return multi_pool_time


def run_apply_sync(num_to_test):
    """
    Run multiprocessing using pool.apply for synchronous execution.

    This method manually applies the pool_square function to each chunk 
    using pool.apply, which executes one task at a time per worker 
    and waits for it to finish before moving on.

    Args:
        num_to_test (int): The upper limit of numbers to square (starting from 1).

    Returns:
        float: The time taken to complete the multiprocessing task.
    """
    multi_pool_start = time()

    num_of_cores = cpu_count()
    data = [i for i in range(1, num_to_test + 1)]
    chunks = chunker(data, num_of_cores)

    num_results = []
    with Pool(processes=num_of_cores) as pool:
        results = [pool.apply(pool_square, args=(chunk,)) for chunk in chunks]
        for result in results:
            num_results.extend(result)

    print(f"Total Number Of Squares Calculated: {len(num_results)}")
    print(f"Highest Square Calculated: {num_results[-1]}")

    multi_pool_end = time()
    multi_pool_time = multi_pool_end - multi_pool_start

    print(f"Multiprocessing Loop Time Taken: {multi_pool_time}")
    return multi_pool_time


def run_pool_async(num_to_test):
    """
    Run multiprocessing using pool.map_async for asynchronous execution.

    This method applies the pool_square function to each chunk using 
    pool.map_async, which submits all tasks and then waits for the results 
    to be collected using .get().

    Args:
        num_to_test (int): The upper limit of numbers to square (starting from 1).

    Returns:
        float: The time taken to complete the multiprocessing task.
    """
    multi_pool_start = time()

    num_of_cores = cpu_count()
    data = [i for i in range(1, num_to_test + 1)]
    chunks = chunker(data, num_of_cores)

    with Pool(processes=num_of_cores) as pool:
        chunked_results = pool.map_async(pool_square, chunks).get()

    num_results = [num for chunk in chunked_results for num in chunk]

    print(f"Total Number Of Squares Calculated: {len(num_results)}")
    print(f"Highest Square Calculated: {num_results[-1]}")

    multi_pool_end = time()
    multi_pool_time = multi_pool_end - multi_pool_start

    print(f"Multiprocessing Loop Time Taken: {multi_pool_time}")
    return multi_pool_time


def run_apply_async(num_to_test):
    """
    Run multiprocessing using pool.apply_async for asynchronous execution.

    This method asynchronously submits each chunk to pool_square using 
    pool.apply_async and later retrieves the results using .get().

    Args:
        num_to_test (int): The upper limit of numbers to square (starting from 1).

    Returns:
        float: The time taken to complete the multiprocessing task.
    """
    multi_pool_start = time()

    num_of_cores = cpu_count()
    data = [i for i in range(1, num_to_test + 1)]
    chunks = chunker(data, num_of_cores)

    num_results = []
    with Pool(processes=num_of_cores) as pool:
        async_results = [pool.apply_async(pool_square, args=(chunk,)) for chunk in chunks]
        for async_result in async_results:
            num_results.extend(async_result.get())

    print(f"Total Number Of Squares Calculated: {len(num_results)}")
    print(f"Highest Square Calculated: {num_results[-1]}")

    multi_pool_end = time()
    multi_pool_time = multi_pool_end - multi_pool_start

    print(f"Multiprocessing Loop Time Taken: {multi_pool_time}")
    return multi_pool_time