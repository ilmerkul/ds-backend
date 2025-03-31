import requests


def download_image(img_id: int, save_path="") -> bool:
    url = f"http://89.169.157.72:8080/images/{img_id}"

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        if not save_path:
            save_path = f"/image_{img_id}.jpg"

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        return True

    except requests.exceptions.RequestException as e:
        return False
