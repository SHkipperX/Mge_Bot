from characters import *


class Rank:
    def __init__(self, points: int):
        self._points = points
        self._rank_name = None


class Player:
    def __init__(self, level_damage: int, level_accuracy: int, level_health: int, hero: str, username: str, rank: str):
        """
        :param level_damage: Уровень урона
        :param level_accuracy: Уровень точности
        :param level_health: Уровень HP
        :param hero: Имя героя: soldier; sniper; любой другой текст: demoman
        :param username: Имя пользователя
        """

        self._user_name = username
        self._hero = Sniper if hero == 'sniper' else Soldier if username == 'soldier' else Demoman

        self._hero.level_up_damage(count_level=level_damage if level_damage > 1 else 1)
        self._hero.level_up_health(count_level=level_health if level_health > 1 else 1)
        self._hero.level_up_accuracy(count_level=level_accuracy if level_accuracy > 1 else 1)
