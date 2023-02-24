import requests
import logging

logging.basicConfig(level = logging.INFO, filename="py_log.log", filemode='w', format="%(asctime)s %(levelname)s %(message)s")

class YaUploader:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        
    def create_folder(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {"path": "vk_photos"}
        requests.put(url, headers=headers, params=params)
        logging.info('Папка для фотографий "vk_photos" создана')

    def upload(self, file_path, url):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path':file_path, 'url':url, 'disable_redirects':True}
        requests.post(upload_url, headers=headers, params=params)
        
        