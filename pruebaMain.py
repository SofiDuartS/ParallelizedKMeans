import sys
import time
from master import Master
from slave import Slave

if __name__ == "__main__":
    role = sys.argv[1]
    host = 'localhost'
    port = 12345

    def example_func(scatterData, broadcastData, data):
        print(f"Received scattered data: {scatterData}")
        print(f"Received broadcasted data: {broadcastData}")
        return data ** 2

    if role == "master":
        num_slaves = 2
        data_to_scatter = [i for i in range(100)]
        data_to_broadcast = {"message": "Broadcast data"}
        master = Master(host, port, num_slaves)
        master.initialize()
        results = master.runSlaves(data_to_scatter, data_to_broadcast, example_func, data=5)
        print(f"Resultados: {results}")

    elif role == "slave":
        time.sleep(1)  # Esperar un momento para asegurarse de que el master está listo
        slave = Slave(host, port)
        slave.initialize()
        slave.run()