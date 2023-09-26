from sklearn.cluster import DBSCAN


def clustering(centers, boxes, names, confs):
    X = centers
    eps = 1
    min_samples = 1
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    dbscan.fit(X)

    labels = dbscan.labels_
    core_samples = dbscan.core_sample_indices_

    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

    clusters = [0] * n_clusters

    for idx, c in enumerate(centers):
        cls = int(boxes[idx].cls.tolist()[0])
        nm = names[cls]
        cnf = confs[idx]
        # print(type(cnf))
        if clusters[labels[idx]] == 0:
            clusters[labels[idx]] = [c, nm, cnf]
        elif clusters[labels[idx]][2] < cnf:
            clusters[labels[idx]] = [c, nm, cnf]

    return clusters
