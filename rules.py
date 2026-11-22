import random
from typing import List, NamedTuple, Optional, Tuple
try:
    from .board import HOME, LAST_TRACK, SAFE_SQUARES, START_SQUARE, TRACK_LEN, YARD, abs_square, on_track
    from .state import State
except ImportError:
    from board import HOME, LAST_TRACK, SAFE_SQUARES, START_SQUARE, TRACK_LEN, YARD, abs_square, on_track
    from state import State

class Move(NamedTuple):
    token: int
    dice: int
    src: int
    dst: int
    captured: Tuple[Tuple[int, int], ...] = ()

    @property
    def enters(self) -> bool:
        return self.src == YARD

    @property
    def finishes(self) -> bool:
        return self.dst == HOME

def tokens_on_square(state: State, square: int, exclude: Optional[int]=None):
    found = []
    for q in state.players:
        if q == exclude:
            continue
        for t, rel in enumerate(state.pos[q]):
            if on_track(rel) and (START_SQUARE[q] + rel) % TRACK_LEN == square:
                found.append((q, t))
    return found

def _has_block(state: State, square: int, mover: int) -> bool:
    if square in SAFE_SQUARES:
        return False
    counts = {}
    for q, _ in tokens_on_square(state, square, exclude=mover):
        counts[q] = counts.get(q, 0) + 1
    return any((c >= 2 for c in counts.values()))

def _path_blocked(state: State, player: int, src: int, dst: int) -> bool:
    for rel in range(src + 1, min(dst, LAST_TRACK) + 1):
        if _has_block(state, abs_square(player, rel), player):
            return True
    return False

def roll_dice(rng: Optional[random.Random]=None) -> int:
    return (rng or random).randint(1, 6)

def is_terminal(state: State) -> bool:
    return state.is_terminal()

def winner(state: State) -> Optional[int]:
    return state.winner()

def get_legal_moves(state: State, dice: int) -> List[Move]:
    if state.is_terminal():
        return []
    rules = state.rules
    if rules.three_sixes_forfeit and dice == 6 and (state.sixes >= 2):
        return []
    p = state.turn
    moves: List[Move] = []
    seen_src = set()
    for t, src in enumerate(state.pos[p]):
        if src == HOME or src in seen_src:
            continue
        if src == YARD:
            if dice != 6:
                continue
            dst = 0
        else:
            dst = src + dice
            if dst > HOME:
                if rules.exact_finish:
                    continue
                dst = HOME
        seen_src.add(src)
        if rules.blocks and _path_blocked(state, p, src, dst):
            continue
        captured = ()
        if on_track(dst):
            sq = abs_square(p, dst)
            if sq not in SAFE_SQUARES:
                captured = tuple(tokens_on_square(state, sq, exclude=p))
        moves.append(Move(t, dice, src, dst, captured))
    return moves

def _next_player(state: State) -> int:
    i = state.players.index(state.turn)
    return state.players[(i + 1) % len(state.players)]

def pass_turn(state: State) -> State:
    return state._replace(turn=_next_player(state), sixes=0)

def apply_move(state: State, move: Move) -> State:
    p = state.turn
    pos = [list(row) for row in state.pos]
    pos[p][move.token] = move.dst
    for q, t in move.captured:
        pos[q][t] = YARD
    new_pos = tuple((tuple(row) for row in pos))
    new_state = state._replace(pos=new_pos)
    if new_state.is_terminal():
        return new_state
    r = state.rules
    extra = move.dice == 6 and r.extra_turn_on_six or (bool(move.captured) and r.extra_turn_on_capture) or (move.finishes and r.extra_turn_on_home)
    if extra:
        sixes = state.sixes + 1 if move.dice == 6 else 0
        return new_state._replace(sixes=sixes)
    return new_state._replace(turn=_next_player(state), sixes=0)
