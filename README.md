Clustering Algorithms
This repository contains custom implementations of the K-Means and DBSCAN clustering algorithms in Python using NumPy and scikit-learn.

Introduction
Clustering is an unsupervised learning technique used to group similar data points together based on certain features. K-Means and DBSCAN are two popular clustering algorithms used for this purpose.

Features
CustomKMeans
Implementation of the K-Means clustering algorithm.
Allows users to specify the number of clusters (n_clusters), maximum number of iterations (max_iter), and random state for reproducibility (random_state).
Provides methods for fitting the model to data (fit) and predicting cluster labels (fit_predict).
CustomDBSCAN
Implementation of the DBSCAN clustering algorithm.
Users can specify the epsilon (eps) parameter, which defines the radius for neighboring points, and the minimum number of points in a neighborhood (min_samples).
Supports fitting the model to data (fit) and predicting cluster labels (fit_predict).
Usage
Clone the repository:
bash

git clone https://github.com/your-username/clustering-algorithms.git
cd clustering-algorithms
Import the desired clustering algorithm:

from clustering_algorithms import CustomKMeans, CustomDBSCAN
Create an instance of the chosen algorithm:


kmeans = CustomKMeans(n_clusters=3)
dbscan = CustomDBSCAN(eps=0.5, min_samples=5)
Fit the model to your data and predict cluster labels:


kmeans.fit(data)
kmeans_labels = kmeans.labels_

dbscan.fit(data)
dbscan_labels = dbscan.labels_
