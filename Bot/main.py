from vk_api import VkApi, VkUpload  # Vk_api
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
import time
# Другое_2
from orm_connector import db_session
from orm_connector.__all_models import User, User_Heros
from functions import create_keyboard, decoding_orm, Rock_Paper_Scissors
from button import BUTTONS_SETTINGS as bs
from Mode_text import *
from button import pop_up, sp_unccor, sp_corr, speech

# VK нужен для обращения к методам API через код
# Upload для чего-то другого
VK = None
Upload = None
invite: dict[int, dict] = dict()
preparation: dict = dict()
pick_character: dict = dict()
game: dict[int, dict] = dict()
general_list = list()

Accept = bs.get('accept')
Deny = bs.get('deny')
Rock, Paper, Sciss = bs['rock'], bs['paper'], bs['scissors']
Sniper, Solder, Demoman = bs['sniper'], bs['solder'], bs['demoman']
Body_Sh, Head_Sh, Move_R, Move_L = bs['body_shot'], bs['head_shot'], bs['move_R'], bs['move_L']


def dump(param: str) -> json:
    """
    :return:
    """
    if param == 'notU':
        pop_up['text'] = choice(speech['ntubut'])
    if param == 'wait':
        pop_up['text'] = choice(speech['wait'])
    return json.dumps(pop_up)


class Checker_time:
    """
    Doc
    """

    def __init__(self):
        self.wait = delta(minutes=1, seconds=30)

    def delete(self, data: dict, name: str):
        """
        очистка словарей от просроченных пользователей
        """
        start_time = data['time']
        peer_id = data['peer_id']
        id_1 = data['id']
        id_2 = None

        if start_time + self.wait < date.now():

            if name == 'invite':
                id_2 = invite[id_1]['id']
                del invite[id_1], invite[id_2]
            elif name == 'preparation':
                id_2 = preparation[id_1]['id']
                del preparation[id_1], preparation[id_2]
            elif name == 'game':
                id_2 = preparation[id_1]['id']
                del game[id_1], game[id_2]

            print(general_list)
            index_1 = general_list.index(id_1)
            del general_list[index_1]
            index_2 = general_list.index(id_2)
            del general_list[index_2]
            print(general_list)

            self.sender(peer_id=peer_id, message='Error Time')

    def sender(self, peer_id: int, message: str) -> None:
        post = {'peer_id': peer_id, 'chat_id': 100000000, 'message': message,
                'random_id': get_random_id()}
        VK.messages.send(**post)

    def pepe(self):
        """
        Функция ищет просроченное время и удаляет пользователя из игры
        :return:
        """

        while True:
            time.sleep(1)
            try:
                if invite:
                    for id in invite:
                        self.delete(invite[id], 'invite')
                if preparation:
                    for id in preparation:
                        self.delete(preparation[id], 'preparation')
                if game:
                    for id in game:
                        self.delete(game[id], 'game')

            except Exception as error:
                print(Text_Warning, error, M_0)


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
        self.holders_button: list = self.payload['ids']

        if (self.user_id in general_list) and (self.user_id in self.holders_button):
            if self.user_id in invite:
                self.toss()

            elif self.user_id in preparation:
                self.rps()

            elif self.user_id in pick_character:
                self.character_selection()
        else:
            self.event_sender(dump(param='notU'))

    def toss(self) -> None:
        id_1, flag_1 = invite[self.user_id]['id'], invite[self.user_id]['bool']
        id_2, flag_2 = invite[id_1]['id'], invite[id_1]['bool']
        if flag_2:
            self.event_sender(event_data=dump(param='wait'))
        else:
            if self.payload['type'] == 'accept':
                """opt - одно из [камень, ножницы, бумага]"""

                preparation[id_1] = {'id': id_2, 'opt': None, 'time': date.now(), 'peer_id': self.peer_id}
                preparation[id_2] = {'id': id_1, 'opt': None, 'time': date.now(), 'peer_id': self.peer_id}
                Rock['payload']['ids'] = [id_1, id_2]
                Paper['payload']['ids'] = [id_1, id_2]
                Sciss['payload']['ids'] = [id_1, id_2]
                keyboard = create_keyboard(Rock, Paper, Sciss)
                self.messages_edit(message='Тут будет продолжение', keyboard=keyboard)
                del invite[id_1], invite[id_2]


            else:
                del invite[id_1], invite[id_2]

                self.messages_edit(message=f'@id{self.user_id} отказался от битвы')

    def rps(self) -> None:
        """
        rps -> Rock-Paper-Scissors
            Выбор победителя
            """
        id_2 = preparation[self.user_id]['id']  # user_id_2

        if not preparation[self.user_id]['opt']:
            preparation[self.user_id]['opt'] = self.payload['type']
        if preparation[id_2]['opt'] and preparation[self.user_id]['opt']:
            db_sess = db_session.create_session()

            Sniper['payload']['ids'], Solder['payload']['ids'], Demoman['payload']['ids'] = [self.user_id, id_2], [
                self.user_id, id_2], [self.user_id, id_2]
            keyboard = create_keyboard(Sniper, Solder, Demoman)

            parm_1 = [self.user_id, preparation[self.user_id]['opt']]
            parm_2 = [id_2, preparation[id_2]['opt']]
            data = Rock_Paper_Scissors(param_1=parm_1, param_2=parm_2)

            user_1 = data['user_1']
            user_2 = data['user_2']

            id_1, opt_1, status_1 = user_1
            id_2, opt_2, status_2 = user_2

            pick_character[id_1] = {'enemy_id': id_2, 'step': status_1}
            pick_character[id_2] = {'enemy_id': id_1, 'step': status_2}

            user_name_1 = db_sess.query(User).filter_by(user_id=id_1).first().user_name
            user_name_2 = db_sess.query(User).filter_by(user_id=id_2).first().user_name

            if status_1:
                """id_1 победил, id_2 проиграл"""
                message = f'@id{id_1}({user_name_1}) Победил @id{id_2}({user_name_2})\n{opt_1} Vs {opt_2}'
                self.messages_edit(message=message, keyboard=keyboard)
                del preparation[id_1], preparation[id_2]


            elif status_1 is False:
                """id_1 проиграл, id_2 победил"""
                message = f'@id{id_1}({user_name_1}) Проиграл @id{id_2}({user_name_2})\n{opt_1} Vs {opt_2}'
                self.messages_edit(message=message, keyboard=keyboard)
                del preparation[id_1], preparation[id_2]


            else:
                """Ничья"""
                message = f'{opt_1} Vs {opt_2}\nПереигрываем'

                Rock['payload']['ids'] = [id_1, id_2]
                Paper['payload']['ids'] = [id_1, id_2]
                Sciss['payload']['ids'] = [id_1, id_2]

                keyboard = create_keyboard(Rock, Paper, Sciss)

                preparation[self.user_id]['opt'] = None
                preparation[self.user_id]['time'] = date.now()

                preparation[id_2]['opt'] = None
                preparation[id_2]['time'] = date.now()
            self.messages_edit(message=message, keyboard=keyboard)

    def character_selection(self) -> None:
        """
        :return:
        """
        db_sess = db_session.create_session()
        data_user_1 = db_sess.query(User).filter_by(user_id=self.user_id).first()
        key_id = data_user_1.id
        name = data_user_1.user_name
        data_character = db_sess.query(User_Heros).filter_by(user_key=key_id).first()

        """Инициализация персонажа"""
        step = pick_character[self.user_id]['step']
        enemy_id = pick_character[self.user_id]['enemy_id']
        enemy_step = pick_character[enemy_id]['step']

        unit = self.payload['type']

        person = decoding_orm(data_character, unit)[unit]
        d_lvl, h_lvl, a_lvl = person['d_lvl'], person['h_lvl'], person['a_lvl']
        game[self.user_id] = {'enemy_id': enemy_id, 'name': name, 'step': step, 'time': date.now(),
                              'character': {'class': unit, 'd_lvl': d_lvl, 'h_lvl': h_lvl, 'a_lvl': a_lvl, 'hp': int}}

        if self.user_id in game and enemy_id in game:
            enemy_unit = game[enemy_id]['character']['class']
            enemy_name = game[enemy_id]['name']
            if step:  # если право выстрела у нажавшего кнопу полседним
                # инициализируем кнопочки
                if unit == 'sniper':
                    Head_Sh['payload']['step'], Head_Sh['payload']['ids'] = step, [self.user_id, enemy_id]
                Body_Sh['payload']['step'], Move_R['payload']['step'], Move_L['payload']['step'] = step, step, step
                Body_Sh['payload']['ids'], Move_R['payload']['ids'], Move_L['payload']['ids'] = [self.user_id, enemy_id], [self.user_id, enemy_id], [
                    self.user_id, enemy_id]
                if unit == 'sniper':
                    keyboard = create_keyboard(Move_L, Head_Sh, Body_Sh, Move_R)
                else:
                    keyboard = create_keyboard(Move_L, Body_Sh, Move_R)
                message = f'Первым стрелять будет @id{self.user_id}({name}) по @id{enemy_id}({enemy_name})'
            else:  # иначе у другого
                if enemy_unit == 'sniper':
                    Head_Sh['payload']['step'], Head_Sh['payload']['ids'] = step, [self.user_id, enemy_id]
                Body_Sh['payload']['step'], Move_R['payload']['step'], Move_L['payload']['step'] = step, step, step
                Body_Sh['payload']['ids'], Move_R['payload']['ids'], Move_L['payload']['ids'] = [self.user_id, enemy_id], [self.user_id, enemy_id], [
                    self.user_id, enemy_id]
                if enemy_unit == 'sniper':
                    keyboard = create_keyboard(Move_L, Head_Sh, Body_Sh, Move_R)
                else:
                    keyboard = create_keyboard(Move_L, Body_Sh, Move_R)
                message = f'Первым стрелять будет @id{enemy_id}({enemy_name}) по @id{self.user_id}({name})'

            self.messages_edit(message=message, keyboard=keyboard)

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
        """
        Добавление пользователя в базу данных
        """
        db_sess = db_session.create_session()
        try:
            user = db_sess.query(User).filter_by(user_id=self.user_id).first().user_id
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
        """
        Приглашение пользователя на дуэль
        :return:
        """
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
                    general_list.append(id_1), general_list.append(id_2)
                    print(general_list)
                    keyboard = create_keyboard(Accept, Deny)
                    invite[id_1] = {'id': id_2, 'bool': False, 'time': date.now(), 'peer_id': self.peer_id}
                    invite[id_2] = {'id': id_1, 'bool': True, 'time': date.now(), 'peer_id': self.peer_id}

                    self.sender(message=text, keyboard=keyboard)
            else:
                self.sender(message=f'Error: @id{user.user_id} == @id{user_2.user_id}')
        else:
            name = f'@id{self.reply_user}'
            self.sender(message=speech['ntrg'][0].replace('@id', name))
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
