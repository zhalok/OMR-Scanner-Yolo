import zipfile
import os


def zip_file(folder_path, zip_file_name):
    with zipfile.ZipFile(zip_file_name, "w") as zipf:
        for foldername, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)

                zipf.write(file_path, os.path.relpath(file_path, folder_path))
