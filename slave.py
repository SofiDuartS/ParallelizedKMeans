import socket
import pickle

class Slave:
    def __init__(self, masterHost, masterPort):
        # For connection with master
        self.masterHost = masterHost
        self.masterPort = masterPort
        self.socket = None

    def receiveTask(self):
        try:
            data = self.socket.recv(1024)
            if not data:
                return None, None, None, None
            scatteredData, broadcastedData, task, kwargs = pickle.loads(data)
            return scatteredData, broadcastedData, task, kwargs
        except EOFError:
            return None, None, None, None
        except Exception as e:
            print(f"Error receiving task: {e}")
            return None, None, None, None

        #scatteredData, broadcastedData, task, kwargs = pickle.loads(self.socket.recv(1024))
        #return scatteredData, broadcastedData, task, kwargs

    def executeTask(self, scatteredData, broadcastedData, task, kwargs):
        if task is not None:
            result = task(scatteredData, broadcastedData, **kwargs)
            return result
        else:
            return None

    def sendResults(self, result):
        self.socket.send(pickle.dumps(result))

    def initialize(self):
        # Initialize connection with master
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.masterHost, self.masterPort))

    def run(self):
        while True:
            scatteredData, broadcastedData, task, kwargs = self.receiveTask()
            if task is None and scatteredData is None and broadcastedData is None:
                break
            result = self.executeTask(scatteredData, broadcastedData, task, kwargs)
            self.sendResults(result)

        self.socket.close()