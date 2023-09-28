from predict import predict
from reg_detection import detect_reg
from set_detection import detect_set
from util.grading import grading
import os
import cv2
import json

# uploaded = files.upload()

# image_path = list(uploaded.keys())[0]
image_path = "images/test.jpg"
model_path = "models/model.pt"

image = cv2.imread(image_path)
predictions = predict(model_path=model_path, image=image)

reg = detect_reg(predictions, image_path)

# print(reg)

setCode = detect_set(predictions, image_path)
# print("setCode",setCode)

# print("registration",reg)

# os.remove(image_path)

answers = grading(predictions)
# print(answers)


# print(answers)

answers = [{"question_no": ans["question"], "answer": ans["answer"]} for ans in answers]
results = {"registartion": reg, "setCode": setCode, "answers": answers}


with open("results.json", "w") as json_file:
    json.dump(results, json_file, indent=4)
    print("Answers saved successfully")
