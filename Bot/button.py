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
a = {'label': 'Label', 'color': color, 'payload': {'type': 'Type'}}

BUTTONS_SETTINGS: dict[str, dict] = {
    'test': {'label': 'Push', 'color': RED, 'payload': {"type": "show_snackbar", "text": "Биг_Пиг"}},

    'rock': {'label': 'Камень', 'color': RED, 'payload': {'type': 'rock', 'squad': 'rps'}},
    'paper': {'label': 'Бумага', 'color': WHITE, 'payload': {'type': 'paper', 'squad': 'rps'}},
    'scissors': {'label': 'Ножницы', 'color': GREEN, 'payload': {'type': 'scissors', 'squad': 'rps'}},

    'accept': {'label': 'принять', 'color': GREEN, 'payload': {'type': 'accept'}},
    'deny': {'label': 'отказать', 'color': RED, 'payload': {'type': 'deny'}}
}

incorrect_user_click = ['1', '2', '3', '4', '5', '6', '7', '8']
ius = {"type": "show_snackbar", "text": f"{random.choice(incorrect_user_click)}"}

correct_user_click = ['1', '2', '3', '4', '5', '6', '7', '8']
cus = {"type": "show_snackbar", "text": f"{random.choice(correct_user_click)}"}


