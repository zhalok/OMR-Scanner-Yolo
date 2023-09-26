from ultralytics import YOLO
from util.grayscale_conversion import grayscale_conversion
import cv2


def predict(model_path, image_path):
    model = YOLO(model_path)
    image = cv2.imread(image_path)
    gray_image = grayscale_conversion(image)
    predictions = model.predict(save=True, show_labels=False, source=gray_image)
    # print(predictions)
    return predictions[0]
