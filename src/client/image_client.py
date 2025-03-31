import requests
from typing import Tuple


class ImageClient:
    def __init__(self, host: str, connect_timeout: float = 3.0,
                 read_timeout: float = 10.0):
        self.host = host
        self.timeout = (connect_timeout, read_timeout)

    def download_image(self, img_id: int, save_path: str = "") -> Tuple[
        str, bool]:
        url = f"{self.host}/{img_id}"

        try:
            response = requests.get(url,
                                    stream=True,
                                    timeout=self.timeout)
            response.raise_for_status()

            if not save_path:
                save_path = f"/image_{img_id}.jpg"

            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            return '', True

        except requests.exceptions.RequestException as e:
            return 'Request error', False
        except requests.exceptions.Timeout:
            return 'Timeout error while downloading image', False
        except requests.exceptions.HTTPError as e:
            return f'HTTP error for image {img_id}: {e.response.status_code}', False
        except requests.exceptions.RequestException as e:
            return f'Request failed for image {img_id}: {str(e)}', False
        except IOError as e:
            return f'File write error for image {img_id}: {str(e)}', False
