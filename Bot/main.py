import random
from typing import *
from traceback import format_exc
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotEvent, VkBotLongPoll, VkBotEventType, VkBotMessageEvent
from vk_api.keyboard import VkKeyboard, VkKeyboardButton
from vk_api.utils import get_random_id
from threading import Thread
from datetime import datetime as date
import json
from orm_connector import db_session
from orm_connector.__all_models import User
from button import BUTTONS_SETTINGS as BS
from random import choice
from Mode_text import *

# VK нужен для обращения к методам API через код
VK = None
buttle_dict: dict = dict()
TEST_bt = BS['test']


class Event_command:
    """
    Doc
    """

    def __init__(self, event_dict: dict):
        self.user_id: int = event_dict['user_id']
        self.event_id: int = event_dict['event_id']
        self.peer_id: int = event_dict['peer_id']
        # event_data = json.dumps(choice(...))
        self.con_mes_id: int = event_dict['conversation_message_id']

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

    def decoding_orm(self, user_object: object) -> list:
        """
        :param user_object:
        :return: [user_name, point, count_of_game, wins, loses]
        """
        if user_object:
            user_data = dict()
            for atr in user_object.__dict__:
                user_data[atr] = user_object.__dict__[atr]
            user_name = user_data['user_name']
            point = user_data['points']
            col_game = user_data['count_of_game']
            win = user_data['wins']
            lose = user_data['loses']
            return [user_name, point, col_game, win, lose]

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

    def command_handler(self) -> None:

        keyboard = self.create_keyboard(TEST_bt)
        self.sender(message='TEXT', keyboard=keyboard)

    def create_keyboard(self, *args) -> VkKeyboard:
        """
        Принимает не ограниченное кол-в аргументов в виде кнопок
        :param args:
        :return: VkKeyboard
        """
        try:
            keyboard = VkKeyboard(one_time=False, inline=True)

            for num, kwargs in enumerate(args):
                if num % 3 == 0 and num != 0:
                    keyboard.add_line()

                else:
                    keyboard.add_callback_button(**kwargs)
            return keyboard.get_keyboard()
        except Exception as error:
            print(T_WHITE, M_FAT, B_RED, error, M_0)

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


class Bot:
    """
    DOC
    Тело бота
    """

    def __init__(self, Token: str, Page_id: str, App_id=6441755):
        global VK
        self.Token = Token
        self.Page_id = Page_id

        self.session = VkApi(token=Token, app_id=App_id)
        self.VkBotLongPoll = VkBotLongPoll(vk=self.session, group_id=Page_id)
        VK = self.session.get_api()
        db_session.global_init(db_file=f'data/{Page_id}.db')

    def runner(self) -> NoReturn:
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
