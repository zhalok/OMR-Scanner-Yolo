from sklearn.cluster import DBSCAN
import numpy as np


def column_detection(clusters, boxes, names):
    X = [cluster[0] for cluster in clusters]

    eps = 10
    min_samples = 1
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    dbscan.fit((np.array(X)[:, 0]).reshape(-1, 1))

    labels = dbscan.labels_
    core_samples = dbscan.core_sample_indices_

    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

    # print("clusters",n_clusters)

    columns = [[] for i in range(n_clusters)]

    for idx, x in enumerate(X):
        columns[labels[idx]].append([x, clusters[idx][1]])

    return columns
