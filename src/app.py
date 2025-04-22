import io
import logging
from typing import Tuple

from flask import Flask, request

from client import ImageClient
from models import PlateReader

IMAGES_PATH = './images'
IMAGE_HOST = 'http://89.169.157.72:8080/images'

app = Flask(__name__)
model = PlateReader.load_from_file('./model_weights/plate_reader_model.pth')
image_client = ImageClient(IMAGE_HOST)


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
    mes, b = image_client.download_image(id, image_path)
    if not b:
        return mes, 500

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
        image_path = f"{IMAGES_PATH}/{id}.jpg"

        print(id)
        mes, b = image_client.download_image(id, image_path)
        if not b:
            return mes, 500

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
