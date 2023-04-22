from typing import Union

from characters import Sniper, Demoman, Soldier, TARGET_BODY, TARGET_HEAD
from constants import RANKS
from tools import rank_to_str, is_rank


class Player:
    def __init__(self, level_damage: int, level_accuracy: int, level_health: int, hero: str, username: str,
                 rank: Union[int, str]):
        """
        :param level_damage: Уровень урона
        :param level_accuracy: Уровень точности
        :param level_health: Уровень HP
        :param hero: Имя героя: soldier; sniper; любой другой текст: demoman
        :param username: Имя пользователя
        :param rank: Очки или имя ранга
        """

        self._user_name = username
        self._rank = rank if type(rank) == str and is_rank(rank, RANKS) else rank_to_str(rank, RANKS) if type(
            rank) == int else 'Unknown'
        self._hero = Sniper if hero == 'sniper' else Soldier if hero == 'soldier' else Demoman

        self._hero.level_up_damage(self._hero, count_level=level_damage if level_damage > 1 else 1)
        self._hero.level_up_health(count_level=level_health if level_health > 1 else 1)
        self._hero.level_up_accuracy(count_level=level_accuracy if level_accuracy > 1 else 1)

    @property
    def rank(self) -> str:
        return self._rank


# Testing
if __name__ == '__main__':
    """ ОШИБКИ!!!!! """
    player = Player(1, 1, 1, 'soldier', 'dipy', 'Хомяк')
    print(player.rank)
