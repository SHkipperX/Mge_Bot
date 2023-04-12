"""
Если Python ниже версии 3.9, то будет ошибка,
но from __future__ import annotations решает эту проблему.

Можно использовать только BaseStat, но ведь код будет приятнее если
будет какое-то наименование классов
"""

from __future__ import annotations
from typing import Optional


class BaseStat:
    _value: int
    _percent: int | float
    _level: int = 0
    _max_level: int = None

    def __init__(self, value: Optional[int] = 0, percent: Optional[int | float] = 0, max_level: Optional[int] = None):
        self._start_value = value
        self._value = value
        self._percent = percent
        self._level = 1
        self._max_level = max_level

    def level_up(self, count_level: int = 1):
        if count_level <= 0:
            raise ValueError('count_level must not be zero')

        self._level += count_level

        for _ in range(count_level):
            self._value = self._value + int(self._start_value / 100 * self._percent)

        if self._max_level and self._level > self._max_level:
            level = self._level - self._max_level
            for _ in range(level):
                self._value = self._value - int(self._start_value / 100 * self._percent)
            print('maximum level')

    @property
    def percent(self) -> int | float:
        return self._percent

    @property
    def level(self) -> int:
        return self._level

    @property
    def value(self) -> int:
        return self._value


class Damage(BaseStat):
    def __init__(self, damage: Optional[int] = 0, percent: Optional[int | float] = 0, max_level: Optional[int] = None):
        super(Damage, self).__init__(value=damage, percent=percent, max_level=max_level)

    @property
    def damage(self) -> int:
        return self._value


class Accuracy(BaseStat):
    def __init__(self, accuracy: Optional[int] = 0, percent: Optional[int | float] = 0,
                 max_level: Optional[int] = None):
        super(Accuracy, self).__init__(value=accuracy, percent=percent, max_level=max_level)

    @property
    def accuracy(self) -> int:
        return self._value


class Health(BaseStat):
    def __init__(self, health: Optional[int] = 0, percent: Optional[int | float] = 0, max_level: Optional[int] = None):
        super(Health, self).__init__(value=health, percent=percent, max_level=max_level)

    @property
    def health(self) -> int:
        return self._value
