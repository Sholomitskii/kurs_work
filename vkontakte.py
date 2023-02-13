import requests

class VK:

   def __init__(self, access_token, version= '5.131'):
       self.token = access_token
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

   def profile_photo(self, owner_id):
       url = 'https://api.vk.com/method/photos.get'
       params = {'owner_id': owner_id,'album_id':'profile','offset': 0, 'count':5, 'extended':1 }
       params = {**self.params, **params}
       global result
       result = requests.get(url, params)