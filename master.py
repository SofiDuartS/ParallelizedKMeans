import socket
import select

class Master:
    def __init__(self, IP, PORT, k, max_iter, dataset):
        # Socket setup
        self.HEADER_LENGTH = 10
        self.IP = IP
        self.PORT = PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #To reuse the same port
        self.socket.bind((self.IP, self.PORT))
        self.socket.listen()

        # K-means parameters
        self.k = k
        self.max_iter = max_iter
        self.dataset = dataset
        self.centroids = []
        self.clusters = {}

        # Slaves data
        self.slaves = [self.socket]
        self.centroidsAssignments = {}


    def splitData(self):
        # Split data equally for all slaves

        # Send data to slaves
        pass

    def sendData(self, slave_socket, data):
        # Send data to a slave
        pass

    def initCentroids(self):
        # Initialize centroids randomly
        pass

    def broadcastCentroids(self):
        # Broadcast centroids to all slaves
        pass

    def receiveCentroidAssigments(self, slave_socket):
        # Receive centroids from a slave
        pass
    
    def updateCentroids(self):
        # Receive centroid assignments from all slaves

        # Update centroids based on assignments from slaves
        pass

    def run(self):
        # Split data among slaves

        # Initialize centroids

        # Send centroids to all slaves

        # Update centroids
        pass

    