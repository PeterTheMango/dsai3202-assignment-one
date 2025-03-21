from multiprocessing import Semaphore, Manager, current_process, Process
from random import uniform
from time import sleep

class ConnectionPool:
    """
    A class that simulates a pool of database connections controlled by a semaphore.

    This class allows only a limited number of processes to acquire connections at the same time,
    using a multiprocessing.Semaphore for synchronization.
    """
    def __init__(self, max_connections: int):
        """
        Initializes the connection pool with a specified number of connections.

        Args:
            max_connections (int): Maximum number of simultaneous connections allowed.
        """
        self.semaphore = Semaphore(max_connections)
        self.connections = Manager().list(range(max_connections))
        
    def get_connection(self):
        """
        Acquires a connection from the pool.

        This method blocks if the maximum number of concurrent connections is reached,
        and waits for a connection to become available.

        Returns:
            int or None: A simulated connection identifier (e.g., an index from the pool),
                         or None if no connection is available.
        """
        print(f"[{current_process().name}] Waiting for a connection...")
        self.semaphore.acquire()
        connection = self.connections.pop() if self.connections else None
        print(f"[{current_process().name}] Acquired connection {connection}")
        return connection

    def release_connection(self, connection):
        """
        Releases a previously acquired connection back to the pool.

        Args:
            connection (int): The connection identifier to return to the pool.
        """
        self.connections.append(connection)
        print(f"[{current_process().name}] Released connection {connection}")
        self.semaphore.release()


def access_database(pool: ConnectionPool):
    """
    Simulates a process accessing a database using a connection from the pool.

    The function acquires a connection, simulates some work using sleep,
    and then releases the connection.

    Args:
        pool (ConnectionPool): The connection pool to acquire and release connections from.
    """
    connection = pool.get_connection()
    try:
        work_time = uniform(1, 3)
        print(f"[{current_process().name}] Working for {work_time:.2f} seconds...")
        sleep(work_time)
    finally:
        pool.release_connection(connection)
        
def run_database(max_connections=3, num_processes=10):

    pool = ConnectionPool(max_connections=max_connections)

    processes = []
    for i in range(num_processes):
        p = Process(target=access_database, args=(pool,), name=f"Process-{i+1}")
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print("All processes have finished.")