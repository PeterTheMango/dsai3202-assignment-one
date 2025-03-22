import numpy as np
import pandas as pd
from mpi4py import MPI
from src.genetic_algorithm_sequential import run_sequentially
from src.genetic_algorithm_parallel import run_parallel
from warnings import filterwarnings
filterwarnings("ignore")

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Load the distance matrix (all processes will load the same data)
    if rank == 0:
        distance_matrix = pd.read_csv('./data/city_distances_extended.csv').to_numpy()
    else:
        distance_matrix = None

    distance_matrix = comm.bcast(distance_matrix, root=0)


    # Parameters
    num_nodes = distance_matrix.shape[0]
    population_size = 10000
    num_tournaments = 4  # Number of tournaments to run
    mutation_rate = 0.1
    num_generations = 200
    infeasible_penalty = 1e6  # Penalty for infeasible routes
    stagnation_limit = 5  # Number of generations without improvement before regeneration

    # Run sequential part on the master process only.
    if rank == 0:
        seq_time = run_sequentially(distance_matrix, 
                                    num_nodes, 
                                    population_size, 
                                    num_tournaments, 
                                    mutation_rate, 
                                    num_generations, 
                                    infeasible_penalty, 
                                    stagnation_limit)
        print("Sequential run time:", seq_time)
        print("\n\n")
    
    # Ensure all processes wait until the sequential part is finished.
    comm.Barrier()

    # Now run the parallel genetic algorithm across all MPI processes.
    par_time = run_parallel(distance_matrix, 
                            num_nodes, 
                            population_size, 
                            num_tournaments, 
                            mutation_rate, 
                            num_generations, 
                            infeasible_penalty, 
                            stagnation_limit)
    # Only rank 0 prints the parallel run time.
    if rank == 0:
        print("Parallel run time:", par_time)
        
        parallel_portion = 0.85
        speedup = seq_time / par_time
        efficiency = speedup / size
        amdahl_speedup = 1 / ((1 - parallel_portion) + (parallel_portion / size))
        gustafson_speedup = size - (1 - parallel_portion)  * (size - 1)
        
        print("======= Metrics ======= ")
        print(f"Speedup: {speedup}")
        print(f"Efficiency: {efficiency}")
        print(f"Amdahl's Speedup: {amdahl_speedup}")
        print(f"Gustafson's Speedup: {gustafson_speedup}")
