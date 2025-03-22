
# DSAI3202 - Assignment Part One

This repo contains all code related to part one of the DSAI3202 Assignment One.

## Authors
- [@PeterTheMango [60301211]](https://www.github.com/PeterTheMango)

# Objectives

- Develop Python programs that take advantage of python multiprocessing capabilities.

# Task One

Create e function square that computes the square number of an int.

- Create a list of 10e6 (1,000,000) numbers.

- Time the program in these scenarios on the random list.

- A sequential for loop.

- A multiprocessing for loop with a process for each number.

- A multiprocessing pool with both map() and apply().

- A concurrent.futures ProcessPoolExecutor.

- Redo the test with 10e7 (10,000,000) numbers.

## Results
**1,000,000 Numbers:**
| Method | Time Taken (s)|
|--|--|
| Sequential | 0.8 |
| MP Loop | DNF |
| Pool Apply | 2.40 |
| Pool Map | 1.57 |
| Pool Apply Async | 1.48 |
| Pool Map Async | 1.40 |
| Concurrent Futures | 1.39 |

**10,000,000 Numbers:**
| Method | Time Taken (s)|
|--|--|
| Sequential | 7.31 |
| MP Loop | DNF |
| Pool Apply | 25.43 |
| Pool Map | 15.43 |
| Pool Apply Async | 14.68 |
| Pool Map Async | 16.48 |
| Concurrent Futures | 14.74 |


## Questions

- What are your conclusions?
	- Multiprocessing is not particularly effective in this type of task. Based on the results above, we can clearly see the handling the data sequentially has shown much better results rather than processing the data in parallel. This is caused by the fact that the implementation of multiprocessing greatly increased the overhead when the task itself is already relatively light which shows that the benefit does not outweigh the cost of it.

# Task Two
In order to experiment on how to use semaphores in Python’s multiprocessing module to manage access to a limited pool of resources. Implement a **ConnectionPool** class that simulates a pool of database connections, using a **semaphore** to control access.
- Create a ConnectionPool class with methods to get and release connections, using a semaphore to limit access.
- Write a function that simulates a process performing a database operation by acquiring and releasing a connection from the pool.
- Observe how the semaphore ensures that only a limited number of processes can access the pool at any given time.

## Questions
- What happens if more processes try to access the pool than there are available connections?
	- > Since if there are already X amount of process taking up the available lock space defined in the semaphore lock, they will be put in a waiting state where it will wait until a processes releases the lock signifying that it is ready for more operations.
- How does the semaphore prevent race conditions and ensure safe access to the connections?
	- > This eliminates the issue of when multiple connections are trying to edit the same data because only the process that was able to acquire the lock can edit it and no other process can do the same at the same time until the lock is released.

# Acknowledgement
> OpenAI ChatGPT-4o model for helping with diagnosing the errors that was present when implementing the synchronous and asynchronous version of the multiprocessing pools as well as the docstrings of each function. 
