from characters import Sniper, Demoman, Soldier, TARGET_BODY, BaseCharacter
from constants import SIDE_NONE
from stats import Side


class Player:
    _side: Side = Side()

    def __init__(self, hero: str, l_damage: int = 0, l_accuracy: int = 0,
                 health: int = 0):
        """
        :param l_damage: Уровень урона
        :param l_accuracy: Уровень точности
        :param health: Уровень HP
        :param hero: Имя героя: soldier; sniper; любой другой текст: demoman
        """

        self._hero = Sniper() if hero == 'sniper' else Soldier() if hero == 'soldier' else Demoman()

        self._hero.level_up_damage(count_level=l_damage)
        self._hero.health.health = health
        self._hero.level_up_accuracy(count_level=l_accuracy)

    def step(self, side: str = SIDE_NONE):
        self._side.side = side

    def hit(self, player, target: str = TARGET_BODY) -> int:
        """
        При любом уроне срезает хапэшки у передаваемого в аргумент игрока

        :param player: Объект класса Player
        :param target: Цель (только для снайпера)
        :return: Нанесённый урон
        """
        damage = 0

        if isinstance(self._hero, Sniper):
            if self._hero.hit(target):
                if self._side == player.side:
                    damage = self._hero.get_and_nullify_damage()
                    player.hero.health.health -= damage
                else:
                    self._hero.get_and_nullify_damage()
                    if self._hero.hit(target):
                        damage = self._hero.get_and_nullify_damage()
                        player.hero.health.health -= damage
        elif isinstance(self._hero, (Soldier, Demoman)):
            if self._hero.hit():
                if self._side == player.side:
                    damage = self._hero.get_and_nullify_damage()
                    player.hero.health.health -= damage
                else:
                    self._hero.get_and_nullify_damage()
                    if self._hero.hit():
                        damage = self._hero.get_and_nullify_damage()
                        player.hero.health.health -= damage
            else:
                self._hero.hit_splash()
                damage = self._hero.get_and_nullify_damage()
                player.hero.health.health -= damage

        return damage

    @property
    def side(self) -> str:
        return self._side.side

    @side.setter
    def side(self, value: str):
        self.step(value)

    @property
    def hero(self) -> BaseCharacter:
        return self._hero

    @property
    def health(self):
        return self.hero.health
