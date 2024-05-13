import socket
import select

class Slave:
    def __init__(self, MASTERIP, MASTERPORT):
        # Socket setup
        self.HEADER_LENGTH = 10
        self.MASTERIP = MASTERIP
        self.MASTERPORT = MASTERPORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
        self.socket.connect((self.IP, self.PORT))
        self.socket.setblocking(False)

        # K-means parameters
        self.centroids = []
        self.data = []
        self.centroid_assignments = {}

    def receiveData(self):
        # Receive data from master
        pass

    def receiveCentroids(self):
        # Receive centroids from master
        pass
    
    def assignCentroids(self):
        # Assign data points to the closest centroid

        # Send assignments to master
        pass

    def sendCentroidAssignments(self):
        # Send centroid assignments to master
        pass