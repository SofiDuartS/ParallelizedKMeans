import socket
import pickle
import numpy as np

class Master:
    def __init__(self, host, port, numSlaves):
        self.host = host
        self.port = port
        self.numSlaves = numSlaves
        self.slaves = []
        self.slavesData = []
        self.results = []

    def connections(self):
        masterSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        masterSocket.bind((self.host, self.port))
        masterSocket.listen(self.numSlaves)

        for _ in range(self.numSlaves):
            slaveSocket, addr = masterSocket.accept()
            self.slaves.append(slaveSocket)
            print(f"New slave connected from {addr}")

    def scatter(self, data):
        size = len(data) // self.numSlaves
        for i in range(self.numSlaves):
            start = i * size
            end = len(data) if i == self.numSlaves - 1 else start + size
            slaveData = data[start:end]
            self.slavesData.append(slaveData)

    def sendTaskToSlave(self, slave, scatteredData, broadcastedData, task, kwargs):
        try:
            completeTask = (scatteredData, broadcastedData, task, kwargs)
            slave.sendall(pickle.dumps(completeTask))
        except Exception as e:
            print(f"Error sending task to slave: {e}")

    def receiveResults(self):
        self.results = []
        for slave in self.slaves:
            try:
                result = pickle.loads(slave.recv(524288000))
                if result is not None:
                    self.results.append(result)
            except Exception as e:
                print(f"Error receiving result from slave: {e}")
        
        self.results = [item.item() for sublist in self.results for item in sublist]

    def initialize(self):
        self.connections()

    def runSlaves(self, scatterData, broadcastData, task, kwargs):
        self.scatter(scatterData)
        for i in range(len(self.slaves)):
            self.sendTaskToSlave(self.slaves[i], self.slavesData[i], broadcastData, task, kwargs)

        # for slave in self.slaves:
        #     try:
        #         slave.sendall(pickle.dumps((None, None, None, None)))
        #     except Exception as e:
        #         print(f"Error sending termination signal to slave: {e}")

        self.receiveResults()
        print("Recibiendo resultados de esclavo")
        return self.results

    def close_connections(self):
        for slave in self.slaves:
            try:
                slave.close()
            except Exception as e:
                print(f"Error closing connection to slave: {e}")
        print("All slave connections closed.")
