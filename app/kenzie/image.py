# Desenvolva sua lógica de manipulação das imagens aqui

from ntpath import join
import os
from flask import safe_join
from datetime import datetime
from werkzeug.utils import secure_filename

FILES_DIRECTORY = os.getenv('FILES_DIRECTORY')  


def make_extension_dir(filename: str):
    extension = get_file_extension(filename)
    path = os.path.join(FILES_DIRECTORY, extension)
    try:
        os.mkdir(path)
    except FileExistsError:
        return


def get_file_path(file):
    filename = file.filename
    extension = get_file_extension(filename)

    joined_paths = os.path.join(FILES_DIRECTORY, extension)
    make_extension_dir(filename)
    abs_path = os.path.abspath(joined_paths)
    filepath = safe_join(abs_path, filename)

    return filepath


def upload_file(file):
    filepath = get_file_path(file)
    file.save(filepath)
    
def get_file_extension(file):
    return file.split(".")[-1]
