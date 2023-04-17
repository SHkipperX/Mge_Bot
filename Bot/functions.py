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


def Rock_Paper_Scissors(param_1: list, param_2: list) -> int:
    game_params = {'rock': {'scissors': True, 'paper': False},
                   'paper': {'rock': True, 'scissors': False},
                   'scissors': {'paper': True, 'rock': False}}

    opt_1 = param_1[1]
    opt_2 = param_2[1]
    flag_user_1 = game_params[opt_1].get(opt_2)  # True - первый юзер победил, False - проиграл

    if flag_user_1:
        return {'user_1': [param_1[0], True], 'user_2': [param_2[0], False]}
    elif flag_user_1 is False:
        return {'user_1': [param_1[0], False], 'user_2': [param_2[0], True]}
    return {'user_1': [param_1[0], None], 'user_2': [param_2[0], None]}  # None - ничья
