import cv2
from util.determine_set import determine_set


def detect_set(prediction, image_path):
    image = cv2.imread(image_path)
    boxes = prediction.boxes
    names = prediction.names

    # print(boxes)
    # print(names)
    boxes = [box for box in boxes if names[int(box.cls.item())] in ["testID layout"]]
    # print("boxes",boxes[0].xywh[0].tolist())
    # return
    x1, y1, x2, y2 = boxes[0].xyxy[0].tolist()
    # x1 = 539
    # x2 = 616
    # y1 = 148
    # y2 = 588
    cropped = image[int(y1) : int(y2), int(x1) : int(x2)]

    # cv2_imshow(cropped)
    # return
    # print(cropped)
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    # cv2_imshow(cropped)
    th, threshed = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)
    cnts = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
    # cv2_imshow(threshed)
    # return
    # print(cnts)

    cnt_list = []
    # print(cnts)
    for i in cnts:
        M = cv2.moments(i)
        (x, y, w, h) = cv2.boundingRect(i)
        print(w, h)
        ar = w / float(h)
        if w >= 35 and w <= 60 and h >= 35 and h <= 60:
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                if cy >= 106 and cy <= 520:
                    # print(w, h)
                    cnt_list.append([cx, cy])

    # cv2.drawContours(cropped, cnts, -1, (0, 255, 0), 2)
    # print(len(cnt_list))
    # cv2_imshow(threshed)
    # return
    # print(cnt_list)

    for idx, cnt in enumerate(cnt_list):
        cv2.circle(cropped, (cnt[0], cnt[1]), 10, (255, 0, 0), -1)  # cv2.drawContou

    # cv2_imshow(cropped)
    if len(cnt_list) == 0:
        return "Not found"

    _, y = cnt_list[0]
    setCode = chr(determine_set(y) + ord("A"))

    # print("setCode", setCode)
    return setCode
