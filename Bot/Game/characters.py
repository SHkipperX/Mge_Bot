from typing import Optional, Tuple, Union

from Bot.Game.stats import Damage, Accuracy, Health, Splash, CurDamage
from Bot.Game.constants import TARGET_HEAD, TARGET_BODY, SNIPER_STATS, SNIPER_HEAD_ACCURACY, SOLDIER_STATS, DEMOMAN_STATS


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
        self._splash = Splash(splash_damage_range) if splash_damage_range else None

        self._current_damage = CurDamage()

    def hit(self, *args) -> bool:
        if self.accuracy.chance_body():
            self.cur_damage.add_damage(self.damage.damage)
            return True
        return False

    def hit_splash(self):
        self.cur_damage.add_damage(int(self.damage.damage * self._splash.splash()))

    def level_up_damage(self, count_level: int = 1):
        self.damage.level_up(count_level)

    def level_up_accuracy(self, count_level: int = 1):
        self.accuracy.level_up(count_level)

    def level_up_health(self, count_level: int = 1):
        self.health.level_up(count_level)

    def set_cur_damage(self, damage: int):
        self._current_damage.damage = damage

    def add_cur_damage(self, damage: int):
        self._current_damage.damage += damage

    def sub_cur_damage(self, damage: int):
        self._current_damage.damage -= damage

    def add_health(self, health: int):
        self.health.health += health

    def sub_health(self, health: int):
        self.health -= health

    def set_health(self, health: int = 0):
        self.health = health

    def get_and_nullify_damage(self) -> int:
        res = self.cur_damage.damage
        self.cur_damage.set_damage()
        return res

    def chance_body(self) -> bool:
        return self.accuracy.chance_body()

    @property
    def cur_damage(self) -> CurDamage:
        return self._current_damage

    @property
    def splash(self) -> Tuple[float, float]:
        return self._splash.get_splash()

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
        super(Sniper, self).__init__(**SNIPER_STATS)
        self.accuracy.accuracy_head = SNIPER_HEAD_ACCURACY

    def hit(self, target: str = TARGET_BODY):
        """
        :param target: Цель: body; head
        """
        if target == TARGET_BODY:
            return BaseCharacter.hit(self)
        elif target == TARGET_HEAD:
            if self.accuracy.chance_head():
                self.cur_damage.add_damage(self.damage.damage * 2)
                return True
        return False


class Soldier(BaseCharacter):
    def __init__(self):
        super(Soldier, self).__init__(**SOLDIER_STATS)


class Demoman(BaseCharacter):
    def __init__(self):
        super(Demoman, self).__init__(**DEMOMAN_STATS)
