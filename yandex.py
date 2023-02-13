import requests

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

    def _get_upload_link(self, file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {"path": file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload(self, file_path, filename):
        href = self._get_upload_link(file_path=file_path).get("href")
        requests.put(href, data=open(filename, 'rb'))
        