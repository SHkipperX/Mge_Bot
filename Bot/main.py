# Vk_api
from vk_api import VkApi, VkUpload
from vk_api.bot_longpoll import VkBotEvent, VkBotLongPoll, VkBotEventType, VkBotMessageEvent
from vk_api.keyboard import VkKeyboard
from vk_api.utils import get_random_id
# Другое_1
from random import choice, randint
from typing import *
from traceback import format_exc
from datetime import datetime as date
import json
# Другое_2
from orm_connector import db_session
from orm_connector.__all_models import User
from functions import create_keyboard, decoding_orm
from button import BUTTONS_SETTINGS as bs
from Mode_text import *
from button import ius, cus  # ius - incorrect user send

# VK нужен для обращения к методам API через код
VK = None
Upload = None
battle: dict[int, dict] = dict()
preparation: dict = dict()

Accept = bs.get('accept')
Deny = bs.get('deny')
Rock, Paper, Sciss = bs['rock'], bs['paper'], bs['sciss']


class Event_command:
    """
    Doc
    """

    def __init__(self, event_dict: dict):
        self.user_id: int = event_dict['user_id']
        self.event_id: int = event_dict['event_id']
        self.peer_id: int = event_dict['peer_id']
        self.con_mes_id: int = event_dict['conversation_message_id']
        self.payload: dict = event_dict['payload']
        squad = self.payload.get('rps')

        if self.user_id in battle and not squad == 'rps':
            self.battel()

        elif squad == 'rps':
            self.rps()

    def rps(self):
        """Rock-Paper-Scissors"""

        preparation[self.user_id]['opt'] = self.payload['type']
        id_2 = preparation[self.user_id]['id']
        if preparation[id_2]['opt']:
            """
            Выбор победителя
            """

    def battel(self):

        if battle[self.user_id][self.user_id]:
            self.event_sender(event_data=json.dumps(ius))
        else:
            if self.payload['type'] == 'accept':
                battle[self.user_id][self.user_id] = True
                id_2, id_1 = battle[self.user_id].keys()  # ответ даёт 2 пользователь, поэтому сначала идёт id_2

                preparation[id_2] = {'id': id_1, 'opt': None}
                preparation[id_1] = {'id': id_2, 'opt': None}

                self.messages_edit(message='Тут будет продолжение')
            else:
                for user in battle[self.user_id]:
                    del battle[user]

                self.messages_edit(message=f'@id{self.user_id} отказался от битвы')

    def event_sender(self, event_data: str) -> None:
        """
        Подробнее смотреть док-ю -> https://dev.vk.com/method/messages.sendMessageEventAnswer
        :param event_data: (dict) Объект действия, которое должно произойти после нажатия на кнопку
        :return:
        """
        post = {'peer_id': self.peer_id, 'user_id': self.user_id, 'event_id': self.event_id, 'event_data': event_data}
        VK.messages.sendMessageEventAnswer(**post)

    def messages_edit(self, message: Optional[str], attachment: Optional[object] = None,
                      keyboard: Optional[VkKeyboard] = None) -> None:
        """
        Редактирование сообщения
        :param message:
        :param attachment:
        :param keyboard:
        :return:
        """
        post = {'peer_id': self.peer_id, 'user_id': self.user_id, 'message': message, 'attachment': attachment,
                'keyboard': keyboard,
                'conversation_message_id': self.con_mes_id}
        VK.messages.edit(**post)


class Commands:
    """
    Обраотчик комманд

    """

    def __init__(self, event_dict: dict):
        # print(event_object)
        self.event_dict = event_dict
        self.peer_id: int = event_dict.get('peer_id')  # chat id
        self.user_id: int = event_dict.get('from_id')
        self.reply_user = None  # то же что и user_id для 2 человека
        self.message: str = event_dict.get('text').lower()
        self.date: object = date.utcfromtimestamp(event_dict.get('date'))  # дата сообщения
        self.reply: dict = event_dict.get('reply_message')
        reply = self.reply
        if reply:
            self.reply_user: int = reply.get('from_id')
            self.reply_message: str = reply.get('text')
            self.reply_date: object = date.utcfromtimestamp(reply.get('date'))
        try:
            self.reply_user = self.message.split()[1][3:12]
        except:
            pass

        self.command_handler()

    def command_handler(self) -> None:
        """
        :return:
        """
        if self.message.split()[0] == 'mge':
            self.mge()
            if self.reply_user:
                """Вызов определённого пользователя на дуэль"""
                pass
            else:
                """Вызов рандомного пользователя на дуэль"""
                pass

        elif self.message == 'reg':
            self.register()

        elif self.message.split()[0] == 'name':
            """Смена ника"""
            self.new_nickname()

    def new_nickname(self) -> None:
        """
        :return None:
        """
        result = 'Error'
        nickname = (' ').join(self.event_dict['text'].split()[1:])
        if len(nickname) <= 16:
            db_sess = db_session.create_session()
            db_sess.query(User).filter_by(user_id=self.user_id).update({'user_name': nickname})
            db_sess.commit()
            result = 'complete'
        self.sender(message=f'{result}: {nickname}')

    def register(self) -> None:
        db_sess = db_session.create_session()
        try:
            user_object = db_sess.query(User).filter_by(user_id=self.user_id).first().user_id
            db_sess.close()
            self.sender(message=f'@id{self.user_id}(USER), ты, регистрировался уже!')
        except:

            user = User()
            user.user_id = self.user_id
            user.user_name = 'участник'
            db_sess.add(user)
            db_sess.commit()

            self.sender(message=f'@id{self.user_id}(USER) Зарегестрирован на участие в МГЕ схватках!')

    def sender(self, message: Optional[str] = None, keyboard: Optional[object] = None,
               attachments: Optional[object] = None) -> None:
        """
        Отправка сообщения в беседу
        :param message: (str) отправляемый текст
        :param keyboard: (VkKeyBoard) клавиатура к сообщению
        :param attachments: (object) фото/аудио фаил
        :return:
        """
        post = {'peer_id': self.peer_id, 'chat_id': 100000000, 'message': message, 'keyboard': keyboard,
                'attachments': attachments, 'sticker_id': None, 'peer_ids': self.peer_id,
                'random_id': get_random_id()}
        VK.messages.send(**post)

    def mge(self):
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter_by(user_id=self.user_id).first()
        user_2 = db_sess.query(User).filter_by(user_id=self.reply_user).first()

        if user and user_2:
            id_1: int = user.user_id
            name: str = user.user_name

            id_2: int = user_2.user_id
            name_2: str = user_2.user_name

            if id_1 in battle:
                self.sender(message='Error')
            elif id_2 in battle:
                self.sender(message='Error')
            else:
                text = f'@id{id_1}({name_2.title()}), Вас вызывает на дуэль господин @id{id_2}({name.title()})'
                keyboard = create_keyboard(Accept, Deny)
                battle[id_1] = {id_1: True, id_2: False}
                battle[id_2] = {id_2: False, id_1: True}

                self.sender(message=text, keyboard=keyboard)

        db_sess.close()


class Bot:
    """
    DOC
    Тело бота
    """

    def __init__(self, Token: str, Page_id: str, App_id=6441755):
        global VK, Upload
        self.Token = Token
        self.Page_id = Page_id

        self.session = VkApi(token=Token, app_id=App_id)
        self.VkBotLongPoll = VkBotLongPoll(vk=self.session, group_id=Page_id)
        VK = self.session.get_api()
        Upload = VkUpload(self.session)
        db_session.global_init(db_file=f'data/{Page_id}.db')

    def runner(self) -> NoReturn:
        """
        :типа докстринг: ахахахаха
        """
        while True:
            try:
                for event in self.VkBotLongPoll.listen():
                    print(T_RED, M_FAT, event, M_0)
                    print(event.message)
                    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                        Commands(event_dict=event.message)
                    elif event.type == VkBotEventType.MESSAGE_EVENT:
                        Event_command(event_dict=event.object)
            except Exception as error:
                print(T_RED, M_FAT, error, '\n', format_exc(), M_0)


if __name__ == '__main__':
    from setting import setting as setting

    token = setting['token']
    group_id = setting['group_id']

    bot = Bot(token, group_id)
    bot.runner()
    Commands.create_keyboard()
