import numpy as np

def split_population(pop, num_chunks):
        chunks = []
        chunk_sizes = [len(pop) // num_chunks for _ in range(num_chunks)]
        for i in range(len(pop) % num_chunks):
            chunk_sizes[i] += 1
        index = 0
        for cs in chunk_sizes:
            chunks.append(pop[index:index + cs])
            index += cs
        return chunks

def flatten(data):
    """Recursively flattens any nested list-like structure and extracts integers."""
    flat = []

    def _flatten(x):
        if isinstance(x, (int, np.integer)):
            flat.append(int(x))
        elif isinstance(x, list) or isinstance(x, np.ndarray):
            for item in x:
                _flatten(item)
        else:
            raise TypeError(f"Unsupported type in gathered data: {type(x)} -> {x}")

    _flatten(data)
    return np.array(flat, dtype=np.int32)
