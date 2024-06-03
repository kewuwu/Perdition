import json
import os
from game import Game
import card
from game_events import Observer
from functools import partial

START_OF_TURN_EVENT = "start-of-turn"
END_OF_TURN_EVENT = "end-of-turn"

def parse_vars(obj, game:Game, **kwargs):
    if isinstance(obj, str):
        for key, value in kwargs.items():
            if f"${{{key}}}" in obj:
                obj = value
                return obj
        var = obj[2:].replace("}", "")
        if var == 'current-player':
            return game.active_player
        elif var == 'soul-deck':
            return game.board.soul_deck
        return obj
    elif isinstance(obj, dict):
        return {key: parse_vars(value, game, **kwargs) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [parse_vars(item, game, **kwargs) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(parse_vars(item, game, **kwargs) for item in obj)
    elif isinstance(obj, set):
        return {parse_vars(item, game, **kwargs) for item in obj}
    else:
        return obj

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
    
        for effect_type in ['ceffect', 'reffect']:
            if 'passive' in card_dict.get(effect_type, {}):
                effect_type_passive_func = card_dict[effect_type]['passive']
                effect_event = effect_type_passive_func.pop('event')
                if effect_event == END_OF_TURN_EVENT:
                    game_event = game.end_of_turn_passive_game_event 
                elif effect_event == START_OF_TURN_EVENT:
                    game_event = game.start_of_turn_passive_game_event
                elif effect_event == 'soul_card_purchased':
                    game_event = game.game_events.soul_card_purchased
                else:
                    continue
                event_observer = Observer(partial(game.do_card_effect, effect_type_passive_func, c, effect_type))
                c.event_observers.append(event_observer)
                game_event.subscribe(event_observer)
        return c

def exec_from_dict(obj, game, **kwargs):
    obj = parse_vars(obj, game, **kwargs)
    return execute(game=game,obj=obj, **kwargs)

def execute(game:Game = None, obj=None, **kwargs):
    if not isinstance(obj, dict) and not isinstance(obj, list):
        return obj
    if 'action' in obj:
        return getattr(CardActions, obj['action'].upper())(game=game, obj={k: v for k,v in obj.items() if k != 'action'})
    for a in obj:
        if a.upper() in Functions.__dict__:
            next_obj = obj[a]
            if isinstance(next_obj, list):
                return getattr(Functions, a.upper())(game=game, *next_obj, **kwargs)
            else:
                return getattr(Functions, a.upper())(game=game, **next_obj, **kwargs)
    else:
        raise ValueError(f"Unknown base function {list(obj.keys())}")

class Functions:
    @staticmethod
    def IF(*args, game=None, **kwargs):
        if args and not(isinstance(args, list) or isinstance(args, tuple)):
            raise TypeError(f"IF function expected to receive a list [cond, true, false] or [cond, true]. got {type(args)}")
        if execute(game=game, obj=args[0], **kwargs):
            return execute(game=game, obj=args[1], **kwargs)
        if len(args) > 2:
            return execute(game=game, obj=args[2], **kwargs)
    
    @staticmethod
    def NOT(game=None, **kwargs):
        return not bool(execute(game=game, obj=kwargs))
    
    @staticmethod
    def WHERE(*args, game=None, **kwargs):
        for i in iterable:
            _, v = member_cond.items()
            [all(vv) for _, vv in v.items()]
    
    @staticmethod
    def GTE(game=None, **kwargs):
        pass

    @staticmethod
    def GT(game=None, **kwargs):
        pass

    @staticmethod
    def LTE(game=None, **kwargs):
        pass

    @staticmethod
    def LT(game=None, **kwargs):
        pass

    def EQUALS(*args, game=None, **kwargs):
        if not args:
            return True
        return all(execute(game, x, **kwargs) == execute(game, args[0], **kwargs) for x in args)

    def CARD_AT_INDEX(game=None, **kwargs):
        index = kwargs.get("index")
        deck = kwargs.get('deck')
        try:
            return deck[index]
        except Exception as err:
            print(str(err))
            return None

class CardActions:
    @staticmethod
    def PURCHASE(game:Game = None, **kwargs):
        game.active_player.purchased_souls_this_turn = [card.Card("", "", "", "", "")]
        print(**kwargs)

    @staticmethod
    def RECEIVE(game: Game=None, **kwargs):
        obj = kwargs['obj']
        amount = obj['amount']
        currency = obj['currency']
        target = kwargs.get("target", game.active_player)

        print(f"{target.player_article_text} receives {amount} {currency.replace('-', ' ')}")
        if currency == 'layer-currency':
            target.layer_currency += amount

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

    def PURGE(obj, **kwargs):
        pass

class Statuses:
    @staticmethod
    def IN_DEBT(player, **kwargs) -> bool:
        pass


if __name__ == "__main__":
    with open("cards.json", 'r') as fp:
        data = json.load(fp)

    exec_from_dict(data[0]['reffect']['passive'])