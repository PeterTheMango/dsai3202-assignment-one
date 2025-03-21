from src.functions import shared_square, chunker
from multiprocessing import Queue, Process
from time import time

def run_loop(num_to_test):
    multi_loop_start = time()

    results = Queue()
    processes = []
        
    for num in range(1, num_to_test + 1):
        processes.append(Process(target=shared_square, args=(num, results)))
    
    for proc in processes:
        proc.start()
    
    for proc in processes:
        proc.join()
    
    num_results = []
    while not results.empty():
        num_results.append(results.get())
    
    print(f"Total Number Of Squares Calculated: {len(num_results)}")
    print(f"Highest Square Calculated: {num_results[-1]}")
    
    multi_loop_end = time()
    multi_loop_time = multi_loop_end - multi_loop_start
    
    print(f"Multiprocessing Loop Time Taken: {multi_loop_time}")
    return multi_loop_time
    