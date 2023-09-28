from util.determine_digit import determine_digit
import cv2


def detect_reg(prediction, image):
    boxes = prediction.boxes
    names = prediction.names

    # print(boxes)
    # print(names)
    boxes = [box for box in boxes if names[int(box.cls.item())] in ["reg layout"]]
    # print("boxes",boxes[0].xywh[0].tolist())
    # return
    x1, y1, x2, y2 = boxes[0].xyxy[0].tolist()
    # print(x,y,width,height)
    # image = cv2.imread(image_path)
    reg_roi = image[int(y1) : int(y2), int(x1) : int(x2)]
    gray = cv2.cvtColor(reg_roi, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)
    cnts = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]

    cnt_list = []
    # print(cnts)
    for i in cnts:
        M = cv2.moments(i)
        (x, y, w, h) = cv2.boundingRect(i)
        ar = w / float(h)
        if w >= 35 and w <= 55 and h >= 35 and h <= 55:
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                if cy >= 106 and cy <= 787:
                    # print(w, h)
                    cnt_list.append([cx, cy])

    # cv2.drawContours(reg_roi, cnts, -1, (255, 255, 0), 3)

    # print(len(cnt_list))
    cnt_list = sorted(cnt_list)

    # dbscan = DBSCAN(eps=1, min_samples=1)
    # dbscan.fit((np.array(cnt_list)[:, 1]).reshape(-1, 1))
    # labels = dbscan.labels_

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (0, 0, 255)  # BGR color format (Blue, Green, Red)
    thickness = 2
    reg = ""

    for idx, cnt in enumerate(cnt_list):
        # print(cnt)
        cv2.circle(reg_roi, (cnt[0], cnt[1]), 10, (255, 0, 0), -1)  # cv2.drawContou
        digit = determine_digit(cnt[1])
        cv2.putText(
            reg_roi,
            str(digit),
            (cnt[0], cnt[1]),
            font,
            font_scale,
            font_color,
            thickness,
            cv2.LINE_AA,
        )

        reg += str(digit)
    # Crop the bounding box region
    # cropped_image = image[y1:y2, x1:x2]
    # cv2.circle(reg_roi, (int(x1), int(y1)), 1, (255,0,0), -1)
    # print(cropped_image)
    # cv2_imshow(reg_roi)
    return reg
    # cv2.imwrite("cropped.jpg",cropped_image)
