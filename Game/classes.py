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

    def hit(self, target: str = BODY) -> bool:
        if target == BODY:
            return self.accuracy.get_chance_body()
        elif target == HEAD:
            return self.accuracy.get_chance_head()
        else:
            raise ValueError('An invalid value was passed to the target parameter')
