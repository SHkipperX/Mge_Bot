Const_damage, Const_hp, Const_acc = 10, 15, 5  # MAX LVLs


class Sniper:
    """Статы по умолчанию: Снайпер"""
    Damage = 50
    Dm_Percent = 0.10

    Health = 80
    Hp_Percent = 0.08

    Accuracy_head = 0.12
    Accuracy_body = 0.4
    Acc_percent = 0.08


class Solder:
    """Статы по умолчанию: Солдат"""
    Damage = 80
    Dm_Percent = 0.075

    Health = 130
    Hp_Percent = 0.12

    Accuracy_body = 0.3
    Acc_percent = 0.065


class Demoman:
    """Статы по умолчанию: Подрывник"""
    Damage = 70
    Dm_Percent = 0.10

    Health = 100
    Hp_Percent = 0.15

    Accuracy_body = 0.35
    Acc_percent = 0.08


class Cost_up:
    """для прокачки 1-ого уровня, далее {_lvl_} * Cost_up"""
    Damage = 50
    Health = 40
    Accuracy = 60
