from src.sequential import run_sequential
from src.loop_multiprocessing import run_loop
from src.pool_multiprocessing import run_pool_async, run_apply_async, run_apply_sync, run_pool_sync
from src.database import run_database
from src.concurrent import run_pool


if __name__ == "__main__":
    num_to_test = int(10e7)
    max_connections = 3
    num_of_processes = 6

    print("========= Sequential Data =========")
    seq_time = run_sequential(num_to_test)
    print("========= Loop Data =========")
    # multiprocessing_loop_time = run_loop(num_to_test)
    print("Multiprocessing Loop Stopped As System Does Not Have Enough Resources.")
    print("========= Pool Data =========")
    multiprocessing_pool_time = run_pool_sync(num_to_test)
    print("========= Pool Apply Data =========")
    multiprocessing_pool_time = run_apply_sync(num_to_test)
    print("========= Pool Data ASYNC =========")
    multiprocessing_pool_time = run_pool_async(num_to_test)
    print("========= Pool Apply Data ASYNC =========")
    multiprocessing_pool_time = run_apply_async(num_to_test)
    print("========= ProcessPoolExecutor Data =========")
    multiprocessing_pool_time = run_pool(num_to_test)
    print("\n\n=======================================")
    
    run_database(max_connections, num_of_processes)
