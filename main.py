import logging
import json
import vkontakte
from vkontakte import VK
from yandex import YaUploader
from threading import Thread
from tqdm import tqdm
from time import sleep
import configparser

logging.basicConfig(level = logging.INFO, filename="py_log.log", filemode='w', format="%(asctime)s %(levelname)s %(message)s")

config = configparser.ConfigParser()  
config.read("settings.ini")

def user_requests():
    global owner_ids
    owner_ids = str(input('Введите id или screen_name пользователя Вконтакте: '))
    flag = False
    for i in 'qwertyuiopasdfghjklzxcvbnm':
        if i in owner_ids:
            flag = True
    if flag == True:
        vk.know_id(owner_ids)
        owner_ids = vkontakte.owner_id 
    global number_photo
    number_photo = int(input('Введите количество фотографий для загрузки: '))
    global token_ya
    token_ya = str(input('Введите токен пользователя платформы Яндекс.Диск: '))

def progress_bar(dir, counter, photo_list):
    for i in tqdm(range(100), f'Загрузка {dir} фотографии {counter} из {len(photo_list)}'):
            sleep(.01)

def photo_uploader():
    result = vkontakte.result
    urls, likes, dates, types = [], [], [], []
    for el in result.json()['response']['items']:
        likes.append(el['likes']['count'])
        dates.append(el['date'])
        arr = []
        for elem in el['sizes']:
            arr.append(elem['type'])
        for i in 'wzyrqpoxms':
            if i in arr:
                for elem in el['sizes']:
                    if elem['type'] == i:
                        urls.append(elem['url'])
                        types.append(elem['type'])
                if i in types:
                    break       
    photo_list = list(zip(urls, likes, dates, types))
    like_list = []
    global data
    data = []
    counter = 0
    for photo in photo_list:
        counter += 1
        if photo[1] in like_list:
            file_path = f'vk_photos/{str(photo[1])} {str(photo[2])}.jpg'
        else:
            file_path = f'vk_photos/{str(photo[1])}.jpg'
        like_list.append(photo[1])
        url = photo[0]
        Thread(target=ya.upload(file_path, url)).start()
        Thread(target=progress_bar('на Яндекс.Диск', counter, photo_list)).start()
        logging.info(f'Фотография №{counter} загружена на Яндекс.Диск')
        img = {}
        img.setdefault("file_name",file_path[10:])
        img.setdefault("size", photo[3])
        data.append(img)

def json_creator():
    with open('data.json', 'w') as file:
        file.write(json.dumps(data, sort_keys=True, indent=2))
        logging.info(f'Информация о загруженных фотографиях отражена в файле data.json')        
    logging.info("Загрузка фотографий на Яндекс.Диск завершена")

if __name__ == "__main__":
    access_token = config['VK']['access_token']
    vk = VK(access_token)
    user_requests()
    ya = YaUploader(token_ya)
    vk.profile_photo(owner_ids, number_photo)
    ya.create_folder()
    photo_uploader()
    json_creator()

    
    
   