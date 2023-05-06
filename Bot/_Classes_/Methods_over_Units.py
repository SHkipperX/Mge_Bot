from Bot.orm_connector.__all_models import *
from Bot._Classes_.data_characteristic import *


class Character_show_lvl:

    def __init__(self, data_units: User_Heros, param: str = None):
        self.data = data_units
        self.balance = self.data.credits
        self.param = param

    @staticmethod
    def show_sum_lvl(dt: User_Heros):
        sn_lvl = dt.sn_damage + dt.sn_health + dt.sn_accuracy
        so_lvl = dt.so_damage + dt.so_health + dt.so_accuracy
        de_lvl = dt.de_damage + dt.de_health + dt.de_accuracy
        return sn_lvl, so_lvl, de_lvl

    def show_lvl_Sniper(self) -> str:
        sn_damage_lvl = self.data.sn_damage
        sn_health_lvl = self.data.sn_health
        sn_accuracy_lvl = self.data.sn_accuracy
        damage = Sniper.Damage * (1 + sn_damage_lvl * Sniper.Dm_Percent) if sn_damage_lvl > 1 else Sniper.Damage
        health = Sniper.Health * (1 + sn_health_lvl * Sniper.Hp_Percent) if sn_health_lvl > 1 else Sniper.Health
        precent = Sniper.Acc_percent * sn_accuracy_lvl if sn_accuracy_lvl > 1 else (
            100 * Sniper.Accuracy_head, 100 * Sniper.Accuracy_body)
        if type(precent) is tuple:
            Head, Body = precent
        else:
            Head, Body = 100 * (Sniper.Accuracy_head + precent), 100 * (Sniper.Accuracy_body + precent)
        message = f'●Снайпер:\n' \
                  f'•Lvl урона: {sn_damage_lvl} | {damage:.1f}Ур\n' \
                  f'•Lvl здоровья: {sn_health_lvl} | {health:.1f}Hp\n' \
                  f'•Lvl точность: {sn_accuracy_lvl}\n' \
                  f'Шанс попадания:\n' \
                  f'В Голову -> 〚{Head:.1f}%〛| В Тело -> 〚{Body:.1f}%〛'
        return message

    def show_lvl_Solder(self) -> str:
        so_damage_lvl = self.data.so_damage
        so_health_lvl = self.data.so_health
        so_accuracy_lvl = self.data.so_accuracy

        damage = Solder.Damage * (1 + so_damage_lvl * Solder.Dm_Percent) if so_damage_lvl > 1 else Solder.Damage
        health = Solder.Health * (1 + so_health_lvl * Solder.Hp_Percent) if so_health_lvl > 1 else Solder.Health
        precent = 1 + Solder.Acc_percent * so_accuracy_lvl if so_accuracy_lvl > 1 else 1
        Body = 100 * (Solder.Accuracy_body * precent)

        message = f'🚀Солдат:\n' \
                  f'•Lvl урона: {so_damage_lvl} | {damage:.1f}Ур.\n' \
                  f'•Lvl здоровья: {so_health_lvl} | {health:.1f}Hp\n' \
                  f'•Lvl точности: {so_accuracy_lvl}\n' \
                  f'Шанс попадания -> 〚{Body:.1f}%〛'
        return message

    def show_lvl_Demoman(self) -> str:
        de_damage_lvl = self.data.de_damage
        de_health_lvl = self.data.de_health
        de_accuracy_lvl = self.data.de_accuracy

        damage = Demoman.Damage * (1 + de_damage_lvl * Demoman.Dm_Percent) if de_damage_lvl > 1 else Demoman.Damage
        health = Demoman.Health * (1 + de_health_lvl * Demoman.Hp_Percent) if de_health_lvl > 1 else Demoman.Health
        precent = 1 + Demoman.Acc_percent * de_accuracy_lvl if de_accuracy_lvl > 1 else 1
        Body = 100 * (Demoman.Accuracy_body * precent)

        message = f'🔥Подрывник:\n' \
                  f'•Lvl урона: {de_damage_lvl} | {damage:.1f}Ур.\n' \
                  f'•Lvl здоровья: {de_health_lvl}| {health:.1f}Хп\n' \
                  f'•Lvl точности: {de_accuracy_lvl}\n' \
                  f'Шанс попадания -> 〚{Body:.1f}%〛'
        return message


class Character_Up_lvl:
    def __init__(self, data_units: User_Heros, param: str = None):
        self.data = data_units
        self.balance = self.data.credits
        self.param = param

    def Lvl_Up_sniper(self) -> dict[str, User_Heros]:
        text = None
        if self.param == 'damage':
            lvl_damage = self.data.sn_damage
            cost = Cost_up.Damage * lvl_damage
            if (lvl_damage < Const_damage) and (cost <= self.balance):
                self.data.sn_damage += 1
                self.data.credits -= cost
            elif lvl_damage == Const_damage:
                text = f'Достигнут максимальный уровень: {Const_damage}lvl!'
            elif cost > self.balance:
                text = f'Текущих средств недостаточно для улучшения урона.\n' \
                       f' Не хватает ещё {cost - self.balance} из {cost}!'

        elif self.param == 'health':
            lvl_health = self.data.sn_health
            cost = Cost_up.Health * lvl_health
            if (lvl_health < Const_hp) and (cost <= self.balance):
                self.data.sn_health += 1
                self.data.credits -= cost
            elif lvl_health == Const_hp:
                text = f'Достигнут максимальный уровень: {Const_hp}lvl!'
            elif cost > self.balance:
                text = f'Текущих средств недостаточно для улучшения здоровья.\n' \
                       f'Не хватает ещё {cost - self.balance} из {cost}!'

        elif self.param == 'accuracy':
            lvl_accuracy = self.data.sn_accuracy
            cost = Cost_up.Accuracy * lvl_accuracy
            if (lvl_accuracy < Const_acc) and (cost <= self.balance):
                self.data.sn_accuracy += 1
                self.data.credits -= cost
            elif lvl_accuracy == Const_acc:
                text = f'Достигнут максимальный уровень: {Const_acc}lvl!'
            elif cost > self.balance:
                text = f'Текущих средств недостаточно для улучшения точности.\n' \
                       f' Не хватает ещё {cost - self.balance} из {cost}!'
        return dict(data=self.data, text=text)

    def Lvl_Up_solder(self) -> dict[str, User_Heros]:
        text = None
        if self.param == 'damage':
            lvl_damage = self.data.so_damage
            cost = Cost_up.Damage * lvl_damage
            if (lvl_damage < Const_damage) and (cost <= self.balance):
                self.data.so_damage += 1
                self.data.credits -= cost
            elif lvl_damage == Const_damage:
                text = f'Достигнут максимальный уровень: {Const_damage}lvl!'
            elif cost > self.balance:
                text = f'Текущих средств недостаточно для улучшения урона.\n' \
                       f' Не хватает ещё {cost - self.balance}₭ из {cost}₭!'

        elif self.param == 'health':
            lvl_health = self.data.so_health
            cost = Cost_up.Health * lvl_health
            if (lvl_health < Const_hp) and (cost <= self.balance):
                self.data.so_health += 1
                self.data.credits -= cost
            elif lvl_health == Const_hp:
                text = f'Достигнут максимальный уровень: {Const_hp}lvl!'
            elif cost > self.balance:
                text = f'Текущих средств недостаточно для улучшения здоровья.\n' \
                       f' Не хватает ещё {cost - self.balance}₭ из {cost}₭!'

        elif self.param == 'accuracy':
            lvl_accuracy = self.data.so_accuracy
            cost = Cost_up.Accuracy * lvl_accuracy
            if (lvl_accuracy < Const_acc) and (cost <= self.balance):
                self.data.so_accuracy += 1
                self.data.credits -= cost
            elif lvl_accuracy == Const_acc:
                text = f'Достигнут максимальный уровень: {Const_acc}lvl!'
            elif cost > self.balance:
                text = f'Текущих средств недостаточно для улучшения точности.\n' \
                       f' Не хватает ещё {cost - self.balance}₭ из {cost}₭!'
        return dict(data=self.data, text=text)

    def Lvl_Up_demoman(self) -> dict[str, User_Heros]:
        text = None
        if self.param == 'damage':
            lvl_damage = self.data.de_damage
            cost = Cost_up.Damage * lvl_damage
            if (lvl_damage < Const_damage) and (cost <= self.balance):
                self.data.de_damage += 1
                self.data.credits -= cost
            elif lvl_damage == Const_damage:
                text = f'Достигнут максимальный уровень: {Const_damage}lvl!'
            elif cost > self.balance:
                text = f'Текущих средств недостаточно для улучшения урона.\n' \
                       f' Не хватает ещё {cost - self.balance} из {cost}!'

        elif self.param == 'health':
            lvl_health = self.data.de_health
            cost = Cost_up.Health * lvl_health
            if (lvl_health < Const_hp) and (cost <= self.balance):
                self.data.de_health += 1
                self.data.credits -= cost
            elif lvl_health == Const_hp:
                text = f'Достигнут максимальный уровень: {Const_hp}lvl!'
            elif cost > self.balance:
                text = f'Текущих средств недостаточно для улучшения здоровья.\n' \
                       f' Не хватает ещё {cost - self.balance} из {cost}!'

        elif self.param == 'accuracy':
            lvl_accuracy = self.data.de_accuracy
            cost = Cost_up.Accuracy * lvl_accuracy
            if (lvl_accuracy < Const_acc) and (cost <= self.balance):
                self.data.de_accuracy += 1
                self.data.credits -= cost
            elif lvl_accuracy == Const_acc:
                text = f'Достигнут максимальный уровень: {Const_acc}lvl!'
            elif cost > self.balance:
                text = f'Текущих средств недостаточно для улучшения точности.\n' \
                       f' Не хватает ещё {cost - self.balance} из {cost}!'
        return dict(data=self.data, text=text)


class Get_stat:
    """Выдаёт статистику аользователя за конкретный класс"""

    def __init__(self, data_unit_stat: User_Stat):
        self.data = data_unit_stat
        self.damage: int
        self.hits: int
        self.shots: int
        self.games: int
        self.loses: int
        self.wins: int

    def Sniper_stat(self):
        self.damage = self.data.sn_damage
        self.hits = self.data.sn_hits
        self.shots = self.data.sn_shot
        self.games = self.data.sn_games
        self.loses = self.data.sn_loses
        self.wins = self.data.sn_wins

    def Solder_stat(self):
        self.damage = self.data.so_damage
        self.hits = self.data.so_hits
        self.shots = self.data.so_shot
        self.games = self.data.so_games
        self.loses = self.data.so_loses
        self.wins = self.data.so_wins

    def Demoman_stat(self):
        self.damage = self.data.de_damage
        self.hits = self.data.de_hits
        self.shots = self.data.de_shot
        self.games = self.data.de_games
        self.loses = self.data.de_loses
        self.wins = self.data.de_wins

    def get_message(self):
        prc_wins = f'{self.wins / self.games * 100:.2f}％' if self.wins != 0 else 0
        prc_loses = f'{self.loses / self.games * 100:.2f}％' if self.loses != 0 else 0
        prc_hits = f'{self.hits / self.shots * 100:.2f}％' if self.hits != 0 else 0
        # 「」
        message = f'Статистика @id за класс 『@class』:\n' \
                  f'Нанесено урона: 「{self.damage}」| Количество боёв: 「{self.games}」\n' \
                  f'Произведенно выстрелов: 「{self.shots}」| Попаданий 「{self.hits} ({prc_hits})」\n' \
                  f'Побед: 「{self.wins} ({prc_wins})」| Поражений: 「{self.loses} ({prc_loses})」'

        return message


class Update_stat:
    def __init__(self, data_unit_stat: User_Stat, data: dict):
        self.data = data_unit_stat
        print(data)
        self.damage = data['damage']
        self.games = data['games']
        self.shots = data['shots']
        self.hits = data['hits']
        self.wins = data['wins']
        self.loses = data['loses']

    def Update_sniper(self):
        self.data.sn_damage += self.damage
        self.data.sn_games += self.games
        self.data.sn_shot += self.shots
        self.data.sn_hits += self.hits
        self.data.sn_wins += self.wins
        self.data.sn_loses += self.loses
        return self.data

    def Update_solder(self):
        self.data.so_damage += self.damage
        self.data.so_games += self.games
        self.data.so_shot += self.shots
        self.data.so_hits += self.hits
        self.data.so_wins += self.wins
        self.data.so_loses += self.loses
        return self.data

    def Update_demoman(self):
        self.data.de_damage += self.damage
        self.data.de_games += self.games
        self.data.de_shot += self.shots
        self.data.de_hits += self.hits
        self.data.de_wins += self.wins
        self.data.de_loses += self.loses
        return self.data
