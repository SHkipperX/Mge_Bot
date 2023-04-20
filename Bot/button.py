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

    'body_shot': {'label': 'Тело', 'color': GREEN, 'payload': {'type': 'bd_sh', 'squad': 'game', 'ids': None}},
    'head_shot': {'label': 'Голова', 'color': RED, 'payload': {'type': 'hs_sh', 'squad': 'game', 'ids': None}},
    'move_R': {'label': 'Вправо', 'color': BLUE, 'payload': {'type': 'move_r', 'squad': 'game', 'ids': None}},
    'move_L': {'label': 'Влево', 'color': BLUE, 'payload': {'type': 'move_l', 'squad': 'game', 'ids': None}}
}

sp_unccor = ['1', '2', '3', '4', '5', '6', '7', '8']
ius = {"type": "show_snackbar", "text": None}

sp_corr = ['1', '2', '3', '4', '5', '6', '7', '8']
cus = {"type": "show_snackbar", "text": None}


