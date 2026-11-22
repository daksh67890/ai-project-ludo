from typing import NamedTuple, Optional, Tuple
try:
    from .board import HOME, YARD, TOKENS_PER_PLAYER, seats_for
except ImportError:
    from board import HOME, YARD, TOKENS_PER_PLAYER, seats_for

class Rules(NamedTuple):
    extra_turn_on_six: bool = True
    extra_turn_on_capture: bool = True
    extra_turn_on_home: bool = True
    three_sixes_forfeit: bool = True
    exact_finish: bool = True
    blocks: bool = False

class State(NamedTuple):
    pos: Tuple[Tuple[int, ...], ...]
    turn: int
    sixes: int
    players: Tuple[int, ...]
    rules: Rules

    def winner(self) -> Optional[int]:
        for p in self.players:
            if all((r == HOME for r in self.pos[p])):
                return p
        return None

    def is_terminal(self) -> bool:
        return self.winner() is not None

def new_game(num_players: int=2, rules: Optional[Rules]=None, first: int=0) -> State:
    players = seats_for(num_players)
    pos = tuple((tuple([YARD] * TOKENS_PER_PLAYER) for _ in range(4)))
    return State(pos=pos, turn=players[first], sixes=0, players=players, rules=rules or Rules())
