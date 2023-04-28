import random
import json
from vk_api.keyboard import VkKeyboardColor as color

BLUE = color.PRIMARY  # Синяя
WHITE = color.SECONDARY  # Белая
RED = color.NEGATIVE  # Красная
GREEN = color.POSITIVE  # Зелёная

"""
KeyBoardDoc --> https://dev.vk.com/api/bots/development/keyboard
"""
a = {'label': '___', 'color': None, 'payload': {'type': '___'}}

BUTTONS_SETTINGS: dict[str, dict] = {
    'accept': {'label': 'принять', 'color': GREEN, 'payload': {'type': 'accept', 'ids': None}},
    'deny': {'label': 'отказать', 'color': RED, 'payload': {'type': 'deny', 'ids': None}},

    'rock': {'label': 'Камень', 'color': RED, 'payload': {'type': 'rock', 'squad': 'rps', 'ids': None}},
    'paper': {'label': 'Бумага', 'color': WHITE, 'payload': {'type': 'paper', 'squad': 'rps', 'ids': None}},
    'scissors': {'label': 'Ножницы', 'color': GREEN, 'payload': {'type': 'scissors', 'squad': 'rps', 'ids': None}},

    'sniper': {'label': 'Снайпер', 'color': RED, 'payload': {'type': 'sniper', 'squad': 'class'}},
    'solder': {'label': 'Солдат', 'color': BLUE, 'payload': {'type': 'solder', 'squad': 'class'}},
    'demoman': {'label': 'Подрывник', 'color': GREEN, 'payload': {'type': 'demoman', 'squad': 'class'}},
    'shot_L': {'label': 'Влево', 'color': GREEN,
               'payload': {'type': '_left_', 'squad': 'game', 'step': False, 'ids': []}},
    'shot_R': {'label': 'Вправо', 'color': WHITE,
               'payload': {'type': '_right_', 'squad': 'game', 'step': False, 'ids': []}},
    'body_shot': {'label': 'Выстрел в тело', 'color': GREEN,
                  'payload': {'type': '_body_', 'squad': 'game', 'step': False, 'ids': []}},
    'head_shot': {'label': 'Выстрел в голову', 'color': RED,
                  'payload': {'type': '_head_', 'squad': 'game', 'step': False, 'ids': []}},
    'move_R': {'label': 'Вправо', 'color': BLUE,
               'payload': {'type': '_right_', 'squad': 'game', 'step': False, 'ids': []}},
    'move_L': {'label': 'Влево', 'color': BLUE,
               'payload': {'type': '_left_', 'squad': 'game', 'step': False, 'ids': []}},
    'units': {'label': 'Персонажи', 'color': BLUE,
              'payload': {'type': 'persons', 'squad': 'menu'}},
    'back': {'label': 'Назад', 'color': BLUE,
             'payload': {'type': 'back', 'squad': 'menu'}},

    'menu_setting': {
        'stat': {'label': 'Статистика', 'color': WHITE, 'payload': {'type': 'stat', 'squad': 'menu', 'ids': []}},

        'units': {'sniper': {'label': 'Снайпер', 'color': RED,
                             'payload': {'type': 'sniper_up', 'squad': 'menu', 'ids': []}},
                  'solder': {'label': 'Солдат', 'color': BLUE,
                             'payload': {'type': 'solder_up', 'squad': 'menu', 'ids': []}},
                  'demoman': {'label': 'Подрывник', 'color': GREEN,
                              'payload': {'type': 'demoman_up', 'squad': 'menu', 'ids': []}}},

        'lvl_up': {'damage': {'label': 'Урон', 'color': RED, 'payload': {'type': 'damage', 'squad': 'menu', 'ids': []}},
                   'health': {'label': 'Здоровье', 'color': GREEN,
                              'payload': {'type': 'health', 'squad': 'menu', 'ids': []}},
                   'accuracy': {'label': 'Точность', 'color': WHITE,
                                'payload': {'type': 'accuracy', 'squad': 'menu', 'ids': []}}}},
    'sniper_stat': {'label': 'Снайпер', 'color': RED,
                    'payload': {'type': 'sniper_stat', 'squad': 'menu', 'ids': []}},
    'solder_stat': {'label': 'Солдат', 'color': BLUE,
                    'payload': {'type': 'solder_stat', 'squad': 'menu', 'ids': []}},
    'demoman_stat': {'label': 'Подрывник', 'color': GREEN,
                     'payload': {'type': 'demoman_stat', 'squad': 'menu', 'ids': []}}
}

pop_up = {"type": "show_snackbar", "text": None}

speech = {'inv': ['@id уже приглашён кем-то!', '@id ожидает своей битвы!', '@id всё ещё в раздумьях, подожди ещё!'],
          'ntubut': ['Это не твоя кнопочка!❏', 'не трогай меня ╱╸◠╺╲', 'Я могу и разочароваться в тебеت'],
          '==': ['@id с самим собой?〠', '@id, а-за-за, нельзя так ㋡', '@id, много умный играть против себя?'],
          'ntrg': ['@id ещё не регистрировался для участия в битвах', '@id, не находится в списках МГЕ...'],
          'wait': ['Ожидай ответа!']}
