from typing import Union

from characters import Sniper, Demoman, Soldier, TARGET_BODY, TARGET_HEAD
from constants import RANKS
from tools import rank_to_str, is_rank


class Player:
    def __init__(self, hero: str, username: str, rank: Union[int, str], l_damage: int = 0, l_accuracy: int = 0,
                 l_health: int = 0, ):
        """
        :param l_damage: Уровень урона
        :param l_accuracy: Уровень точности
        :param l_health: Уровень HP
        :param hero: Имя героя: soldier; sniper; любой другой текст: demoman
        :param username: Имя пользователя
        :param rank: Очки или имя ранга
        """

        self._user_name = username
        self._rank = rank if type(rank) == str and is_rank(rank, RANKS) else rank_to_str(rank, RANKS) if type(
            rank) == int else 'Unknown'
        self._hero = Sniper() if hero == 'sniper' else Soldier() if hero == 'soldier' else Demoman()

        self._hero.level_up_damage(count_level=l_damage)
        self._hero.level_up_health(count_level=l_health)
        self._hero.level_up_accuracy(count_level=l_accuracy)

    @property
    def rank(self) -> str:
        return self._rank
