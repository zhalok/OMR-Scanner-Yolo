from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import base64
from PIL import Image
import io
import cv2
import numpy as np

# from functions.detect import detect
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from fastapi import Request as request
import json

# from util.firebase import upload
import os
import zipfile
import io
import uuid
import shutil
import sys
from util.upload_to_aws import upload_to_aws
from util.zipping import zip_file
from predict import predict
from reg_detection import detect_reg
from set_detection import detect_set
from util.grading import grading

print("version: ", sys.version)

# class Data(BaseModel):
#     name: str
#     total_size: int
#     chunk: File


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")


def save_file(directory, name, file):
    root = os.path.abspath(os.curdir)
    path = os.path.join(root, directory, name)
    open(path, "wb").write(file)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/upload/single")
def uploadtotal(file: Annotated[bytes, File()], name: Annotated[str, Form()]):
    try:
        root = os.path.abspath(os.curdir)
        image_np = np.frombuffer(file, np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        predictions = predict("models/model.pt", image)
        setCode = detect_set(predictions, image)
        reg = detect_reg(predictions, image)
        # return {"predictions": predictions}
        # print(predictions)
        # return {"success": True}
        answers = grading(predictions)
        # print(answers)

        # print(answers)

        answers = [
            {"question_no": ans["question"], "answer": ans["answer"]} for ans in answers
        ]
        results = {"registartion": reg, "setCode": setCode, "answers": answers}
        return results

        os.mkdir(os.path.join("single", str(name)))
        os.mkdir(os.path.join("single", str(name), "answers"))
        os.mkdir(os.path.join("single", str(name), "images"))
        result = detect(image, name, dir=os.path.join("single", str(name)))
        zippath = os.path.join("single", str(name))
        zip_file(folder_path=zippath, zip_file_name=zippath + ".zip")
        upload_to_aws(zippath + ".zip")
        shutil.rmtree(os.path.join("single", str(name)))
        os.remove(zippath + ".zip")
        data = {}

        data["result"] = result

        return data
    except Exception as e:
        print(e)


# @app.post("/api/upload/batch")
# def uploadBatchBuffer(filezip: Annotated[bytes, File()], name: Annotated[str, Form()]):
#     z = zipfile.ZipFile(io.BytesIO(filezip))
#     # print("name", name)
#     os.mkdir(os.path.join("batch", str(name)))
#     os.mkdir(os.path.join("batch", str(name), "answers"))
#     os.mkdir(os.path.join("batch", str(name), "images"))
#     results = []
#     for i in z.infolist():
#         if i.filename[-1] == "/":
#             continue

#         content = z.read(i)
#         image_np = np.frombuffer(content, np.uint8)
#         image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
#         filename = uuid.uuid4()

#         result = detect(image, name=str(filename), dir=os.path.join("batch", str(name)))
#         results.append(result)

#     zippath = os.path.join("batch", str(name))

#     zip_file(folder_path=zippath, zip_file_name=zippath + ".zip")

#     upload_to_aws(zippath + ".zip")
#     shutil.rmtree(os.path.join("batch", str(name)))
#     os.remove(zippath + ".zip")
#     return {"results": results}
