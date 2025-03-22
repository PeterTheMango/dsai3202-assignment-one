from mpi4py import MPI
import numpy as np
from src.genetic_algorithms_functions import (
    calculate_fitness, select_in_tournament,
    order_crossover, mutate, generate_unique_population
)
from time import time

def run_parallel(distance_matrix, num_nodes, population_size, num_tournaments, mutation_rate,
                 num_generations, infeasible_penalty, stagnation_limit):

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    global_best_fit = infeasible_penalty
    global_best_route = None
    
    np.random.seed(23 + rank)
    
    local_size = population_size // size
    
    local_population = generate_unique_population(local_size, num_nodes)
    
    local_best_fitness = infeasible_penalty
    stagnation_counter = 0
    
    start = time()
    
    for gen in range(num_generations):
        local_fit = np.array([-calculate_fitness(route, distance_matrix) for route in local_population])
        global_fit_values = np.zeros(population_size)
        comm.Allgather(local_fit, global_fit_values)
        
        best_fit = np.min(global_fit_values)
        
        if best_fit < global_best_fit:
            global_best_fit = best_fit
            idx = np.argmin(global_fit_values)
            
            combined_population = comm.allgather(local_population)
            global_population = [ind for sublist in combined_population for ind in sublist]
            global_best_route = global_population[idx]
            
            stagnation_counter = 0
            
            if rank == 0:
                print(f"FOUND BETTER GLOBAL FIT @ Generation {gen}: {global_best_fit}")
        else:
            stagnation_counter += 1
            
        if stagnation_counter >= stagnation_limit:
            if rank == 0:
                print(f"Regenerating population at generation {gen} due to stagnation")
            local_population = generate_unique_population(local_size, num_nodes)
            stagnation_counter = 0
            continue
        
        local_selected = select_in_tournament(local_population, local_fit, num_tournaments, tournament_size=3)
        
        offspring = []
        for i in range(0, len(local_selected), 2):
            parent1, parent2 = local_selected[i], local_selected[i + 1]
            child = order_crossover(parent1[1:], parent2[1:])
            offspring.append([0] + child)
        mutated_offspring = [mutate(route, mutation_rate) for route in offspring]
        
        worst_indices = np.argsort(local_fit)[-len(mutated_offspring):]
        for i, idx in enumerate(worst_indices):
            local_population[idx] = mutated_offspring[i]
            
        unique_population = set(tuple(ind) for ind in local_population)
        while len(unique_population) < local_size:
            individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
            if -calculate_fitness(individual, distance_matrix) < 1e6:
                unique_population.add(tuple(individual))
        local_population = [list(ind) for ind in unique_population]
        
        if rank == 0:
            print(f"Generation {gen}: Best fitness = {best_fit}")
            
    if rank == 0 and global_best_route is not None:
        print("Best Route:", [int(x) for x in global_best_route])
        print("Total Distance:", best_fit)
    
    return time() - start