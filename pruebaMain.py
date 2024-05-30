import sys
import time
import pandas as pd
import matplotlib.pyplot as plt

from master import Master
from slave import Slave
from utils import initCentroids, assignClusters, updateCentroids, plot_output


if __name__ == "__main__":
    
    role = sys.argv[1]
    host = 'localhost'
    port = 12345

    if role == "master":

        # Define number of slaves
        num_slaves = 5

        # Define kmeans variables
        kmeans_n_iters = 5
        K = 5 # Number of clusters

        # Data to be scattered
        file_name = "Mall_Customers.csv"
        input_data_path = f"input_data/{file_name}"
        df = pd.read_csv(input_data_path, encoding='UTF-8') #Filter the data if necessary
        df = df.iloc[:, [3, 4]]
        df_values = df.values
        data_to_scatter = df_values

        # Data to be broadcasted 
        data_to_broadcast = initCentroids(df_values, K) # centroids initialization

        # Create a master instance
        master = Master(host, port, num_slaves)

        # Intialize the master connection
        master.initialize()
        print("Connection stablished with slaves.")
        start_time = time.time()
        # ---------------------------------------------
        # --------------Kmeans algorithm---------------
        # ---------------------------------------------
        print("Running Kmeans algorithm in parallel...")
        for n in range(kmeans_n_iters):
           
            # Assign the clusters
            cluster_assignation = master.runSlaves(data_to_scatter, data_to_broadcast, assignClusters, K)
            # Update the centroids
            Output, data_to_broadcast = updateCentroids(df_values, data_to_broadcast, K, cluster_assignation)
            print(data_to_broadcast)
            print(f"Acabo iteracion {n+1}")
            
        Centroids = data_to_broadcast.T # Define the final centroids
        print("Kmeans algorithm finished.")
        end_time = time.time()
        master.close_connections()
        execution_time = end_time-start_time
        print(f"Execution time: {execution_time}")
        plot_output(Output,Centroids,K)
       
    elif role == "slave":
        time.sleep(1)  # Esperar un momento para asegurarse de que el master está listo
        slave = Slave(host, port)
        slave.initialize()
        slave.run()