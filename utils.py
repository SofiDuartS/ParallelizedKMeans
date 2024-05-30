import numpy as np
import matplotlib.pyplot as plt

import random as rd

def example_func(scatterData, broadcastData, data):
    print(f"Received scattered data: {scatterData}")
    print(f"Received broadcasted data: {broadcastData}")
    return data ** 2

# Inititalize centroids assignation using kmeans++
def initCentroids(X,K):
    #Randomly initialize the centroids
    i=rd.randint(0,X.shape[0])
    Centroid_temp=np.array([X[i]])
    for k in range(1,K):
        D=np.array([]) 
        for x in X:
            D=np.append(D,np.min(np.sum((x-Centroid_temp)**2)))
        prob=D/np.sum(D)
        cummulative_prob=np.cumsum(prob)
        r=rd.random()
        i=0
        for j,p in enumerate(cummulative_prob):
            if r<p:
                i=j
                break
        Centroid_temp=np.append(Centroid_temp,[X[i]],axis=0)
    Centroids = Centroid_temp.T
    return Centroids

# Assign the points to the corresponding cluster
def assignClusters(X, Centroids, K):
    #Compute euclidian distances and assign clusters
    EuclidianDistance=np.array([]).reshape(X.shape[0], 0)
    for k in range(K):
        tempDist = np.sum((X - Centroids[:,k])**2,axis=1)
        EuclidianDistance = np.c_[EuclidianDistance,tempDist]
    cluster_assignation = np.argmin(EuclidianDistance, axis=1)+1
    return cluster_assignation

# Adjust the centroids based on the cluster assignation
def updateCentroids(X, Centroids, K, cluster_assignation):
    output={}
    for k in range(K):
        output[k+1]=np.array([]).reshape(2,0)

    for i in range(X.shape[0]):
        output[cluster_assignation[i]]=np.c_[output[cluster_assignation[i]], X[i]]

    for k in range(K):
        output[k+1]=output[k+1].T

    for k in range(K):
        Centroids[:,k] = np.mean(output[k+1],axis=0)
    
    return output, Centroids

def plot_output(Output, Centroids, K):
    color = ['red','blue','green','cyan','magenta']
    color = color[:K]
    labels = [f"cluster{i}" for i in range(1, K+1)]
    
    for k in range(K):
        plt.scatter(Output[k+1][:,0],Output[k+1][:,1],c=color[k],label=labels[k])
        
    plt.scatter(Centroids[:,0],Centroids[:,1],s=300,c='yellow',label='Centroids')
    plt.title('Clusters of customers')
    plt.xlabel('Annual Income (k$)')
    plt.ylabel('Spending Score (1-100)')
    plt.legend()
    plt.show()