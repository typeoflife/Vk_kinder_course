from vkinder import Vksearch
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from tokens import vkbottoken

vk = vk_api.VkApi(token=vkbottoken())
longpoll = VkLongPoll(vk)

vkinder = Vksearch()

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})

def run_bot():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text

                if request == "привет":
                    write_msg(event.user_id, f"Хай, {event.user_id}")
                else:
                    data = vkinder.find_top_photo(f'{request}')
                    if data == 0:
                        write_msg(event.user_id, f"Нет такого пользователя {request}")
                    elif data == 1:
                        write_msg(event.user_id, f"Нет пары для {request}")
                    else:
                        for user_href, photo in data.items():
                            write_msg(event.user_id, f'{user_href}, {photo}')


if __name__ == '__main__':
    run_bot()