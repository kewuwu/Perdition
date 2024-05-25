import json
import os
from game import Game
import card
from observer import Observer
from functools import partial

START_OF_TURN_EVENT = "start-of-turn"
END_OF_TURN_EVENT = "end-of-turn"

def parse_vars(var, game:Game):
    if var == 'current_player':
        return game.active_player

def parse_card_definition(card_dict, game: Game) -> card.Card:
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
        # return c
    
        for effect_type in ['ceffect', 'reffect']:
            if 'passive' in card_dict.get(effect_type, {}):
                effect_type_passive_func = card_dict[effect_type]['passive']
                effect_event = effect_type_passive_func.pop('event')
                if effect_event == END_OF_TURN_EVENT:
                    subject = game.end_of_turn_passive_subject 
                elif effect_event == START_OF_TURN_EVENT:
                    subject = game.start_of_turn_passive_subject
                c.event_observer = Observer(partial(exec_from_dict, effect_type_passive_func))
                subject.subscribe(c.event_observer)
        return c

def exec_from_dict(obj, subject, game):
    return execute(game=game,obj=obj)

def execute(game:Game = None, obj=None):
    if 'action' in obj:
        return getattr(CardActions, obj['action'].upper())(game=game, obj={k: v for k,v in obj.items() if k != 'action'})
    for a in obj:
        if a.upper() in Functions.__dict__:
            next_obj = obj[a]
            if isinstance(next_obj, list):
                return getattr(Functions, a.upper())(game=game, *next_obj)
            else:
                return getattr(Functions, a.upper())(game=game, **next_obj)
    else:
        raise ValueError(f"Unknown base function {list(obj.keys())}")

class Functions:
    @staticmethod
    def IF(*args, game=None, **kwargs):
        if args and not(isinstance(args, list) or isinstance(args, tuple)):
            raise TypeError(f"IF function expected to receive a list [cond, true, false] or [cond, true]. got {type(args)}")
        if execute(game=game, obj=args[0]):
            return execute(game=game, obj=args[1])
        if len(args) > 2:
            return execute(game=game, obj=args[2])
    
    @staticmethod
    def NOT(game=None, **kwargs):
        return not bool(execute(game=game, obj=kwargs))
    
    @staticmethod
    def WHERE(iterable, member_cond, **kwargs):
        for i in iterable:
            _, v = member_cond.items()
            [all(vv) for _, vv in v.items()]
    
    @staticmethod
    def GTE(a, b, **kwargs):
        pass

    @staticmethod
    def GT(a, b, **kwargs):
        pass

    @staticmethod
    def LTE(a, b, **kwargs):
        pass

    @staticmethod
    def LT(a, b, **kwargs):
        pass

class CardActions:
    @staticmethod
    def PURCHASE(game:Game = None, **kwargs):
        game.active_player.purchased_souls_this_turn = [card.Card("", "", "", "", "")]
        print(**kwargs)

    @staticmethod
    def RECEIVE(game=None, **kwargs):
        print("Receiving currency")
        pass

    @staticmethod
    def LOAN(target, give, in_exchange_for, expiry, **kwargs):
        pass

    @staticmethod
    def PUT(p_from, p_to, **kwargs):
        pass

    @staticmethod
    def CHOOSE(c_from, amount, **kwargs):
        pass

    @staticmethod
    def OWN(comparison, a, b, **kwargs) -> bool:
        pass

    @staticmethod
    def SKIP(action, target, duration, **kwargs):
        pass

    @staticmethod
    def DESTROY(obj, **kwargs):
        pass

    @staticmethod
    def IMMOLATE(obj, **kwargs):
        pass

    def HAS_PURCHASED(game: Game=None, **kwargs):
        if game.active_player.turn_actions['purchased_souls_this_turn']:
            return True
        return False

class Statuses:
    @staticmethod
    def IN_DEBT(player, **kwargs) -> bool:
        pass


if __name__ == "__main__":
    with open("cards.json", 'r') as fp:
        data = json.load(fp)

    exec_from_dict(data[0]['reffect']['passive'])