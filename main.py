from src.sequential import run_sequential
from src.loop_multiprocessing import run_loop
from src.pool_multiprocessing import run_pool, run_apply
from src.database import run_database
from src.concurrent import run_pool


if __name__ == "__main__":
    num_to_test = 10000000
    max_connections = 3
    num_of_processes = 6

    print("========= Sequential Data =========")
    seq_time = run_sequential(num_to_test)
    print("========= Loop Data =========")
    # multiprocessing_loop_time = run_loop(num_to_test)
    print("Multiprocessing Loop Stopped As System Does Not Have Enough Resources.")
    print("========= Pool Data =========")
    multiprocessing_pool_time = run_pool(num_to_test)
    print("========= Pool Apply Data =========")
    multiprocessing_pool_time = run_apply(num_to_test)
    print("========= ProcessPoolExecutor Data =========")
    multiprocessing_pool_time = run_pool(num_to_test)
    print("\n\n=======================================")
    
    run_database(max_connections, num_of_processes)
