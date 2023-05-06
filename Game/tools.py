from typing import Dict, Union


def rank_to_str(rank: int, ranks: Dict[str, int]) -> str:
    if rank < ranks['Хомяк']:
        return 'Unknown'
    elif rank >= ranks['Король Сервера']:
        return 'Король Сервера'

    rank_list = list(ranks.items())
    for i, (key, val) in enumerate(rank_list):
        if rank in range(val, rank_list[i + 1][1] if i < len(rank_list) - 1 else val):
            return key


def is_rank(rank: Union[int, str], ranks: Dict[str, int]) -> bool:
    if type(rank) == int:
        rank = rank_to_str(rank, ranks)
    elif type(rank) not in [str, int]:
        return False

    if rank in list(ranks.keys()):
        return True
    return False
