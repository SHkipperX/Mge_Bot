import random

from vk_api.keyboard import VkKeyboardColor as color

BLUE = color.PRIMARY  # Синяя
WHITE = color.SECONDARY  # Белая
RED = color.NEGATIVE  # Красная
GREEN = color.POSITIVE  # Зелёная

"""
KeyBoardDoc --> https://dev.vk.com/api/bots/development/keyboard
"""
BUTTONS_SETTINGS: dict[str, dict] = {
    'test': {'label': 'Push', 'color': RED, 'payload': {"type": "show_snackbar", "text": "Биг_Пиг"}},

    'rock': {'label': 'Камень', 'color': RED, 'payload': {'type': 'rock'}},
    'paper': {'label': 'Бумага', 'color': WHITE, 'payload': {'type': 'paper'}},
    'scissors': {'label': 'Ножницы', 'color': GREEN, 'payload': {'type': 'scissors'}}
}

incorrect_user_click = ['1', '2', '3', '4', '5', '6', '7', '8']
ius = {"type": "show_snackbar", "text": f"{random.choice(incorrect_user_click)}"}

correct_user_click = ['1', '2', '3', '4', '5', '6', '7', '8']
cus = {"type": "show_snackbar", "text": f"{random.choice(correct_user_click)}"}


