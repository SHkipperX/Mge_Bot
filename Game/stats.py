from __future__ import annotations
from typing import Optional, Tuple, Union

from random import random, triangular

from constants import SIDE_NONE, SIDE_LEFT, SIDE_RIGHT


class Side:
    def __init__(self, side: str = SIDE_NONE):
        self._side: str = side

    def side_get(self) -> str:
        return self._side

    def side_set(self, value: str):
        self._side = value

    def side_del(self):
        self._side = SIDE_NONE

    side = property(side_get, side_set, side_del)

    def __eq__(self, other: Side) -> bool:
        return self._side == other.side

    def __ne__(self, other: Side) -> bool:
        return self._side != other.side


class CurDamage:
    def __init__(self, damage: Optional[int] = 0):
        self._cur_damage = damage

    def set_damage(self, damage: Optional[int] = 0):
        self._cur_damage = damage

    def add_damage(self, damage: int):
        self._cur_damage += damage

    def sub_damage(self, damage: int):
        self._cur_damage -= damage

    @property
    def damage(self) -> int:
        return self._cur_damage

    def __str__(self) -> str:
        return str(self.damage)

    @damage.setter
    def damage(self, value):
        self._cur_damage = value


class BaseStat:
    _value: int
    _percent: Union[int, float]
    _level: int = 1
    _max_level: int = None

    def __init__(self, value: Optional[int] = 0, percent: Optional[Union[int, float]] = 0,
                 max_level: Optional[int] = None):
        self._start_value = value
        self._value = value
        self._percent = percent
        self._level = 1
        self._max_level = max_level

    def level_up(self, count_level: int = 1):
        if count_level <= 0:
            return

        self._level += count_level

        for _ in range(count_level):
            self._value = self._value + int(self._start_value / 100 * self._percent)

        if self._max_level and self._level > self._max_level:
            for _ in range(self._level - self._max_level):
                self._value = self._value - int(self._start_value / 100 * self._percent)
            self._level = self._max_level

    @property
    def percent(self) -> Union[int, float]:
        return self._percent

    @property
    def level(self) -> int:
        return self._level

    @property
    def value(self) -> int:
        return self._value

    def __add__(self, value: int):
        self._value += value

    def __sub__(self, value: int):
        self._value -= value


class Splash:
    def __init__(self,
                 splash_range: Tuple[float, float]):
        self._splash_range = splash_range

    def splash(self) -> float:
        """
        Returns a random floating point number from the range specified when the object was created
        """
        return round(triangular(*self._splash_range), 1)

    def get_splash(self) -> Tuple[float, float]:
        return self._splash_range


class Damage(BaseStat):
    def __init__(self, damage: int = 0, percent: Union[int, float] = 0, max_level: int = None):
        super(Damage, self).__init__(value=damage, percent=percent, max_level=max_level)

    @property
    def damage(self) -> int:
        return self._value


class Accuracy(BaseStat):
    def __init__(self, accuracy_body: int = 0, accuracy_head: Optional[int] = 0,
                 percent: Union[int, float] = 0, max_level: int = None):
        super(Accuracy, self).__init__(value=0, percent=percent, max_level=max_level)
        self._accuracy_head = accuracy_head
        self._accuracy_body = accuracy_body

    def level_up(self, count_level: int = 1):
        if count_level <= 0:
            return

        self._level += count_level

        for _ in range(count_level):
            self._accuracy_head = self._accuracy_head + self._percent
            self._accuracy_body = self._accuracy_body + self._percent

        if self._max_level and self._level > self._max_level:
            for _ in range(self._level - self._max_level):
                self._accuracy_head = self._accuracy_head - self._percent
                self._accuracy_body = self._accuracy_body - self._percent

    @property
    def accuracy_body(self) -> int:
        return self._accuracy_head

    @property
    def accuracy_head(self) -> int:
        return self._accuracy_head

    def chance_body(self) -> bool:
        return random() <= self._accuracy_body / 100

    def chance_head(self) -> bool:
        return random() <= self._accuracy_head / 100

    @accuracy_head.setter
    def accuracy_head(self, value):
        self._accuracy_head = value


class Health(BaseStat):
    def __init__(self, health: Optional[int] = 0, percent: Optional[Union[int, float]] = 0,
                 max_level: Optional[int] = None):
        super(Health, self).__init__(value=health, percent=percent, max_level=max_level)

    @property
    def health(self) -> int:
        return self._value

    @health.setter
    def health(self, value: int):
        self._value = value
