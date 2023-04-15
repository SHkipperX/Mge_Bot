from vk_api.keyboard import VkKeyboard
from Mode_text import *

def decoding_orm(user_object: object) -> list:
    """
    :param user_object:
    :return: [user_name, point, count_of_game, wins, loses]
    """
    if user_object:
        user_data = dict()
        for atr in user_object.__dict__:
            user_data[atr] = user_object.__dict__[atr]
        return user_data


def create_keyboard(*args) -> VkKeyboard.get_keyboard:
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
