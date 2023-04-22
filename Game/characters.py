from typing import Optional, Tuple, Union

from stats import Damage, Accuracy, Health, Splash, CurDamage
from constants import TARGET_HEAD, TARGET_BODY


class BaseCharacter:
    def __init__(self, *,
                 damage_value: int = 0,
                 splash_damage_range: Optional[Tuple[float, float]] = None,
                 accuracy_value: int = 0,
                 health_value: int = 0,

                 max_level_damage: int = 10,
                 max_level_accuracy: int = 5,
                 max_level_health: int = 15,

                 percent_damage: Union[int, float] = 0,
                 percent_accuracy: Union[int, float] = 0,
                 percent_health: Union[int, float] = 0):
        self.damage = Damage(damage_value, percent_damage, max_level_damage)
        self.accuracy = Accuracy(accuracy_body=accuracy_value, percent=percent_accuracy, max_level=max_level_accuracy)
        self.health = Health(health_value, percent_health, max_level_health)
        self._splash = Splash(*splash_damage_range) if splash_damage_range else None

        self._current_damage = CurDamage()

    @property
    def cur_damage(self) -> CurDamage:
        return self._current_damage

    def hit(self):
        if self.accuracy.chance_body():
            self.cur_damage.add_damage(self.damage.damage)

    @property
    def splash(self) -> Tuple[float, float]:
        return self._splash.get_splash()

    def hit_splash(self):
        self.cur_damage.add_damage(int(self.damage.damage * self._splash.splash()))

    def level_up_damage(self, count_level: int = 1):
        self.damage.level_up(count_level)

    def level_up_accuracy(self, count_level: int = 1):
        self.accuracy.level_up(count_level)

    def level_up_health(self, count_level: int = 1):
        self.health.level_up(count_level)

    def set_cur_damage(self, damage: int):
        self._current_damage = damage

    def add_cur_damage(self, damage: int):
        self._current_damage += damage

    def sub_cur_damage(self, damage: int):
        self._current_damage -= damage

    def get_and_nullify_damage(self) -> int:
        res = self.cur_damage.damage
        self.cur_damage.set_damage()
        return res

    @property
    def level_damage(self) -> int:
        return self.damage.level

    @property
    def level_accuracy(self) -> int:
        return self.accuracy.level

    @property
    def level_health(self) -> int:
        return self.health.level


class Sniper(BaseCharacter):
    def __init__(self):
        super(Sniper, self).__init__(
            damage_value=50,
            percent_damage=10,

            accuracy_value=40,
            percent_accuracy=12,

            health_value=80,
            percent_health=8
        )
        self.accuracy.accuracy_head = 12

    def hit(self, target: str = TARGET_BODY):
        """
        :param target: Цель: body; head
        """
        if target == TARGET_BODY:
            BaseCharacter.hit(self)
        elif target == TARGET_HEAD:
            if self.accuracy.chance_head():
                self.cur_damage.add_damage(self.damage.damage * 2)


class Soldier(BaseCharacter):
    def __init__(self):
        super(Soldier, self).__init__(
            damage_value=80,
            splash_damage_range=(.2, .8),
            percent_damage=7.5,

            accuracy_value=30,
            percent_accuracy=6,

            health_value=130,
            percent_health=12
        )


class Demoman(BaseCharacter):
    def __init__(self):
        super(Demoman, self).__init__(
            damage_value=70,
            splash_damage_range=(.1, .5),
            percent_damage=10,

            accuracy_value=35,
            percent_accuracy=8,

            health_value=100,
            percent_health=15
        )
