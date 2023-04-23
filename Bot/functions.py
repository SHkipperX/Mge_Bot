from vk_api.keyboard import VkKeyboard
from Mode_text import *
import random


def decoding_orm(user_object: object, character: str) -> dict:
    key = 'sn' if character == 'sniper' else 'so' if character == 'solder' else 'de'
    user_object = user_object.__dict__
    user_data = dict(sniper={}, solder={}, demoman={})
    for atr in user_object:
        if key in atr:
            if 'damage' in atr:
                user_data[character]['d_lvl'] = user_object[atr]
            if 'health' in atr:
                user_data[character]['h_lvl'] = user_object[atr]
            if 'accuracy' in atr:
                user_data[character]['a_lvl'] = user_object[atr]
    return user_data


def create_keyboard(*args) -> VkKeyboard.get_keyboard:
    """
    Принимает не ограниченное кол-в аргументов в виде кнопок
    :param args:
    :return: VkKeyboard
    """

    keyboard = VkKeyboard(one_time=False, inline=True)

    for num, kwargs in enumerate(args):
        print(kwargs)
        try:
            if (num % 3 == 0 and num != 0) and len(args) != 4:
                keyboard.add_line()

            keyboard.add_callback_button(**kwargs)

        except Exception as error:
            print(Text_Warning, error, M_0)
    return keyboard.get_keyboard()


def Rock_Paper_Scissors(param_1: list[int, str], param_2: list[int, str]) -> dict:
    translate = {'rock': 'Камень', 'paper': 'Бумага', 'scissors': 'Ножницы'}
    game_params = {'rock': {'scissors': True, 'paper': False},
                   'paper': {'rock': True, 'scissors': False},
                   'scissors': {'paper': True, 'rock': False}}

    opt_1 = param_1[1]
    opt_2 = param_2[1]
    translate_opt1 = translate[opt_1]
    translate_opt2 = translate[opt_2]
    flag_user_1 = game_params[opt_1].get(opt_2)  # True - первый юзер победил, False - проиграл

    if flag_user_1:
        return {'user_1': [param_1[0], translate_opt1, True], 'user_2': [param_2[0], translate_opt2, False]}
    elif flag_user_1 is False:
        return {'user_1': [param_1[0], translate_opt1, False], 'user_2': [param_2[0], translate_opt2, True]}
    return {'user_1': [param_1[0], translate_opt1, None], 'user_2': [param_2[0], translate_opt2, None]}  # None - ничья
