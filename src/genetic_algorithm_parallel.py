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

    if rank == 0:
        np.random.seed(42)
        population = generate_unique_population(population_size, num_nodes)
        best_calculate_fitness = int(infeasible_penalty)
        stagnation_counter = 0
        seq_time_start = time()
    else:
        population = None

    for generation in range(num_generations):
        # === Broadcast the current population ===
        population = comm.bcast(population, root=0)

        # === Scatter the workload for fitness calculation ===
        chunk_size = len(population) // size
        remainder = len(population) % size

        # Distribute population chunks
        if rank == 0:
            chunks = []
            start = 0
            for i in range(size):
                end = start + chunk_size + (1 if i < remainder else 0)
                chunks.append(population[start:end])
                start = end
        else:
            chunks = None

        local_chunk = comm.scatter(chunks, root=0)

        # Each process evaluates its chunk
        local_fitness = np.array([-calculate_fitness(route, distance_matrix, infeasible_penalty)
                                  for route in local_chunk])

        # Gather all fitness values
        all_fitness_values = comm.gather(local_fitness, root=0)

        if rank == 0:
            # Flatten the gathered fitness values
            calculate_fitness_values = np.concatenate(all_fitness_values)

            # Track best solution
            current_best_fitness = np.min(calculate_fitness_values)
            if current_best_fitness < best_calculate_fitness:
                best_calculate_fitness = current_best_fitness
                stagnation_counter = 0
            else:
                stagnation_counter += 1

            if stagnation_counter >= stagnation_limit:
                print(f"Regenerating population at generation {generation} due to stagnation")
                best_individual = population[np.argmin(calculate_fitness_values)]
                population = generate_unique_population(population_size - 1, num_nodes)
                population.append(best_individual)
                stagnation_counter = 0
                continue

            # Selection and reproduction
            selected = select_in_tournament(population,
                                            calculate_fitness_values,
                                            num_tournaments,
                                            tournament_size=3)

            offspring = []
            for i in range(0, len(selected), 2):
                parent1, parent2 = selected[i], selected[i + 1]
                route1 = order_crossover(parent1[1:], parent2[1:])
                offspring.append([0] + route1)

            mutated_offspring = [mutate(route, mutation_rate) for route in offspring]

            # Replace worst individuals
            for i, idx in enumerate(np.argsort(calculate_fitness_values)[::-1][:len(mutated_offspring)]):
                population[idx] = mutated_offspring[i]

            # Ensure uniqueness
            unique_population = set(tuple(ind) for ind in population)
            while len(unique_population) < population_size:
                individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
                unique_population.add(tuple(individual))
            population = [list(ind) for ind in unique_population]

            print(f"Generation {generation}: Best calculate_fitness = {current_best_fitness}")

    # Final fitness evaluation
    population = comm.bcast(population, root=0)
    local_chunk = comm.scatter([population[i::size] for i in range(size)], root=0)
    local_fitness = np.array([-calculate_fitness(route, distance_matrix, infeasible_penalty)
                              for route in local_chunk])
    all_fitness_values = comm.gather(local_fitness, root=0)

    if rank == 0:
        calculate_fitness_values = np.concatenate(all_fitness_values)
        best_idx = np.argmin(calculate_fitness_values)
        best_solution = population[best_idx]
        seq_time_end = time()

        print("============ Parallel Algorithm Run Metrics ============")
        print("Best Solution:", best_solution)
        print("Total Distance:", -calculate_fitness(best_solution, distance_matrix, infeasible_penalty))
        print(f"Total Time Taken: {seq_time_end - seq_time_start:.4f}s")
        return seq_time_end - seq_time_start
    else:
        return None
