# -*- coding: utf-8 -*-

import random
import numpy as np

class SlotMachine:
    def __init__(self, rtp=0.95):
        self.rtp = rtp

    def play(self, bet_amount):          # 玩家下注金額
        is_win = random.random() < 0.2    # 20% chance to win
        if is_win:
            payout = bet_amount * random.choice([1.5, 2.0, 5.0, 10.0])   # payout multiplier
        else:
            payout = 0
        return is_win, payout


class Roulette:
    def __init__(self):
        # 0-36, European roulette (single zero)
        self.numbers = list(range(0, 37))
        self.red_numbers = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]

    def play(self, bet_amount, bet_type):
        # bet_type: "red_black" (1:1 payout) or "single_number" (35:1 payout)
        result = random.choice(self.numbers)

        if bet_type == "red_black":
            is_win = result in self.red_numbers
            payout = bet_amount * 2 if is_win else 0
        elif bet_type == "single_number":
            is_win = random.random() < (1/37)
            payout = bet_amount * 36 if is_win else 0
        else:
            is_win = False
            payout = 0

        return is_win, payout


class Blackjack:
    def __init__(self):
        self.deck = self._build_deck()

    def _build_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        deck = [r for r in ranks for s in suits]
        random.shuffle(deck)
        return deck

    def _card_value(self, card):
        if card in ['J', 'Q', 'K']:
            return 10
        elif card == 'A':
            return 11
        else:
            return int(card)

    def _hand_value(self, hand):
        value = sum(self._card_value(c) for c in hand)
        aces = hand.count('A')
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def _deal_card(self):
        if len(self.deck) < 10:
            self.deck = self._build_deck()
        return self.deck.pop()

    def play(self, bet_amount, ai_action_fn, persona_type, game_state, initial_balance):
        self.deck = self._build_deck()  # 每輪重新洗牌
        
        # Deal initial hands
        player_hand = [self._deal_card(), self._deal_card()]
        dealer_hand = [self._deal_card(), self._deal_card()]

        # Player's turn — AI decides hit or stand each time
        while True:
            player_value = self._hand_value(player_hand)

            if player_value == 21:
                break
            if player_value > 21:
                break

            action = ai_action_fn(
                persona_type  = persona_type,
                game_state    = game_state,
                initial_balance = initial_balance,
                player_hand   = player_hand,
                dealer_upcard = dealer_hand[0]
            )

            if action == "hit":
                player_hand.append(self._deal_card())
            else:
                break

        player_value = self._hand_value(player_hand)

        # Dealer's turn — dealer hits until 17+
        while self._hand_value(dealer_hand) < 17:
            dealer_hand.append(self._deal_card())

        dealer_value = self._hand_value(dealer_hand)

        # Determine outcome
        if player_value > 21:
            is_win = False
            payout = 0
        elif dealer_value > 21:
            is_win = True
            payout = bet_amount * 2
        elif player_value > dealer_value:
            is_win = True
            payout = bet_amount * 2
        elif player_value == dealer_value:
            is_win = False
            payout = bet_amount  # push — return bet
        else:
            is_win = False
            payout = 0

        return is_win, payout


def decide_bet(player_info):
    base_bet = 10

    if player_info["income_bracket"] == "Low":
        base_bet = 5
    elif player_info["income_bracket"] == "High":
        base_bet = 20

    if player_info["risk_tolerance"] == "High":
        bet = np.random.choice(
            [base_bet, base_bet * 2, base_bet * 5],
            p=[0.7, 0.2, 0.1]
        )
    else:
        bet = base_bet

    return bet