from __future__ import annotations
from Game.characters import Sniper, Demoman, Soldier, TARGET_BODY, BaseCharacter
from Game.constants import SIDE_NONE
from Game.stats import Side


class Player:
    _side: Side = Side()
    _enemy: Player

    def __init__(self, _class: str, d_lvl: int = 1, a_lvl: int = 1, h_lvl: int = 1):
        """
        :param d_lvl: Уровень урона
        :param a_lvl: Уровень точности
        :param hp: Уровень HP
        :param _class: Имя героя: soldier; sniper; любой другой текст: demoman
        """
        self._hero = Sniper() if _class == 'sniper' else Soldier() if _class == 'solder' else Demoman()

        self._hero.level_up_damage(count_level=d_lvl-1)
        self._hero.level_up_health(count_level=h_lvl-1)
        #self._hero.health.health = hp
        self._hero.level_up_accuracy(count_level=a_lvl-1)

    def step(self, side: str = SIDE_NONE):
        self._side.side = side

    def hit(self, player: Player, side_shot: str, target: str = TARGET_BODY) -> int:
        assert player, side_shot
        """
        При любом уроне срезает хапэшки у передаваемого в аргумент игрока

        :param side_shot: Направление выстрела
        :param player: Объект класса Player
        :param target: Цель (только для снайпера)
        :return: Нанесённый урон
        """
        damage = 0
        is_hit = False

        if isinstance(self._hero, (Sniper)):
            if self._hero.hit(target):  # Если попал снайпер
                if player.side == side_shot:  # Если попал в сторону куда шагнул враг
                    damage = self._hero.get_and_nullify_damage()
                    player.hero.health.health -= damage
                else:  # Если не попал в сторону куда шагнул враг
                    self._hero.get_and_nullify_damage()
                    if self._hero.hit(target):
                        damage = self._hero.get_and_nullify_damage()
                        player.hero.health.health -= damage

        elif isinstance(self._hero, (Soldier, Demoman)):
            if self._hero.hit():
                if player.side == side_shot:
                    is_hit = True
                    damage = self._hero.get_and_nullify_damage()
                    player.hero.health.health -= damage
                else:
                    self._hero.get_and_nullify_damage()
                    if self._hero.hit():
                        is_hit = True
                        damage = self._hero.get_and_nullify_damage()
                        player.hero.health.health -= damage
            if not is_hit:  # Если не попал по противнику вообще
                self._hero.hit_splash()  # Расчёт сплэша
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
    def health(self) -> int:
        return self.hero.health.health
