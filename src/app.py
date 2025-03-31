import io
import logging
from typing import Tuple

from flask import Flask, request

from models import PlateReader
from utils import download_image

IMAGES_PATH = './images'

app = Flask(__name__)
model = PlateReader.load_from_file('./model_weights/plate_reader_model.pth')


def model_read_text(image_path: str) -> Tuple[str, int]:
    try:
        with open(image_path, 'rb') as f:
            text = model.read_text(io.BytesIO(f.read()))
    except:
        return 'model error', 500

    return {'car_numbers': text}, 200


@app.route('/')
def hello():
    return '<h1><center>Hello!</center></h1>'


@app.route('/get_car_numbers')
def get_car_numbers():
    id = request.args.get('id')

    if not id:
        return 'id не передан', 400

    try:
        id = int(id)
    except:
        return 'id должен быть числом', 400

    image_path = IMAGES_PATH + f"/{id}.jpg"
    if not download_image(id, image_path):
        return "ошибка загрузки изображения", 500

    return model_read_text(image_path)


@app.route('/get_few_car_numbers')
def get_few_car_numbers():
    ids = request.args.get('ids')

    if not ids:
        return 'ids не передан', 400

    ids = ids.split(',')

    try:
        ids = list(map(int, ids))
    except:
        return 'ids должны быть числами', 400

    texts = []
    for id in ids:
        image_path = IMAGES_PATH + f"/{id}.jpg"

        if not download_image(id, image_path):
            return "ошибка загрузки изображения", 500

        text, c = model_read_text(image_path)

        if c != 200:
            return text, c

        texts.append(text)

    return {'car_numbers': texts}, 200


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.run(host='0.0.0.0', port=8080, debug=True)
