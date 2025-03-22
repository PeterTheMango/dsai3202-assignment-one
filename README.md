
# DSAI3202 - Assignment Part Two

This repo contains all code related to part two of the DSAI3202 Assignment One.

## Authors
- [@PeterTheMango [60301211]](https://www.github.com/PeterTheMango)

# Objectives

- Develop Python programs that run the uses genetic algorithms in a distributed fashion using MPI4PY or Celery.
- The goal of this assignment is to use a genetic algorithm to optimize the routes for a fleet of delivery vehicles in a city. **The objective is to minimize the total distance traveled by all vehicles while ensuring that each delivery node in the city is visited exactly once by any vehicle**. In this version, we will start with one car that must go through all the nodes

# Tasks
## Completing the functions
### calculate_fitness
![enter image description here](https://izsf0fvi1i.ufs.sh/f/X2JLT2PTUuxwHrM8sFklmakOBv4Ayi3cjVGbrThYpe8R9LSJ)
> To calculate the fit of a specific route, what we will do is loop through each index from 0 to len - 1 so that we can analyze the distance between node_1 and node 2. If we find the the distance is unfeasible, we immediately return the penalty. If not, we add it to the distance and continue with the next route. Lastly, we evaluate the distance from the last point to the depot (initial point). If it is invalid, we return negative penalty, if not we then add it to the total distance and return that.
### select_in_tournament
![enter image description here](https://izsf0fvi1i.ufs.sh/f/X2JLT2PTUuxwIjWsGfCLZivCU2GXqlArm7KDHWVe4kcjwOJg)
> We will iterate from 0 to num_of_tournaments that was defined in the parameters of the program. Where we select **tournament_size** amount of choices from the population where we then look for which item has the best score. Once we found that we then add it to the list and return the list back after the program is finished.


## Questions

- Explain the program outlined in the script
	- First we generate different routes based on population_size defined in our parameters.
	- We then keep track of what the best calculated fitness score is as well as if there are no improvements between each calculation.
	- We then loop from 0 to num_of_generations defined in the parameters.
	- We calculate the fit for each generation and multiply it by -1 to maximize the fitness
	- We then compare if it has improved or not. 
	- If it has not improved based on the limit defined we regenerate the population again and restart the loop.
	- We then select the best route to take using tournament selection function.
	- We then choose two parents to create an offspring route using the crossover function.
	- We slightly mutate the offspring to look for new routes.
	- We then replace the worst individual with the offspring made
	- We then check to see if all routes are unique
- Define the parts to be distributed and parallelized, explain your choices
	- > The function calls for calculating fit, tournament selection, mutation, crossover can all be done in parallel as the results are not dependent on one another. 
- How would you add more cars to the problem (Extended)? 
	- > Instead of one car visiting each node, we split the nodes to k amount of cars and let each car generate its own unique route to follow in order to ensure that the nodes are visited at most once except for the initial point.

# Results

> *Program ran on 16 processes distributed among 3 machines with 6 cores available on each.*

**city_distances.csv:**
| Metric              | Sequential      | Parallel        |
|---------------------|------------------|------------------|
| Time Taken (s)     | 13.14         | 6.23         |
| Speedup    | 1.0          |  2.11       |
| Efficiency     | 1.0             |   0.11       |
| Amdahl’s Speedup        | N/A             |    3.43   |
| Gustafson’s Speedup         | N/A         |13.75 |



# Additional Comments
### AWS Implementation
Can be distributed to AWS Machines using the following command.

    mpirun -n 16 --hostfile aws_machines.txt python main.py 

### How to run the program?

    mpirun -n 16 --hostfile machines.txt python main.py

# Acknowledgement
> OpenAI ChatGPT-4o and o3-mini-high model for helping with diagnosing the errors that was present when implementing MPI4PY as well as the docstrings of the functions. 