import vk_api
import apiai
import json
from vk_api.longpoll import VkLongPoll, VkEventType
import os


def text_Message(user_id, input_msg, random_id):
    request = apiai.ApiAI('b2ac5a69d50645f581a8ef65c95ce218').text_request()
    request.lang = 'ru'
    request.session_id = 'BatlabAIBot'
    request.query = input_msg
    response_Json = json.loads(request.getresponse().read().decode('utf-8'))
    response = response_Json['result']['fulfillment']['speech']
    if response:
        write_msg(user_id, response, random_id)
    else:
        write_msg(user_id, 'Я Вас не совсем понял!', random_id)


def write_msg(user_id, message, random_id):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random_id})


token = os.environ.get('BOT_TOKEN')

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)
# Работа с сообщениями
longpoll = VkLongPoll(vk)

# Основной цикл
for event in longpoll.listen():
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:
            # Сообщение от пользователя
            rid = event.random_id
            request = event.text  # полученное сообщение
            id = event.user_id  # id пользователя
            # ответ
            text_Message(id, request, rid)

