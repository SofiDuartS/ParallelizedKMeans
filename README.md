# ParallelizedKMeans

One of the fundamental techniques to efficiently analyze and extract insights from large datasets
in data analysis is clustering, which involves grouping similar data points together. K-means clus-
tering is a widely used algorithm for this purpose, but its traditional implementation may struggle
with the computational demands of large datasets.

To address this challenge, we aim to use parallelized version of the K-means clustering algorithm
using MPI communication in python. By using this technique, we seek to distribute the compu-
tational workload across multiple processes, thereby accelerating the clustering process and enabling
scalability to larger datasets.

With this project we intend to, through efficient communication and synchronization between
master and slave processes, ensure the accuracy and convergence of the clustering results. Further-
more, we intend to evaluate the performance of our parallelized implementation by measuring speedup
metrics based on the number of MPI processes used.
