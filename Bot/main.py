from typing import *
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotEvent, VkBotLongPoll, VkBotEventType, VkBotMessageEvent
from vk_api.keyboard import VkKeyboard, VkKeyboardButton
from datetime import datetime as dt
from random import randint as rnd
from orm_connector import db_session, __all_models
from Mode_text import *

VK = None


class Commands:
    """
    Обраотчик комманд

    """

    def __init__(self, event_object: dict):
        # print(event_object)
        self.peer_id: int = event_object['peer_id']
        self.user_id: int = event_object['from_id']
        self.reply_user = None
        self.message: str = event_object.get('text').lower()
        self.date: object = date.utcfromtimestamp(event_object['date'])
        self.reply: dict = event_object.get('reply_message')
        reply = self.reply
        if reply:
            self.reply_user: int = reply['from_id']
            self.reply_message: str = reply.get('text')
            self.reply_date: object = date.utcfromtimestamp(reply['date'])
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
        """
        Переадрсация
        на
        команды
        """

        if self.message in _cm['mge']:
            if self.reply_user:
                self.mge_for_two()
            else:
                self.mge_for_one()
        elif self.message in _cm['stat']:
            pass
        elif self.message in _cm['top']:
            pass
        elif self.message in _cm['reg']:
            self.register()
        elif self.message in _cm['nick']:
            pass

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
            print(T_RED, error, M_0)

    def sender(self, message: Optional[str] = None, keyboard: Optional[object] = None,
               attachments: Optional[object] = None) -> None:
        """
        Принимает
        : param
        message: Текст сообщения
        : param
        keyboard: Клавиатура в сообщении / нет
        : param
        attachments: приложение(фото)
        """
        post = {'peer_id': self.peer_id, 'chat_id': 100000000, 'message': message, 'keyboard': keyboard,
                'attachments': attachments,
                'random_id': rnd(0, 100000)}
        VK.messages.send(**post)


class Bot:
    """
    DOC
    Тело бота
    """

    def __init__(self, Token: str, Page_id: Optional, App_id=6441755):
        global VK
        self.Token = Token
        self.Page_id = Page_id

        self.session = VkApi(token=Token, app_id=App_id)
        self.VkBotLongPoll = VkBotLongPoll(vk=self.session, group_id=Page_id)
        VK = self.session.get_api()
        db_session.global_init(db_file=f'{Page_id}.db')

    def runner(self) -> NoReturn:
        while True:
            try:
                for event in self.VkBotLongPoll.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                        Commands(event_object=event.object['message'])
            except Exception as error:
                print(T_RED, M_FAT, error, '\n', format_exc(), M_0)


if __name__ == '__main__':
    from setting import setting

    token = setting['token']
    group_id = setting['group_id']
    app_id = setting['app_id']
