import socket
import pickle #to convert data to bytes

# Clase Master
class Master:
    def __init__(self, host, port, numSlaves):
        # For port config
        self.host = host
        self.port = port

        # For slave management
        self.numSlaves = numSlaves
        self.slaves = []
        self.slavesData = [] # data to be sent to slaves
        self.results = [] # results from slaves

    def connections(self):
        # Connection configuration for master and slaves

        # Master socket config
        masterSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        masterSocket.bind((self.host, self.port))
        masterSocket.listen(self.numSlaves)

        # Accept connections from slaves
        for _ in range(self.numSlaves):
            slaveSocket, addr = masterSocket.accept()
            self.slaves.append(slaveSocket)
            print(f"New slave connected from {addr}")

    def scatter(self, data):
        # Splits data into pieces and adds them to slavesData

        size = len(data) // self.numSlaves
        for i in range(self.numSlaves):
            start = i * size
            if i == self.numSlaves - 1:
                # The last slave will receive all the remaining data
                end = len(data)
            else:
                end = start + size
            slaveData = data[start:end]
            self.slavesData.append(slaveData)

    def sendTaskToSlave(self, slave, scatteredData, broadcastedData, task, kwargs):
        # task is a function that has to be executed by the slave
        # kwargs are the arguments of task
        # scatteredData is the portion of data scattered to the slave
        # broadcastedData is the data that has to be sent to all slaves

        completeTask = (scatteredData, broadcastedData, task, kwargs)
        slave.send(pickle.dumps(completeTask))
        

    def receiveResults(self):
        # Receives the results from the slaves

        for slave in self.slaves:
            result = pickle.loads(slave.recv(1024))
            if result is not None:
                self.results.append(result)

    def initialize(self):
        # Initializes the master connection
        self.connections()

    def runSlaves(self, scatterData, broadcastData, task, **kwargs):
        # scatterData is the data that has to be splitted and sent to the slaves
        # broadcastData is the data that has to be sent to all slaves
        self.scatter(scatterData)
        for i in range(len(self.slaves)):    
            self.sendTaskToSlave(self.slaves[i], self.slavesData[i], broadcastData, task, kwargs)

        for slave in self.slaves:
            slave.sendall(pickle.dumps((None, None, None, None)))
            
        self.receiveResults()
        return self.results