from typing import Tuple

from random import random

from stats import Damage, Accuracy, Health

BODY: str = 'body'
HEAD: str = 'head'


class BaseCharacter:
    def __init__(self, *,
                 damage_value: int = 0,
                 accuracy_value: int = 0,
                 health_value: int = 0,

                 max_level_damage: int = None,
                 max_level_accuracy: int = None,
                 max_level_health: int = None,

                 percent_damage: int = 0,
                 percent_accuracy: int = 0,
                 percent_health: int = 0):
        self.damage = Damage(damage_value, percent_damage, max_level_damage)
        self.accuracy = Accuracy(accuracy_value, percent_accuracy, max_level_accuracy)
        self.health = Health(health_value, percent_health, max_level_health)

    def hit(self, target: str = BODY) -> Tuple[bool, int]:
        if target == BODY:
            return self.accuracy.get_chance_body(), self.damage.damage
        elif target == HEAD:
            return self.accuracy.get_chance_head(), self.damage.damage * 2
        else:
            raise ValueError('An invalid value was passed to the target parameter')

    def level_up(self, count_level: int = 1):
        self.damage.level_up(count_level)
        self.accuracy.level_up(count_level)
        self.health.level_up(count_level)

    @property
    def level_damage(self) -> int:
        return self.damage.level

    @property
    def level_accuracy(self) -> int:
        return self.accuracy.level

    @property
    def level_health(self) -> int:
        return self.health.level
