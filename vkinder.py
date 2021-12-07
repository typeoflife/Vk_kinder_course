import json
import requests
from tokens import vktoken
from botbd import BotBD

BotBD = BotBD('user_ids.db')


class Vksearch:

    def check_account(self, user_id):
        url = "https://api.vk.com/method/users.get"
        params = {
            "user_ids": {user_id},
            "fields": "bdate, sex, city, relation",
            "access_token": vktoken(),
            "v": "5.131",
        }


        response = requests.get(url=url, params=params)
        main_keys = dict()

        if 'error' not in response.json():
            for info in response.json()['response']:
                keys = {'bdate', 'sex', 'city', 'relation'} & info.keys()
                for key in keys:
                    main_keys[key] = info[key]

            if 'bdate' in main_keys:
                if len(main_keys['bdate']) > 5:
                    main_keys['bdate'] = main_keys['bdate'][-4:]
                else:
                    del main_keys['bdate']

            return main_keys
        else:
            return 0


    def find_users(self, user_id, offset=1):
        info_user = self.check_account(user_id)
        if info_user == 0:
            return 0
        else:
            pair_users = []
            url = "https://api.vk.com/method/users.search"
            params = {
                "fields": "bdate, sex, city, relation",
                "sort": "1",
                "offset": offset,
                "count": '1000',
                "access_token": vktoken(),
                "v": "5.131"
            }
            response = requests.get(url=url, params=params)
            users = response.json()['response']['items']

            ENGAGED, MARRIED = 3, 4  # в начале файла
            for user in users:
                if user['sex'] == info_user['sex']:
                    continue
                relation = user.get('relation')
                if not relation or relation in (ENGAGED, MARRIED):
                    continue
                if not user.get('bdate'):
                    continue
                check_bdate = (
                        ('bdate' not in info_user) or
                        (info_user['bdate'] == user['bdate'][-4:])
                )
                check_city = user.get('city') == info_user.get('city')
                if check_bdate and check_city:
                    pair_users.append(user)

            return pair_users

    def check_users_in_db(self, user_id):
        users = self.find_users(user_id)
        if users == 0:
            return 0
        elif len(users) == 0:
            return 1

        """Создаем пользователя, которому ищем пару в бд"""
        if BotBD.check_candidate(user_id):
            pass
        else:
            BotBD.candidate_add(user_id)

        """Проверка пары в бд"""
        for user in users:
            print(user['id'])
            if BotBD.user_exists(user['id']):
                print('yes')
                return self.find_users(user_id, +100)
            else:
                BotBD.user_add(user['id'], BotBD.see_candidate_id(user_id))


    def find_top_photo(self, user_id):
        users = self.check_users_in_db(user_id)
        if users == 0:
            return 0
        elif len(users) == 0:
            return 1
        elif len(users) >= 1:
            photo_href = dict()
            main_dict = dict()
            for user in users:
                currend_id_user = user['id']
                url = "https://api.vk.com/method/photos.get"
                params = {
                    "user_id": currend_id_user,
                    "access_token": vktoken(),
                    "v": "5.131",
                    "album_id": "profile",
                    "extended": "1"
                }
                response = requests.get(url=url, params=params)
                photograph = response.json()["response"]["items"]
                for photo in photograph:
                    user_href = f"https://vk.com/id{photo['owner_id']}"
                    photo_href[photo["sizes"][-3]["url"]] = photo["likes"]["count"]
                top_photo = sorted(photo_href.items(), key=lambda x: x[1], reverse=True)
                main_dict[user_href] = top_photo[:3]
                photo_href.clear()
            return main_dict


if __name__ == '__main__':
    vkinder = Vksearch()
    # vkinder.find_top_photo('id182970617')
    vkinder.find_top_photo('tataz87')

