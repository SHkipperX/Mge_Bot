from typing import Union

from characters import Sniper, Demoman, Soldier, TARGET_BODY, TARGET_HEAD, BaseCharacter
from constants import RANKS, SIDE_LEFT, SIDE_RIGHT
from tools import rank_to_str, is_rank


class Player:
    _side: str

    def __init__(self, hero: str, _id: int, rank: Union[int, str], l_damage: int = 0, l_accuracy: int = 0,
                 l_health: int = 0, ):
        """
        :param l_damage: Уровень урона
        :param l_accuracy: Уровень точности
        :param l_health: Уровень HP
        :param hero: Имя героя: soldier; sniper; любой другой текст: demoman
        :param _id: Идентификатор пользователя
        :param rank: Очки или имя ранга
        """

        self._user_id = _id
        self._rank = rank if type(rank) == str and is_rank(rank, RANKS) else rank_to_str(rank, RANKS) if type(
            rank) == int else 'Unknown'  # Возможно уберётся
        self._hero = Sniper() if hero == 'sniper' else Soldier() if hero == 'soldier' else Demoman()

        self._hero.level_up_damage(count_level=l_damage)
        self._hero.level_up_health(count_level=l_health)
        self._hero.level_up_accuracy(count_level=l_accuracy)

    def step_left(self):
        self._side = SIDE_LEFT

    def step_right(self):
        self._side = SIDE_RIGHT

    def hit(self, target: str = TARGET_BODY):
        pass

    @property
    def side(self) -> str:
        return self._side

    @property
    def rank(self) -> str:
        return self._rank

    @property
    def hero(self) -> BaseCharacter:
        return self._hero


def hit_enemy(player: Player):
    pass


# testing
if __name__ == '__main__':
    player_sn = Player('sniper', 231687, 400)
