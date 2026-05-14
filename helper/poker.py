from itertools import combinations
from helper.Deck import Deck

SUITS_EMOJI = {'Spades': '♠', 'Hearts': '♥', 'Clubs': '♣', 'Diamonds': '♦'}
VALUE_NAMES = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
HAND_NAMES = {
    9: 'Royal Flush', 8: 'Straight Flush', 7: 'Four of a Kind',
    6: 'Full House', 5: 'Flush', 4: 'Straight', 3: 'Three of a Kind',
    2: 'Two Pair', 1: 'One Pair', 0: 'High Card'
}


def card_display(card):
    val = VALUE_NAMES.get(card.value, str(card.value))
    suit = SUITS_EMOJI[card.suit]
    return f"[{val}{suit}]"


def _evaluate_five(cards):
    vals = sorted([14 if c.value == 1 else c.value for c in cards], reverse=True)
    suits = [c.suit for c in cards]

    is_flush = len(set(suits)) == 1
    is_straight = vals == list(range(vals[0], vals[0] - 5, -1))
    if not is_straight and sorted(vals) == [2, 3, 4, 5, 14]:
        is_straight = True
        vals = [5, 4, 3, 2, 1]

    counts = {}
    for v in vals:
        counts[v] = counts.get(v, 0) + 1
    freq = sorted(counts.values(), reverse=True)
    groups = sorted(counts.keys(), key=lambda v: (counts[v], v), reverse=True)

    if is_flush and is_straight:
        return (9, vals) if vals[0] == 14 else (8, vals)
    if freq[0] == 4:
        return (7, groups)
    if freq[:2] == [3, 2]:
        return (6, groups)
    if is_flush:
        return (5, vals)
    if is_straight:
        return (4, vals)
    if freq[0] == 3:
        return (3, groups)
    if freq[:2] == [2, 2]:
        return (2, groups)
    if freq[0] == 2:
        return (1, groups)
    return (0, vals)


def best_hand_from_seven(cards):
    best_score = None
    best_five = None
    for five in combinations(cards, 5):
        score = _evaluate_five(list(five))
        if best_score is None or score > best_score:
            best_score = score
            best_five = list(five)
    return best_score[0], best_score[1], best_five


class PokerGame:
    STARTING_CHIPS = 500
    SMALL_BLIND = 10
    BIG_BLIND = 20

    def __init__(self, host_id, host_name):
        self.host_id = host_id
        self.players = []
        self.names = {}
        self.deck = None
        self.hole_cards = {}
        self.community_cards = []
        self.pot = 0
        self.balances = {}
        self.round_bets = {}
        self.current_bet = 0
        self.folded = set()
        self.all_in = set()
        self.phase = 'lobby'
        self.dealer_idx = 0
        self.action_idx = 0
        self._round_acted = set()
        self.add_player(host_id, host_name)

    def add_player(self, user_id, display_name):
        if user_id in self.players:
            return False, "You're already in the game."
        if len(self.players) >= 8:
            return False, "Game is full (max 8 players)."
        self.players.append(user_id)
        self.names[user_id] = display_name
        self.balances[user_id] = self.STARTING_CHIPS
        return True, f"**{display_name}** joined the game!"

    def start_game(self, user_id):
        if user_id != self.host_id:
            return False, "Only the host can start the game."
        if len(self.players) < 2:
            return False, "Need at least 2 players to start."
        self._new_hand()
        return True, "Game started!"

    def _new_hand(self):
        self.deck = Deck()
        self.hole_cards = {}
        self.community_cards = []
        self.pot = 0
        self.round_bets = {p: 0 for p in self.players}
        self.current_bet = 0
        self.folded = set()
        self.all_in = set()
        self._round_acted = set()

        for pid in self.players:
            self.hole_cards[pid] = [self.deck.draw(), self.deck.draw()]

        n = len(self.players)
        sb_idx = (self.dealer_idx + 1) % n
        bb_idx = (self.dealer_idx + 2) % n
        self._post_blind(self.players[sb_idx], self.SMALL_BLIND)
        self._post_blind(self.players[bb_idx], self.BIG_BLIND)
        self.current_bet = self.BIG_BLIND
        self.action_idx = (bb_idx + 1) % n
        self.phase = 'pre-flop'

    def _post_blind(self, uid, amount):
        actual = min(amount, self.balances[uid])
        self.balances[uid] -= actual
        self.round_bets[uid] += actual
        self.pot += actual
        if self.balances[uid] == 0:
            self.all_in.add(uid)

    def active_players(self):
        return [p for p in self.players if p not in self.folded]

    def current_player(self):
        n = len(self.players)
        idx = self.action_idx % n
        for _ in range(n):
            pid = self.players[idx]
            if pid not in self.folded and pid not in self.all_in:
                return pid
            idx = (idx + 1) % n
        return None

    def _advance_turn(self):
        n = len(self.players)
        self.action_idx = (self.action_idx + 1) % n
        for _ in range(n):
            if self.players[self.action_idx] not in self.folded:
                break
            self.action_idx = (self.action_idx + 1) % n

    def do_fold(self, uid):
        if uid != self.current_player():
            return False, "It's not your turn."
        self.folded.add(uid)
        self._round_acted.add(uid)
        self._advance_turn()
        return True, f"**{self.names[uid]}** folded."

    def do_check(self, uid):
        if uid != self.current_player():
            return False, "It's not your turn."
        owed = self.current_bet - self.round_bets.get(uid, 0)
        if owed > 0:
            return False, f"You owe ${owed} — use `.call` or `.fold`."
        self._round_acted.add(uid)
        self._advance_turn()
        return True, f"**{self.names[uid]}** checked."

    def do_call(self, uid):
        if uid != self.current_player():
            return False, "It's not your turn."
        owed = self.current_bet - self.round_bets.get(uid, 0)
        if owed <= 0:
            return self.do_check(uid)
        actual = min(owed, self.balances[uid])
        self.balances[uid] -= actual
        self.round_bets[uid] += actual
        self.pot += actual
        if self.balances[uid] == 0:
            self.all_in.add(uid)
        self._round_acted.add(uid)
        self._advance_turn()
        return True, f"**{self.names[uid]}** called ${actual}."

    def do_raise(self, uid, raise_by):
        if uid != self.current_player():
            return False, "It's not your turn."
        if raise_by < self.BIG_BLIND:
            return False, f"Minimum raise is ${self.BIG_BLIND}."
        owed = self.current_bet - self.round_bets.get(uid, 0)
        total_needed = owed + raise_by
        if total_needed > self.balances[uid]:
            return False, f"Not enough chips (you have ${self.balances[uid]}). Use `.allin` to go all in."
        self.balances[uid] -= total_needed
        self.round_bets[uid] += total_needed
        self.pot += total_needed
        self.current_bet = self.round_bets[uid]
        if self.balances[uid] == 0:
            self.all_in.add(uid)
        self._round_acted = {uid}
        self._advance_turn()
        return True, f"**{self.names[uid]}** raised to ${self.current_bet}."

    def do_allin(self, uid):
        if uid != self.current_player():
            return False, "It's not your turn."
        amount = self.balances[uid]
        if amount == 0:
            return False, "You have no chips left."
        self.round_bets[uid] += amount
        self.pot += amount
        self.balances[uid] = 0
        self.all_in.add(uid)
        if self.round_bets[uid] > self.current_bet:
            self.current_bet = self.round_bets[uid]
            self._round_acted = {uid}
        else:
            self._round_acted.add(uid)
        self._advance_turn()
        return True, f"**{self.names[uid]}** is ALL IN for ${amount}!"

    def is_round_over(self):
        active = self.active_players()
        if len(active) <= 1:
            return True
        for pid in active:
            if pid not in self.all_in:
                if self.round_bets.get(pid, 0) < self.current_bet:
                    return False
                if pid not in self._round_acted:
                    return False
        return True

    def advance_phase(self):
        self.round_bets = {p: 0 for p in self.players}
        self.current_bet = 0
        self._round_acted = set()

        if len(self.active_players()) <= 1 or self.phase == 'river':
            self.phase = 'showdown'
            return False

        if self.phase == 'pre-flop':
            self.deck.draw()
            self.community_cards = [self.deck.draw(), self.deck.draw(), self.deck.draw()]
            self.phase = 'flop'
        elif self.phase == 'flop':
            self.deck.draw()
            self.community_cards.append(self.deck.draw())
            self.phase = 'turn'
        elif self.phase == 'turn':
            self.deck.draw()
            self.community_cards.append(self.deck.draw())
            self.phase = 'river'

        n = len(self.players)
        self.action_idx = (self.dealer_idx + 1) % n
        for _ in range(n):
            if self.players[self.action_idx] not in self.folded:
                break
            self.action_idx = (self.action_idx + 1) % n

        return True

    def resolve(self):
        active = self.active_players()
        hand_results = {}

        if len(active) == 1:
            winner = active[0]
            self.balances[winner] += self.pot
            self.pot = 0
            self.dealer_idx = (self.dealer_idx + 1) % len(self.players)
            self.phase = 'lobby'
            return [winner], hand_results

        for pid in active:
            seven = self.hole_cards[pid] + self.community_cards
            rank, tb, best_5 = best_hand_from_seven(seven)
            hand_results[pid] = (HAND_NAMES[rank], [card_display(c) for c in best_5], (rank, tb))

        best_score = max(v[2] for v in hand_results.values())
        winners = [pid for pid, v in hand_results.items() if v[2] == best_score]

        share = self.pot // len(winners)
        remainder = self.pot % len(winners)
        for pid in winners:
            self.balances[pid] += share
        self.balances[winners[0]] += remainder
        self.pot = 0

        self.dealer_idx = (self.dealer_idx + 1) % len(self.players)
        self.phase = 'lobby'
        return winners, hand_results
