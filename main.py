import logging
import json
import vkontakte
import requests
from vkontakte import VK
from yandex import YaUploader
import os
from threading import Thread
from tqdm import tqdm
from time import sleep

logging.basicConfig(level = logging.INFO, filename="py_log.log", filemode='w', format="%(asctime)s %(levelname)s %(message)s")

def progress_bar(dir, counter, photo_list):
    for i in tqdm(range(100), f'Загрузка {dir} фотографии {counter} из {len(photo_list)}'):
            sleep(.01)

if __name__ == "__main__":
    owner_id = str(input('Введите id пользователя Вконтакте: '))
    access_token = 'vk1.a.k3IQ34zE8adqiCzEhDFy_-HyYa3nu5yZIeyK-QgEc1wT8V2oT609MO8TK4-E3BkZAEZ98kfR704kwmpPRbz2HbVXBgKTj6o8Njmm9yhE_9ZxNx5tkVYVRVLK-e3N4kZ1djy0L15KFzPkyXrHT-jIoPwFmEo6Nc6lABnZ4uqF7PhQBpCPzlaunEoNAr1c-oInEIgJ_380LJodK2U5VZ3a_A'
    vk = VK(access_token)
    vk.profile_photo(owner_id)
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
    token_ya = str(input('Введите токен пользователя платформы Яндекс.Диск: '))
    ya = YaUploader(token_ya)
    ya.create_folder()
    logging.info('Папка для фотографий "vk_photos" создана')
    like_list = []
    data = []
    counter = 0
    for photo in photo_list:
        counter += 1
        img_response = requests.get(photo[0])
        with open(f'{photo[1]} {photo[2]}.jpg', 'wb') as file:
            file.write(img_response.content)
        logging.info(f'Фотография №{counter} загружена в память приложения')
        if photo[1] in like_list:
            file_path = f'vk_photos/{str(photo[1])} {str(photo[2])}.jpg'
        else:
            file_path = f'vk_photos/{str(photo[1])}.jpg'
        like_list.append(photo[1])
        filename = f'{photo[1]} {photo[2]}.jpg'
        Thread(target=ya.upload(file_path, filename)).start()
        Thread(target=progress_bar('на Яндекс.Диск', counter, photo_list)).start()
        logging.info(f'Фотография №{counter} загружена на Яндекс.Диск')
        img = {}
        img.setdefault("file_name",file_path[10:])
        img.setdefault("size", photo[3])
        data.append(img)
        os.remove(f'{photo[1]} {photo[2]}.jpg')
        logging.info(f'Фотография №{counter} удалена из памяти приложения')
    with open('data.txt', 'w') as file:
        file.write(json.dumps(data, sort_keys=True, indent=2))
        logging.info(f'Информация о загруженных фотографиях отражена в файле data.txt')        
    logging.info("Загрузка фотографий на Яндекс.Диск завершена")
    
   