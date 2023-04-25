from vk_api.keyboard import VkKeyboard
from Mode_text import *
import random


def decoding_orm(user_object: object, character: str) -> dict:
    """___Функция под вопросом___"""
    key = 'sn' if character == 'sniper' else 'so' if character == 'solder' else 'de'
    user_object = user_object.__dict__
    user_data = dict()
    user_data[character] = dict()

    for atr in user_object:
        if key in atr:
            if 'damage' in atr:
                user_data[character]['d_lvl'] = user_object[atr]
            elif 'health' in atr:
                user_data[character]['h_lvl'] = user_object[atr]
            elif 'accuracy' in atr:
                user_data[character]['a_lvl'] = user_object[atr]

    return user_data


def add_user_to_button(*args, User_1: int, User_2: int = None) -> list:
    """Добавление пользователей в кнопочки =)"""
    buttons = []
    for button in args:
        button['payload']['ids'] = [User_1, User_2]
        buttons.append(button)
    return buttons


def create_keyboard(*args) -> VkKeyboard.get_keyboard:
    """
    Принимает не ограниченное кол-в аргументов в виде кнопок
    :param args:
    :return: VkKeyboard
    """

    keyboard = VkKeyboard(one_time=False, inline=True)

    for num, kwargs in enumerate(args):
        try:
            if num % 3 == 0 and num != 0:
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


class Sniper:
    Damage = 50
    Dm_Percent = 0.10

    Health = 80
    Hp_Percent = 0.08

    Accuracy_head = 0.12
    Accuracy_body = 0.40
    Acc_percent = 0.08


class Solder:
    Damage = 80
    Dm_Percent = 0.075

    Health = 130
    Hp_Percent = 0.12

    Accuracy_body = 30
    Acc_percent = 0.06


class Demoman:
    Damage = 70
    Dm_Percent = 0.10

    Health = 100
    Hp_Percent = 0.15

    Accuracy_body = 35
    Acc_percent = 0.08

Const_damage, Const_hp, Const_acc = 10, 15, 5
class Character_show_lvl:


    def __init__(self, data_units: object, param: str = None):
        self.data = data_units
        self.param = param

    def show_lvl_Sniper(self) -> str:
        sn_damage_lvl = self.data.sn_damage
        sn_health_lvl = self.data.sn_health
        sn_accuracy_lvl = self.data.sn_accuracy
        damage = Sniper.Damage * (1 + sn_damage_lvl * Sniper.Dm_Percent) if sn_damage_lvl > 1 else Sniper.Damage
        healh = Sniper.Health * (1 + sn_health_lvl * Sniper.Hp_Percent) if sn_health_lvl > 1 else Sniper.Health
        precent = 1 + Sniper.Acc_percent * sn_accuracy_lvl if sn_accuracy_lvl > 1 else (
            100 * Sniper.Accuracy_head, 100 * Sniper.Accuracy_body)
        if type(precent) is tuple:
            Head, Body = precent
        else:
            Head, Body = Sniper.Accuracy_head * precent, Sniper.Accuracy_body * precent
        message = f'●Снайпер:\n' \
                  f'•Lvl урона: {sn_damage_lvl} | {damage:.1f}Ур\n' \
                  f'•Lvl здоровья: {sn_health_lvl} | {healh:.1f}Hp\n' \
                  f'•Lvl точность: {sn_accuracy_lvl}\n' \
                  f'--Шанс попадания В Голову -> {Head:.1f}% | В Тело -> {Body:.1f}%'
        return message

    def show_lvl_Solder(self) -> str:
        so_damage_lvl = self.data.so_damage
        so_health_lvl = self.data.so_health
        so_accuracy_lvl = self.data.so_accuracy

        damage = Solder.Damage * (1 + so_damage_lvl * Solder.Dm_Percent) if so_damage_lvl > 1 else Solder.Damage
        healh = Solder.Health * (1 + so_health_lvl * Solder.Hp_Percent) if so_health_lvl > 1 else Solder.Health
        precent = 1 + Solder.Acc_percent * so_accuracy_lvl if so_accuracy_lvl > 1 else 1
        Body = Solder.Accuracy_body * precent

        message = f'🚀Солдат:\n' \
                  f'•Lvl урона: {so_damage_lvl} | {damage:.1f}Ур.\n' \
                  f'•Lvl здоровья: {so_health_lvl} | {healh:.1f}Hp\n' \
                  f'•Lvl точности: {so_accuracy_lvl}\n' \
                  f'--Шанс попадания -> {Body:.1f}%'
        return message

    def show_lvl_Demoman(self) -> str:
        de_damage_lvl = self.data.de_damage
        de_health_lvl = self.data.de_health
        de_accuracy_lvl = self.data.de_accuracy

        damage = Demoman.Damage * (1 + de_damage_lvl * Demoman.Dm_Percent) if de_damage_lvl > 1 else Demoman.Damage
        healh = Demoman.Health * (1 + de_health_lvl * Demoman.Hp_Percent) if de_health_lvl > 1 else Demoman.Health
        precent = 1 + Demoman.Acc_percent * de_accuracy_lvl if de_accuracy_lvl > 1 else 1
        Body = Demoman.Accuracy_body * precent

        message = f'🔥Подрывник:\n' \
                  f'•Lvl урона: {de_damage_lvl} | {damage:.1f}Ур.\n' \
                  f'•Lvl здоровья: {de_health_lvl}| {healh:.1f}Хп\n' \
                  f'•Lvl точности: {de_accuracy_lvl}\n' \
                  f'--Шанс попадания -> {Body:.1f}%'
        return message

    def Lvl_Up_sniper(self):
        if self.param == 'damage':
            self.data.sn_damage += 1 if self.data.sn_damage < Const_damage else 0
        elif self.param == 'health':
            self.data.sn_health += 1 if self.data.sn_health < Const_hp else 0
        elif self.param == 'accuracy':
            self.data.sn_accuracy += 1 if self.data.sn_accuracy < Const_acc else 0
        return self.data

    def Lvl_Up_solder(self):
        if self.param == 'damage':
            self.data.so_damage += 1 if self.data.so_damage < Const_damage else 0
        elif self.param == 'health':
            self.data.so_health += 1 if self.data.so_health < Const_hp else 0
        elif self.param == 'accuracy':
            self.data.so_accuracy += 1 if self.data.so_accuracy < Const_acc else 0
        return self.data

    def Lvl_Up_demoman(self):
        if self.param == 'damage':
            self.data.de_damage += 1 if self.data.de_damage < Const_damage else 0
        elif self.param == 'health':
            self.data.de_health += 1 if self.data.de_health < Const_hp else 0
        elif self.param == 'accuracy':
            self.data.de_accuracy += 1 if self.data.de_accuracy < Const_acc else 0
        return self.data
