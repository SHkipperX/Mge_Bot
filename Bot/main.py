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
import requests
import json
import time
# Другое_2
from orm_connector import db_session
from orm_connector.__all_models import User, User_Heros, User_Stat
from functions import create_keyboard, decoding_orm, Rock_Paper_Scissors, add_user_to_button, Character_show_lvl, \
    Cost_up, Get_stat, dump
from buttons__init__ import *
from button import speech, pop_up
from Mode_text import *
from Game.constants import RANKS

# VK нужен для обращения к методам API через код
# Upload для чего-то другого
VK = None
Upload: VkUpload = None
Route = "data/meme/"
invite: dict[int, dict] = dict()
preparation: dict = dict()
pick_character: dict = dict()
game: dict[int, dict] = dict()
Lvl_up: dict = dict()
general_list = list()


class Text_Commands:
    """
    Обраотчик текстовых команд

    """

    def __init__(self, event_dict: dict):
        self.event_dict = event_dict
        self.peer_id: int = event_dict.get('peer_id')  # chat id
        self.user_id: int = event_dict.get('from_id')
        self.reply_user = None  # то же что и user_id для 2 человека
        self.message: str = event_dict.get('text').lower()
        if event_dict.get('date'):
            self.date: object = date.utcfromtimestamp(event_dict.get('date'))  # дата сообщения
        self.reply: dict = event_dict.get('reply_message')
        if self.reply:
            self.reply_user: int = self.reply.get('from_id')
            self.reply_message: str = self.reply.get('text')
            self.reply_date: object = date.utcfromtimestamp(self.reply.get('date'))
        try:
            self.reply_user = self.message.split()[1][3:12]
        except Exception:
            pass

        self.command_handler()

    def sender(self, message: Optional[str] = None, keyboard: Optional[object] = None,
               attachment: Optional[object] = None) -> None:
        """
        Отправка сообщения в беседу
        :param message: (str) отправляемый текст
        :param keyboard: (VkKeyBoard) клавиатура к сообщению
        :param attachments: (object) фото/аудио фаил (паблик не может отправлять видео фаилы)
        :return:
        """
        post = {'peer_id': self.peer_id, 'chat_id': 100000000, 'message': message, 'keyboard': keyboard,
                'attachment': attachment, 'sticker_id': None, 'peer_ids': self.peer_id,
                'random_id': get_random_id()}
        VK.messages.send(**post)

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

        elif self.message == 'menu':
            self.create_menu()
        elif self.message == 'meme':
            self.meme_image()

    def meme_image(self, file_name='unknown2.png'):
        photo = Upload.photo_messages(Route + file_name)[0]
        owner_id = photo['owner_id']
        media_id = photo['id']
        attachment = f'photo{owner_id}_{media_id}'
        self.sender(attachment=attachment)

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
        user = db_sess.query(User).filter_by(user_id=self.user_id).scalar()

        if not user:
            user = User()

            user.user_id = self.user_id
            user.user_name = 'участник'
            db_sess.add(user)
            db_sess.commit()

            hero = User_Heros(user_key=user.id)
            stats = User_Stat(user_key=user.id)
            db_sess.add(hero)
            db_sess.commit()
            db_sess.add(stats)
            db_sess.commit()

            self.sender(message=f'@id{self.user_id}(USER) Зарегестрирован на участие в МГЕ схватках!')
        else:
            self.sender(message=f'@id{self.user_id}(USER), ты, регистрировался уже!')

        db_sess.close()

    def create_menu(self):
        global Units, Stat
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter_by(user_id=self.user_id).scalar()
        db_sess.close()
        if user:
            buttons = add_user_to_button(Units, Stat, User_1=self.user_id)
            Units, Stat = buttons
            keyboard = create_keyboard(Units, Stat)
            message = f'@id{self.user_id}(Меню)\n' \
                      f'•Улучшения Урона для 1lvl стоит {Cost_up.Damage}, послдедующее улучшение: lvl * {Cost_up.Damage}\n' \
                      f'•Улучшения Здоровья для 1lvl стоит {Cost_up.Health}, послдедующее улучшение: lvl * {Cost_up.Health}\n' \
                      f'•Улучшения Точности для 1lvl стоит {Cost_up.Accuracy}, послдедующее улучшение: lvl * {Cost_up.Accuracy}\n'
            self.sender(message=message, keyboard=keyboard)

        else:
            message = f'@id{self.user_id}, не зарегистрирован!'
            self.sender(message=message)

    def invitation_to_the_mge(self) -> None:
        """
        Приглашение пользователя на дуэль
        :return:
        """
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter_by(user_id=self.user_id).scalar()
        user_2 = db_sess.query(User).filter_by(user_id=self.reply_user).scalar()

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

                    keyboard = create_keyboard(Accept, Deny)
                    invite[id_1] = {'id': id_2, 'bool': False, 'time': date.now(), 'peer_id': self.peer_id}
                    invite[id_2] = {'id': id_1, 'bool': True, 'time': date.now(), 'peer_id': self.peer_id}

                    self.sender(message=text, keyboard=keyboard)
            else:
                message = choice(speech['==']).replace('@id', f'@id{self.reply_user}')
                self.sender(message=message)
        elif user:
            message = f'@id{self.reply_user} no reg!'
            self.sender(message=message)
        elif user_2:
            message = f'@id{self.user_id} no reg!'
            self.sender(message=message)
        db_sess.close()


class Event_Commands:
    """
    Doc
    """

    def __init__(self, event_dict: dict):
        self.user_id: int = event_dict.get('user_id')
        self.event_id: int = event_dict.get('event_id')
        self.peer_id: int = event_dict.get('peer_id')
        self.con_mes_id: int = event_dict.get('conversation_message_id')
        self.payload: dict = event_dict.get('payload')
        squad: str = self.payload.get('squad')
        self.holders_button: list = self.payload.get('ids')

        if (self.user_id in general_list) and (self.user_id in self.holders_button) and squad != 'menu':
            if self.user_id in invite:
                self.toss()

            elif self.user_id in preparation:
                self.rps()

            elif self.user_id in pick_character:
                self.character_selection()

            elif squad == 'game':
                self.mge_pvp()

        elif squad == 'menu' and self.user_id in self.holders_button:
            Menu(type_button=self.payload['type'], user_id=self.user_id, conversation_message_id=self.con_mes_id,
                 peer_id=self.peer_id, event_id=self.event_id)
        else:
            self.event_sender(dump(param='notU'))

    def toss(self) -> None:
        global Rock, Paper, Sciss
        id_1, flag_1 = invite[self.user_id]['id'], invite[self.user_id]['bool']
        id_2, flag_2 = invite[id_1]['id'], invite[id_1]['bool']
        if flag_2:
            self.event_sender(event_data=dump(param='wait'))
        else:
            if self.payload['type'] == 'accept':
                """opt - одно из [камень, ножницы, бумага]"""

                preparation[id_1] = {'id': id_2, 'opt': None, 'time': date.now(), 'peer_id': self.peer_id}
                preparation[id_2] = {'id': id_1, 'opt': None, 'time': date.now(), 'peer_id': self.peer_id}
                Rock, Paper, Sciss = add_user_to_button(Rock, Paper, Sciss, User_1=id_1, User_2=id_2)
                keyboard = create_keyboard(Rock, Paper, Sciss)
                self.messages_edit(message='Тут будет продолжение', keyboard=keyboard)
                del invite[id_1], invite[id_2]


            else:
                del invite[id_1], invite[id_2]

                self.messages_edit(message=f'@id{self.user_id} отказался от битвы')

    def rps(self) -> None:
        global Sniper, Solder, Demoman, Rock, Paper, Sciss
        """
        rps -> Rock-Paper-Scissors
            Выбор победителя
            """
        id_2 = preparation[self.user_id]['id']  # user_id_2

        if not preparation[self.user_id]['opt']:
            preparation[self.user_id]['opt'] = self.payload['type']
        if preparation[id_2]['opt'] and preparation[self.user_id]['opt']:
            db_sess = db_session.create_session()

            buttons = add_user_to_button(Sniper, Solder, Demoman, User_1=self.user_id, User_2=id_2)
            Sniper, Solder, Demoman = buttons
            keyboard = create_keyboard(Sniper, Solder, Demoman)

            parm_1 = [self.user_id, preparation[self.user_id]['opt']]
            parm_2 = [id_2, preparation[id_2]['opt']]
            data = Rock_Paper_Scissors(param_1=parm_1, param_2=parm_2)

            user_1 = data['user_1']
            user_2 = data['user_2']

            id_1, opt_1, status_1 = user_1
            id_2, opt_2, status_2 = user_2

            user_name_1 = db_sess.query(User).filter_by(user_id=id_1).first().user_name
            user_name_2 = db_sess.query(User).filter_by(user_id=id_2).first().user_name

            if status_1:
                """id_1 победил, id_2 проиграл"""
                message = f'@id{id_1}({user_name_1}) Победил @id{id_2}({user_name_2})\n{opt_1} Vs {opt_2}'
                self.messages_edit(message=message, keyboard=keyboard)
                del preparation[id_1], preparation[id_2]
                pick_character[id_1] = {'enemy_id': id_2, 'step': status_1, 'time': date.now(), 'peer_id': self.peer_id}
                pick_character[id_2] = {'enemy_id': id_1, 'step': status_2, 'time': date.now(), 'peer_id': self.peer_id}


            elif status_1 is False:
                """id_1 проиграл, id_2 победил"""
                message = f'@id{id_1}({user_name_1}) Проиграл @id{id_2}({user_name_2})\n{opt_1} Vs {opt_2}'
                self.messages_edit(message=message, keyboard=keyboard)
                del preparation[id_1], preparation[id_2]
                pick_character[id_1] = {'enemy_id': id_2, 'step': status_1, 'time': date.now(), 'peer_id': self.peer_id}
                pick_character[id_2] = {'enemy_id': id_1, 'step': status_2, 'time': date.now(), 'peer_id': self.peer_id}


            else:
                """Ничья"""
                message = f'{opt_1} Vs {opt_2}\nПереигрываем'
                buttons = add_user_to_button(Rock, Paper, Sciss, User_1=id_1, User_2=id_2)
                Rock, Paper, Sciss = buttons

                keyboard = create_keyboard(Rock, Paper, Sciss)

                preparation[self.user_id]['opt'] = None
                preparation[self.user_id]['time'] = date.now()

                preparation[id_2]['opt'] = None
                preparation[id_2]['time'] = date.now()
            self.messages_edit(message=message, keyboard=keyboard)

    def character_selection(self) -> None:
        global Move_L, Head_Sh, Body_Sh, Move_R
        """
        //выбор Персонажей
        :return:
        """
        db_sess = db_session.create_session()
        data_user_1 = db_sess.query(User).filter_by(user_id=self.user_id).first()
        key_id = data_user_1.id
        name = data_user_1.user_name
        data_character = db_sess.query(User_Heros).filter_by(user_key=key_id).first()
        db_sess.close()

        """Инициализация персонажа"""
        step: bool = pick_character[self.user_id]['step']
        enemy_id: int = pick_character[self.user_id]['enemy_id']

        unit: str = self.payload['type']

        person: dict = decoding_orm(data_character, unit)[unit]
        d_lvl, a_lvl = person['d_lvl'], person['a_lvl']
        hp = Character_show_lvl(data_character, param=unit).get_health_point()
        game[self.user_id] = {'enemy_id': enemy_id, 'name': name, 'step': step, 'time': date.now(),
                              'peer_id': self.peer_id,
                              'character': {'class': unit, 'd_lvl': d_lvl, 'a_lvl': a_lvl, 'hp': hp}}

        if self.user_id in game and enemy_id in game:
            enemy_unit = game[enemy_id]['character']['class']
            enemy_name = game[enemy_id]['name']
            if step:  # если право выстрела у нажавшего кнопу полседним
                if unit == 'sniper':
                    buttons = add_user_to_button(Move_L, Head_Sh, Body_Sh, Move_R, User_1=self.user_id)
                    Move_L, Head_Sh, Body_Sh, Move_R = buttons
                    keyboard = create_keyboard(Move_L, Head_Sh, Body_Sh, Move_R)
                else:
                    buttons = add_user_to_button(Move_L, Body_Sh, Move_R, User_1=self.user_id)
                    Move_L, Body_Sh, Move_R = buttons
                    keyboard = create_keyboard(Move_L, Body_Sh, Move_R)
                message = f'Первым стрелять будет @id{self.user_id}({name}) по @id{enemy_id}({enemy_name})'
                self.messages_edit(message=message, keyboard=keyboard)

            else:  # иначе у другого
                if enemy_unit == 'sniper':
                    buttons = add_user_to_button(Move_L, Head_Sh, Body_Sh, Move_R, User_1=enemy_id)
                    Move_L, Head_Sh, Body_Sh, Move_R = buttons
                    keyboard = create_keyboard(Move_L, Head_Sh, Body_Sh, Move_R)
                else:
                    buttons = add_user_to_button(Move_L, Body_Sh, Move_R, User_1=enemy_id)
                    Move_L, Body_Sh, Move_R = buttons
                    keyboard = create_keyboard(Move_L, Body_Sh, Move_R)
                message = f'Первым стрелять будет @id{enemy_id}({enemy_name}) по @id{self.user_id}({name})'
                self.messages_edit(message=message, keyboard=keyboard)
            del pick_character[self.user_id], pick_character[enemy_id]

    def mge_pvp(self):
        """
        PvP 2 игроков
        """
        data_Unit = game[self.user_id]['character']
        d_lvl, h_lvl, a_lvl = data_Unit['d_lvl'], data_Unit['h_lvl'], data_Unit['a_lvl']
        unit = data_Unit['class']

        enemy_id = game[self.user_id]['enemy_id']
        Hp_enemy = game[enemy_id]['character']['hp']

        game[self.user_id]['step'] = False
        game[enemy_id]['step'] = True

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
        post = {'peer_id': self.peer_id, 'message': message, 'attachment': attachment,
                'keyboard': keyboard,
                'conversation_message_id': self.con_mes_id}
        VK.messages.edit(**post)


class Menu:
    def __init__(self, type_button: str, user_id: int, conversation_message_id: int, event_id: int, peer_id: int):
        self.type_button = type_button
        self.user_id = user_id
        self.con_mes_id = conversation_message_id
        self.peer_id = peer_id
        self.event_id = event_id

        if type_button == 'persons':
            self.person()
        elif type_button == 'stat':
            self.all_stat()
        elif type_button in ('sniper_up', 'solder_up', 'demoman_up'):
            self.show_Lvl()
        elif type_button in ('damage', 'health', 'accuracy'):
            self.character_up()
        elif type_button in ('sniper_stat', 'solder_stat', 'demoman_stat'):
            self.detailed_statistics()
        elif type_button == 'back':
            self.back()

    def back(self):
        global Units, Stat
        buttons = add_user_to_button(Units, Stat, User_1=self.user_id)
        Units, Stat = buttons
        keyboard = create_keyboard(Units, Stat)
        message = f'@id{self.user_id}(Меню)\n' \
                  f'•Улучшения Урона для 1lvl стоит {Cost_up.Damage}, послдедующее улучшение: lvl * {Cost_up.Damage}\n' \
                  f'•Улучшения Здоровья для 1lvl стоит {Cost_up.Health}, послдедующее улучшение: lvl * {Cost_up.Health}\n' \
                  f'•Улучшения Точности для 1lvl стоит {Cost_up.Accuracy}, послдедующее улучшение: lvl * {Cost_up.Accuracy}\n'
        self.messages_edit(message=message, keyboard=keyboard)

    def show_Lvl(self):
        global Damage, Health, Accuracy, Back
        db_sess = db_session.create_session()
        key_id = db_sess.query(User).filter_by(user_id=self.user_id).first().id
        Unit_lvls = db_sess.query(User_Heros).filter_by(user_key=key_id).first()
        db_sess.close()

        if self.type_button == 'sniper_up':
            message = Character_show_lvl(Unit_lvls).show_lvl_Sniper()
        elif self.type_button == 'solder_up':
            message = Character_show_lvl(Unit_lvls).show_lvl_Solder()
        elif self.type_button == 'demoman_up':
            message = Character_show_lvl(Unit_lvls).show_lvl_Demoman()
        else:
            message = "Неизвестная ошибка..."
        Lvl_up[self.user_id] = self.type_button

        Damage, Health, Accuracy, Back = add_user_to_button(Damage, Health, Accuracy, Back, User_1=self.user_id)
        keyboard = create_keyboard(Damage, Health, Accuracy, Back)
        self.messages_edit(message=message, keyboard=keyboard)

    def character_up(self):
        global Damage, Health, Accuracy, Back
        # УРОН - 1-10лвл ТОЧНОСТЬ - 1-5лвл ЗДОРОВЬЕ - 1-15лвл

        db_sess = db_session.create_session()
        key_id = db_sess.query(User).filter_by(user_id=self.user_id).first().id
        heros = db_sess.query(User_Heros).filter_by(user_key=key_id).first()

        abc = Character_show_lvl(data_units=heros, param=self.type_button)
        character = Lvl_up[self.user_id]
        if character == 'sniper_up':
            abc = abc.Lvl_Up_sniper()
            message = Character_show_lvl(heros).show_lvl_Sniper()
        elif character == 'solder_up':
            abc = abc.Lvl_Up_solder()
            message = Character_show_lvl(heros).show_lvl_Solder()
        elif character == 'demoman_up':
            abc = abc.Lvl_Up_demoman()
            message = Character_show_lvl(heros).show_lvl_Demoman()

        text, heros = abc['text'], abc['data']

        if text is None:
            db_sess.add(heros)
            db_sess.commit()
            Damage, Health, Accuracy, Back = add_user_to_button(Damage, Health, Accuracy, Back, User_1=self.user_id)
            keyboard = create_keyboard(Damage, Health, Accuracy, Back)
            self.messages_edit(message=message, keyboard=keyboard)
        else:
            self.event_sender(dump(text))
        db_sess.close()

    def person(self):
        global Sniper_up, Solder_up, Demoman_up, Back
        """
        Открываем пользователю его персонажей
        """
        Sniper_up, Solder_up, Demoman_up, Back = add_user_to_button(Sniper_up, Solder_up, Demoman_up, Back,
                                                                    User_1=self.user_id)

        keyboard = create_keyboard(Sniper_up, Solder_up, Demoman_up, Back)

        db_sess = db_session.create_session()
        key_id = db_sess.query(User).filter_by(user_id=self.user_id).first().id
        Char = db_sess.query(User_Heros).filter_by(user_key=key_id).first()
        db_sess.close()

        sum_lvl_sniper = Char.sn_damage + Char.sn_accuracy + Char.sn_health
        sum_lvl_solder = Char.so_damage + Char.so_accuracy + Char.so_health
        sum_lvl_demoman = Char.de_damage + Char.de_accuracy + Char.de_health
        message = f'Суммарный уровень:\n' \
                  f'●Снайпер {sum_lvl_sniper}lvl\n' \
                  f'🚀Солдат {sum_lvl_solder}lvl\n' \
                  f'🔥Подрывник {sum_lvl_demoman}lvl'

        self.messages_edit(message=message, keyboard=keyboard)

    def all_stat(self):
        global Back, Sniper_stat, Solder_stat, Demoman_stat
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter_by(user_id=self.user_id).first()
        balance = db_sess.query(User_Heros).filter_by(user_key=user.id).first().credits
        db_sess.close()

        name = user.user_name
        register = user.reg_date
        points = user.points
        games = user.count_of_game
        wins = user.wins
        loses = user.loses
        rank = None

        for key in RANKS:
            if RANKS[key] <= points:
                rank = key
        if rank is None:
            rank = 'Отсутствует'

        mes_win = f'Побед: 「{wins}({wins / games * 100:.2f}%)」' if wins != 0 else 'Побед: 「0」'
        mes_lose = f'Поражений: 「{loses}({loses / games * 100:.2f}%)」' if loses != 0 else 'Поражений: 「0」'

        message = f'Статистика @id{self.user_id}({name})\n' \
                  f'Зарегистрирован на МГЕ: {register}:\n\n' \
                  f'Очки: 「{points}」¦  Звание: {rank}\n' \
                  f'Игры: 「{games}」¦ Кредиты: {balance}₭\n' \
                  f'{mes_win}¦ {mes_lose}'

        Sniper_stat, Solder_stat, Demoman_stat, Back = add_user_to_button(Sniper_stat, Solder_stat, Demoman_stat, Back,
                                                                          User_1=self.user_id)
        keyboard = create_keyboard(Sniper_stat, Solder_stat, Demoman_stat, Back)
        self.messages_edit(message=message, keyboard=keyboard)

    def detailed_statistics(self):
        global Back, Sniper_stat, Solder_stat, Demoman_stat
        trs_class = {'sniper_stat': 'Снайпер', 'solder_stat': 'Солдат', 'demoman_stat': 'Подрывник'}
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter_by(user_id=self.user_id).first()
        key_id = user.id
        name = user.user_name
        heros_stat = db_sess.query(User_Stat).filter_by(user_key=key_id).first()

        if self.type_button == 'sniper_stat':
            abc = Get_stat(data_unit_stat=heros_stat)
            abc.Sniper_stat()
            message = abc.get_message()

        elif self.type_button == 'solder_stat':
            abc = Get_stat(data_unit_stat=heros_stat)
            abc.Solder_stat()
            message = abc.get_message()
        elif self.type_button == 'demoman_stat':
            abc = Get_stat(data_unit_stat=heros_stat)
            abc.Demoman_stat()
            message = abc.get_message()

        Sniper_stat, Solder_stat, Demoman_stat, Back = add_user_to_button(Sniper_stat, Solder_stat, Demoman_stat, Back,
                                                                          User_1=self.user_id)
        keyboard = create_keyboard(Sniper_stat, Solder_stat, Demoman_stat, Back)
        message = message.replace('@id', f'@id{self.user_id}({name})')
        message = message.replace('@class', trs_class[self.type_button])
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
        post = {'peer_id': self.peer_id, 'message': message, 'attachment': attachment,
                'keyboard': keyboard,
                'conversation_message_id': self.con_mes_id}
        VK.messages.edit(**post)


class Checker_time:
    """
    Doc
    """

    def __init__(self):
        self.wait = delta(minutes=0, seconds=2)

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

            elif name == 'pick_character':
                id_2 = pick_character[id_1]['id']
                del pick_character[id_1], pick_character[id_2]

            index_1 = general_list.index(id_1)
            del general_list[index_1]
            index_2 = general_list.index(id_2)
            del general_list[index_2]

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

                if pick_character:
                    for id in pick_character:
                        self.delete(pick_character[id], 'game')

            except Exception as error:
                print(Text_Warning, error, M_0)


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
        db_session.global_init(db_file=f'data/{Page_id}/{Page_id}.db')

    def runner(self) -> NoReturn:
        """
        :типа докстринг: ахахахаха
        """
        while True:
            try:
                for event in self.VkBotLongPoll.listen():
                    if event.type == VkBotEventType.MESSAGE_EVENT:
                        Event_Commands(event_dict=event.object)
                    elif event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                        Text_Commands(event_dict=event.message)

            except Exception as error:
                print(T_RED, M_FAT, error, '\n', format_exc(), M_0)


if __name__ == '__main__':
    from setting import setting as setting

    token = setting['token_2']
    group_id = setting['group_id']
    Thread(target=Checker_time().pepe).start()
    bot = Bot(token, group_id)
    run = bot.runner
    Thread(target=run, args=()).start()
