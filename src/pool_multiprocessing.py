from multiprocessing import Pool, cpu_count
from src.functions import pool_square, chunker
from time import time

def run_pool(num_to_test): 
    """
    Executes multiprocessing using Pool.map to calculate squares of numbers.

    This function divides the range of numbers from 1 to `num_to_test` into chunks,
    and distributes them across CPU cores using `Pool.map`. Each chunk is processed
    using the `pool_square` function.

    Args:
        num_to_test (int): The maximum number to calculate the square for (inclusive).

    Returns:
        float: The total time taken to execute the multiprocessing task.
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

def run_apply(num_to_test):
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