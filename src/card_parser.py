import json
import os

import card


def parse_card_definition(card_dict) -> card.Card:
    card_name = " ".join([k.capitalize() if k.lower() != 'of' else k for k in card_dict['name'].split()])

    kwargs = {
        "front_png": card_dict['image_path'],
        'back_png': None,
        'name': card_name
    }

    card_types = {
        "soul": card.SoulCard,
        "player": card.PlayerCard,
        "daemon": card.DaemonCard,
        "divine_revelation": card.DivineRevelationCard,
        "layer_card": card.LayerCard
    }
    card_type = card_dict['type']
    card_id = int(os.path.split(card_dict['image_path'])[-1].split(".")[0])
    if card_type == 'soul':
        c = card.SoulCard(
            card_id, 
            **kwargs, 
            rarity=card_dict['rarity'], 
            sin=card_dict['sin'], 
            ceffect=card_dict.get("ceffect"), 
            reffect=card_dict.get("reffect"), 
            vp=card_dict['vp']
        )
        return c

def exec_from_dict(obj):
    return execute(**obj)
def execute(*args, **kwargs):
    if args is None and kwargs is None:
        return None
    elif 'action' in kwargs:
        return getattr(CardActions, kwargs['action'].upper())(**{k: v for k,v in kwargs.items() if k != 'action'})
    for a in kwargs:
        if a.upper() in Functions.__dict__:
            args = kwargs[a] if not isinstance(kwargs[a], dict) else []
            kwargs = kwargs[a] if isinstance(kwargs[a], dict) else {}
            return getattr(Functions, a.upper())(*args, **kwargs)
    else:
        raise ValueError(f"Unknown base function {list(kwargs.keys())}")
    
class Functions:
    @staticmethod
    def IF(condition=None, true=None, false=None):
        return execute(**true) if execute(**condition) else execute(**false)
    
    @staticmethod
    def NOT(*arg, **kwargs):
        return not bool(execute(*arg, **kwargs))
    
    @staticmethod
    def WHERE(iterable, member_cond):
        for i in iterable:
            _, v = member_cond.items()
            [all(vv) for _, vv in v.items()]
    
    @staticmethod
    def GTE(a, b):
        pass

    @staticmethod
    def GT(a, b):
        pass

    @staticmethod
    def LTE(a, b):
        pass

    @staticmethod
    def LT(a, b):
        pass

class CardActions:
    @staticmethod
    def PURCHASE(currency, amount, **kwargs):
        print(**kwargs)

    @staticmethod
    def RECEIVE(currency, amount, **kwargs):
        pass

    @staticmethod
    def LOAN(target, give, in_exchange_for, expiry):
        pass

    @staticmethod
    def PUT(p_from, p_to):
        pass

    @staticmethod
    def CHOOSE(c_from, amount):
        pass

    @staticmethod
    def OWN(comparison, a, b) -> bool:
        pass

    @staticmethod
    def SKIP(action, target, duration):
        pass

    @staticmethod
    def DESTROY(obj):
        pass

    @staticmethod
    def IMMOLATE(obj):
        pass

class Statuses:
    @staticmethod
    def IN_DEBT(player) -> bool:
        pass


if __name__ == "__main__":
    with open("cards.json", 'r') as fp:
        data = json.load(fp)

    exec_from_dict(data[0]['reffect']['passive'])