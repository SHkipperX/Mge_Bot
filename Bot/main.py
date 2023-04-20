# Vk_api
import time

from vk_api import VkApi, VkUpload
from vk_api.bot_longpoll import VkBotEvent, VkBotLongPoll, VkBotEventType, VkBotMessageEvent
from vk_api.keyboard import VkKeyboard
from vk_api.utils import get_random_id
# Другое_1
from random import choice, randint
from typing import *
from traceback import format_exc
from datetime import datetime as date
from datetime import timedelta as delta
from threading import Thread
import json
# Другое_2
from orm_connector import db_session
from orm_connector.__all_models import User, User_Heros
from functions import create_keyboard, decoding_orm, Rock_Paper_Scissors
from button import BUTTONS_SETTINGS as bs
from Mode_text import *
from button import ius, cus, sp_unccor, sp_corr

# VK нужен для обращения к методам API через код
VK = None
Upload = None
invite: dict[int, dict] = dict()
preparation: dict = dict()
game: dict[int, dict] = dict()

Accept = bs.get('accept')
Deny = bs.get('deny')
Rock, Paper, Sciss = bs['rock'], bs['paper'], bs['scissors']


class Checker_time:
    """
    Doc
    """

    def __init__(self):
        self.wait = delta(seconds=5)

    def delete(self, x: dict, name: str):
        start_time = x['time']
        peer_id = x['peer_id']
        id_1 = x['id']

        if start_time + self.wait < date.now():
            self.sender(peer_id=peer_id, message='Error Time')
            if name == 'invite':
                id_2 = invite[id_1]['id']
                del invite[id_1], invite[id_2]
            elif name == 'preparation':
                id_2 = preparation[id_1]['id']
                del preparation[id_1], preparation[id_2]
            elif name == 'game':
                pass

    def sender(self, peer_id: int, message: str) -> None:
        post = {'peer_id': peer_id, 'chat_id': 100000000, 'message': message,
                'random_id': get_random_id()}
        VK.messages.send(**post)

    def pepe(self):

        while True:
            time.sleep(1)
            try:
                if invite:
                    for data in invite:
                        self.delete(invite[data], 'invite')
                if preparation:
                    for data in preparation:
                        self.delete(preparation[data], 'preparation')

            except Exception as error:
                print(error.__repr__())


def dump() -> json:
    """
    :return:
    """
    ius['text'] = choice(sp_unccor)
    return json.dumps(ius)


class Event_commands:
    """
    Doc
    """

    def __init__(self, event_dict: dict):
        self.user_id: int = event_dict['user_id']
        self.event_id: int = event_dict['event_id']
        self.peer_id: int = event_dict['peer_id']
        self.con_mes_id: int = event_dict['conversation_message_id']
        self.payload: dict = event_dict['payload']
        squad: str = self.payload.get('squad')
        holders_button: list = self.payload['ids']
        if self.user_id in holders_button:
            if self.user_id in invite and not squad == 'rps':
                self.toss()

            elif squad == 'rps' and self.user_id in preparation:
                self.rps()
        else:
            self.event_sender(dump())

    def rps(self) -> None:
        """Rock-Paper-Scissors
            Выбор победителя
            """
        id_2 = preparation[self.user_id]['id']
        if not preparation[self.user_id]['opt']:
            preparation[self.user_id]['opt'] = self.payload['type']
        if preparation[self.user_id]['opt']:
            self.event_sender(dump())
        elif preparation[id_2]['opt'] and preparation[self.user_id]['opt']:
            db_sess = db_session.create_session()

            parm_1 = [self.user_id, preparation[self.user_id]['opt']]
            parm_2 = [id_2, preparation[id_2]['opt']]
            flag = Rock_Paper_Scissors(param_1=parm_1, param_2=parm_2)

            user_1 = flag['user_1']
            user_2 = flag['user_2']

            id_1, status_1 = user_1
            id_2, status_2 = user_2

            user_name_1 = db_sess.query(User).filter_by(user_id=id_1).first().user_name
            user_name_2 = db_sess.query(User).filter_by(user_id=id_2).first().user_name

            if status_1:
                """id_1 победил, id_2 проиграл"""
                message = f'@id{id_1}({user_name_1}) Победил @id{id_2}({user_name_2})\n{parm_1[1]} Vs {parm_2[1]}'
                self.messages_edit(message=message)
            elif status_1 is False:
                """id_1 проиграл, id_2 победил"""
                message = f'@id{id_1}({user_name_1}) Проиграл @id{id_2}({user_name_2})\n{parm_1[1]} Vs {parm_2[1]}'
                self.messages_edit(message=message)
            else:
                """Ничья"""
                message = f'{parm_1[1]} Vs {parm_2[1]}\nПереигрываем'
                keyboard = create_keyboard(Rock, Paper, Sciss)
                preparation[self.user_id]['opt'] = None
                preparation[self.user_id]['time'] = date.now()
                preparation[id_2]['opt'] = None
                preparation[id_2]['time'] = date.now()
                self.messages_edit(message=message, keyboard=keyboard)

    def toss(self) -> None:
        id_1, flag_1 = invite[self.user_id]['id'], invite[self.user_id]['bool']
        id_2, flag_2 = invite[id_1]['id'], invite[id_1]['bool']
        print(f'{id_1}:{flag_1}\n{id_2}:{flag_2}')
        if flag_2:
            self.event_sender(event_data=json.dumps(ius))
        else:
            if self.payload['type'] == 'accept':
                """opt - одно из [камень, ножницы, бумага]"""

                preparation[id_1] = {'id': id_2, 'opt': None, 'time': date.now(), 'peer_id': self.peer_id}
                preparation[id_2] = {'id': id_1, 'opt': None, 'time': date.now(), 'peer_id': self.peer_id}
                keyboard = create_keyboard(Rock, Paper, Sciss)
                self.messages_edit(message='Тут будет продолжение', keyboard=keyboard)

            else:
                del invite[id_1], invite[id_2]

                self.messages_edit(message=f'@id{self.user_id} отказался от битвы')

    def event_sender(self, event_data: str) -> None:
        """
        //Эфемерное сообщение
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
        :param message: текст не более 1000 символов
        :param attachment: фото/аудио фаил
        :param keyboard: клавиатура inline/no-inline
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
        except Exception:
            pass

        self.command_handler()

    def command_handler(self) -> None:
        """
        :return:
        """
        if self.message.split()[0] == 'mge':
            self.invitation_to_the_mge()
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
        Смена имени в database
        :return None:
        """
        nickname = (' ').join(self.event_dict['text'].split()[1:])
        result = f'Error: {len(nickname)} < 16 символов'
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
            self.sender(message=f'@id{self.user_id}(USER), ты, регистрировался уже!')
        except Exception:

            user = User()
            user.user_id = self.user_id
            user.user_name = 'участник'
            db_sess.add(user)
            db_sess.commit()
            hero = User_Heros(user_key=user.id)
            db_sess.add(hero)
            db_sess.commit()
            self.sender(message=f'@id{self.user_id}(USER) Зарегестрирован на участие в МГЕ схватках!')

        finally:
            db_sess.close()

    def sender(self, message: Optional[str] = None, keyboard: Optional[object] = None,
               attachments: Optional[object] = None) -> None:
        """
        Отправка сообщения в беседу
        :param message: (str) отправляемый текст
        :param keyboard: (VkKeyBoard) клавиатура к сообщению
        :param attachments: (object) фото/аудио фаил (паблик не может оправлять видео фаилы)
        :return:
        """
        post = {'peer_id': self.peer_id, 'chat_id': 100000000, 'message': message, 'keyboard': keyboard,
                'attachments': attachments, 'sticker_id': None, 'peer_ids': self.peer_id,
                'random_id': get_random_id()}
        VK.messages.send(**post)

    def invitation_to_the_mge(self) -> None:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter_by(user_id=self.user_id).first()
        user_2 = db_sess.query(User).filter_by(user_id=self.reply_user).first()

        if user and user_2:
            if user.user_id != user_2.user_id:
                id_1: int = user.user_id
                name: str = user.user_name

                id_2: int = user_2.user_id
                name_2: str = user_2.user_name

                if id_1 in invite:
                    self.sender(message=f'Error: @id{id_1} is invited')
                elif id_2 in invite:
                    self.sender(message=f'Error: @id{id_2} is invited')
                else:
                    text = f'@id{id_1}({name_2.title()}), Вас вызывает на дуэль господин @id{id_2}({name.title()})'
                    Accept['payload']['ids'] = [id_1, id_2]
                    Deny['payload']['ids'] = [id_1, id_2]
                    print(Accept, Deny)
                    keyboard = create_keyboard(Accept, Deny)
                    invite[id_1] = {'id': id_2, 'bool': False, 'time': date.now(), 'peer_id': self.peer_id}
                    invite[id_2] = {'id': id_1, 'bool': True, 'time': date.now(), 'peer_id': self.peer_id}

                    self.sender(message=text, keyboard=keyboard)
            else:
                self.sender(message=f'Error: {user.user_id}=={user_2.user_id}')
        else:
            self.sender(message='Error')
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
                    # print(T_RED, M_FAT, event, M_0)
                    # print(event.message)
                    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                        Commands(event_dict=event.message)
                    elif event.type == VkBotEventType.MESSAGE_EVENT:
                        Event_commands(event_dict=event.object)
            except Exception as error:
                print(T_RED, M_FAT, error, '\n', format_exc(), M_0)


if __name__ == '__main__':
    from setting import setting as setting

    token = setting['token']
    group_id = setting['group_id']
    Thread(target=Checker_time().pepe).start()
    bot = Bot(token, group_id)
    bot.runner()
    Commands.create_keyboard()
