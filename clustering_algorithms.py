# -*- coding: utf-8 -*-
"""clustering_algorithms.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1a6qBlSPI8qDQUbwVtG-MoH03R81Rf88R
"""

import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.utils import check_array


class CustomKMeans:
    def __init__(self, n_clusters=8, max_iter=300, random_state=None):
        # Initialize KMeans with specified parameters
        self.n_clusters = n_clusters  # Number of clusters
        self.max_iter = max_iter  # Maximum number of iterations
        self.random_state = random_state  # Random state for reproducibility
        self.cluster_centers_ = None  # Cluster centers
        self.labels_ = None  # Cluster labels for training data points

    def _calc_distances(self, X, centers):
        # Calculate Euclidean distances between points and cluster centers
        return euclidean_distances(X, centers)

    def fit(self, X: np.ndarray, y=None):
        # Convert input data to numpy array
        X = check_array(X, accept_sparse='csr')
        np.random.seed(self.random_state)  # Set random seed for reproducibility

        # Initialize cluster centers randomly
        random_indices = np.random.choice(X.shape[0], size=self.n_clusters, replace=False)
        self.cluster_centers_ = X[random_indices]

        for _ in range(self.max_iter):
            # Assign labels based on closest centroid
            distances = self._calc_distances(X, self.cluster_centers_)
            self.labels_ = np.argmin(distances, axis=1)

            # Update centroids by computing mean of points assigned to each cluster
            new_centers = np.array([X[self.labels_ == k].mean(axis=0) for k in range(self.n_clusters)])

            # Check for convergence by comparing new and old centroids
            if np.allclose(self.cluster_centers_, new_centers):
                break

            self.cluster_centers_ = new_centers  # Update centroids

        return self  # Return fitted KMeans model

    def fit_predict(self, X: np.ndarray, y=None) -> np.ndarray:
        # Fit the model and return predicted cluster labels
        return self.fit(X).labels_


class CustomDBSCAN:
    def __init__(self, eps=0.5, min_samples=5):
        # Initialize DBSCAN with specified parameters
        self.eps = eps  # Epsilon: radius for neighborhood points
        self.min_samples = min_samples  # Minimum number of points in a neighborhood
        self.labels_ = None  # Cluster labels for training data points

    def _grow_cluster(self, X, neighbors, cluster_label, current_cluster):
        # Expand the cluster by adding neighboring points
        for neighbor_idx in neighbors:
            if self.labels_[neighbor_idx] == -1:
                self.labels_[neighbor_idx] = cluster_label
            elif self.labels_[neighbor_idx] == 0:
                self.labels_[neighbor_idx] = cluster_label
                new_neighbors = self._query_region(X[neighbor_idx], X)
                if len(new_neighbors) >= self.min_samples:
                    neighbors = np.union1d(neighbors, new_neighbors)

            if current_cluster is not None and current_cluster != cluster_label:
                self.labels_[neighbor_idx] = cluster_label

    def _query_region(self, point, X):
        # Find neighbors of a point within epsilon distance
        distances = euclidean_distances([point], X)[0]
        return np.where(distances <= self.eps)[0]

    def fit(self, X: np.ndarray, y=None):
        # Convert input data to numpy array
        X = check_array(X, accept_sparse='csr')
        self.labels_ = np.zeros(X.shape[0])  # Initialize labels for each point

        cluster_label = 0
        for idx, point in enumerate(X):
            if self.labels_[idx] != 0:
                continue

            neighbors = self._query_region(point, X)  # Find neighbors of the current point
            if len(neighbors) < self.min_samples:
                self.labels_[idx] = -1  # Mark point as noise (-1)
            else:
                cluster_label += 1
                self.labels_[idx] = cluster_label
                self._grow_cluster(X, neighbors, cluster_label, None)  # Expand the cluster

        return self  # Return fitted DBSCAN model

    def fit_predict(self, X: np.ndarray, y=None) -> np.ndarray:
        # Fit the model and return predicted cluster labels
        return self.fit(X).labels_