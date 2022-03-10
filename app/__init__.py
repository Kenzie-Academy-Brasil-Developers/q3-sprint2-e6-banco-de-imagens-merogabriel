# Desenvolva suas rotas aqui

from http import HTTPStatus
from http.client import NOT_FOUND
from flask import Flask, request, safe_join, send_file
import os

from app.kenzie.image import FILES_DIRECTORY, get_file_extension, upload_file, get_file_path

MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH')) 
ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS').split(':')
FILES_DIRECTORY = os.getenv('FILES_DIRECTORY')


app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


@app.get('/download/<file_name>')
def download(file_name):
	extension = get_file_extension(file_name)

	if extension not in ALLOWED_EXTENSIONS:
		return {'error': f'{extension} not supported'}, HTTPStatus.NOT_FOUND

	for dir in os.listdir(FILES_DIRECTORY):
		for file in os.listdir(f'{FILES_DIRECTORY}/{dir}'):
			if file == file_name:
				abs_path = os.path.abspath(FILES_DIRECTORY)
				filepath = safe_join(abs_path, extension, file_name)
				return send_file(filepath, as_attachment=True), HTTPStatus.OK

	return {'error': f'{file_name} not found'}, HTTPStatus.NOT_FOUND


@app.get('/download-zip')
def download_dir_as_zip():
	# file_extension = request.args.get('file_extension')
	# compression_ratio = int(request.args.get('compression_ratio'))

	# for dir in os.listdir(f'{FILES_DIRECTORY}'):
	# 	if dir == file_extension:
	# 		print(os.listdir(f'{FILES_DIRECTORY}/{dir}'))

	return {'msg': 'ola'}


@app.get('/files')
def list_files():
	file_list = []

	for dir in os.listdir('app/files'):
		for file in os.listdir(f'app/files/{dir}'):
			file_list.append(file)

	return {'files': file_list},HTTPStatus.OK


@app.get('/files/<extension>')
def list_files_by_extension(extension):
	file_list = []
	
	if extension not in ALLOWED_EXTENSIONS:
		return {'error': f'{extension} is not supported'}, HTTPStatus.NOT_FOUND

	for dir in os.listdir('app/files'):
		if dir == extension:
			for file in os.listdir(f'app/files/{dir}'):
				file_list.append(file)

	return {'files': file_list}, HTTPStatus.OK


@app.post('/upload')
def upload():
	files = request.files

	for file in files.values():
		filename = file.filename
		extension = get_file_extension(filename)

		if extension in os.listdir(f'{FILES_DIRECTORY}'):
			if filename not in os.listdir(f'{FILES_DIRECTORY}/{extension}'):
				upload_file(file)
				return {'msg': 'file uploaded'}, HTTPStatus.CREATED
		elif extension not in os.listdir(f'{FILES_DIRECTORY}'):
			upload_file(file)
			return {'msg': 'file(s) uploaded'}, HTTPStatus.CREATED

	return {'error': 'file(s) already exists'}, HTTPStatus.CONFLICT