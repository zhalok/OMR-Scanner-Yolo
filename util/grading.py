import numpy as np
from sklearn.cluster import DBSCAN
from util.clustering import clustering
from util.column_detection import column_detection


def grading(predictions):
    boxes = predictions.boxes
    # print("number of bounding boxes",boxes[0])
    names = predictions.names
    boxes = [
        box
        for box in boxes
        if names[int(box.cls.item())] in ["a", "b", "c", "d", "not answered", "invalid"]
    ]
    # boxes = (filter(boxes,filter_key))
    # print(names)
    confs = predictions.boxes.conf.tolist()
    centers = []

    for idx, box in enumerate(boxes):
        # if names[int(box.cls.item())] in ["a","b","c","d","not answered","invalid"]:
        xywh = box.xywh
        # cls = int(box.cls.tolist()[0])
        center = box.xywh[0][0:2]
        center = center.cpu().numpy().tolist()
        center = [round(cent) for cent in center]

        centers.append(center)

    centers = np.array(centers)

    clusters = clustering(centers, boxes, names, confs)
    columns = column_detection(clusters, boxes, names)

    # print("column len",len(columns))
    # print("column values",len(columns[0]))
    # print("column",columns[0])
    # for c in columns:
    #   print(len(c))
    for i in range(len(columns)):
        columns[i] = sorted(columns[i], key=lambda x: x[0][1])

    columns = sorted(columns, key=lambda x: x[0][0][0])
    # print(columns[0][0][0][0])

    answers = []
    for column in columns:
        # print(column)
        answers += column

    # for i in range(len(answers)):
    #   answers[i] = sorted(answers[i],key=lambda x:x[0][0])

    answers = [
        {"question": idx + 1, "answer": c[1], "center": c[0]}
        for idx, c in enumerate(answers)
    ]

    # answers

    return answers
