from typing import Dict, Union, Tuple

RANKS: Dict[str, int] = {
    "Хомяк": 250,
    "Гибус": 400,
    "Трейдорас": 550,
    "Трайхардер": 700,
    "МГЕ-БРАТ": 850,
    "Путис": 1000,
    "Хеил": 1300,
    "Король Сервера": 1800
}

# Targets for Sniper
TARGET_BODY: str = '_body_'
TARGET_HEAD: str = '_head_'

# Characters
SNIPER_STATS: Dict[str, Union[Union[float, int], Tuple[float, float]]] = {
    'damage_value': 50,
    'percent_damage': 10,
    'accuracy_value': 40,
    'percent_accuracy': 12,
    'health_value': 80,
    'percent_health': 8
}
SNIPER_HEAD_ACCURACY: int = 12

SOLDIER_STATS: Dict[str, Union[Union[float, int], Tuple[float, float]]] = {
    'damage_value': 80,
    'splash_damage_range': (.2, .8),
    'percent_damage': 7.5,
    'accuracy_value': 30,
    'percent_accuracy': 6,
    'health_value': 130,
    'percent_health': 12
}

DEMOMAN_STATS: Dict[str, Union[Union[float, int], Tuple[float, float]]] = {
    'damage_value': 70,
    'splash_damage_range': (.1, .5),
    'percent_damage': 10,
    'accuracy_value': 35,
    'percent_accuracy': 8,
    'health_value': 100,
    'percent_health': 15
}

# Steps
SIDE_LEFT: str = '_left_'
SIDE_RIGHT: str = '_right_'
