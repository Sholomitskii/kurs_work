import requests

class VK:

   def __init__(self, access_token, version= '5.131'):
       self.token = access_token
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

   def profile_photo(self, owner_ids, number_photo):
       url = 'https://api.vk.com/method/photos.get'
       params = {'owner_id': owner_ids,'album_id':'profile','offset': 0, 'count':number_photo, 'extended':1 }
       params = {**self.params, **params}
       global result
       result = requests.get(url, params)
    
   def know_id(self, screen_name):
       url = 'https://api.vk.com/method/utils.resolveScreenName'
       params = {'screen_name':screen_name}
       params = {**self.params, **params}
       result = requests.get(url, params)
       global owner_id
       owner_id = result.json()['response']['object_id']
       return owner_id
       
