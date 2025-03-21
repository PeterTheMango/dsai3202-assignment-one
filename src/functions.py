from multiprocessing import Queue

def seq_square(num: float) -> float:
    """
    Calculates the square of a single number.

    Args:
        num (float): The number to be squared.

    Returns:
        float: The square of the input number.
    """
    return num ** 2

def shared_square(num: int, shared_queue: Queue) -> None:
    """
    Calculates the square of each number in a chunk and puts the results into a shared queue.

    This function is intended to be used with multiprocessing. Each number in the
    provided chunk is squared, and the result is put into the shared multiprocessing queue.

    Args:
        chunk (list[int]): A list of integers to be squared.
        shared_queue (Queue): A multiprocessing queue used to store the results.
    """
    shared_queue.put(num ** 2)

    
def pool_square(chunk: list[int]) -> None:
    """
    Calculates the square of each number in a chunk and returns the results as a list.

    Intended to be used with multiprocessing.Pool methods like map or apply_async.

    Args:
        chunk (list[int]): A list of integers to be squared.

    Returns:
        list[int]: A list containing the squares of the input numbers.
    """
    return [num ** 2 for num in chunk]

def chunker(data: list[int], num_of_chunks: int) -> list[list[int]]:
    """
    Splits a list of data into evenly sized chunks for parallel processing.

    Args:
        data (list[int]): The full list of data to split.
        num_of_chunks (int): The number of chunks to create.

    Returns:
        list[list[int]]: A list containing `num_of_chunks` sublists of the original data.
    """
    chunk_size = len(data) // num_of_chunks
    remainder = len(data) % num_of_chunks

    chunks = []
    start = 0

    for i in range(num_of_chunks):
        end = start + chunk_size + (1 if i < remainder else 0)
        chunks.append(data[start:end])
        start = end

    return chunks