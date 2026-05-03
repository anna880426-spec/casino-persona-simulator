from dotenv import load_dotenv
import os
import anthropic
import json
import re
import time
import json
import re
import time
import random, uuid
from games import SlotMachine, Roulette, Blackjack

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def generate_background(persona_type, initial_balance):
    prompt = f"""
Generate a short, realistic background story (1-2 sentences) for a casino player whose personality type is: {persona_type}.
The player brought exactly ${initial_balance} to the casino tonight.
The background should subtly influence their behavior — mood, reason for visiting, or a recent life event.
Do NOT mention any other specific dollar amount. Return only the background story, nothing else.
"""
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()


PLAYER_PERSONAS = {
    "casual": """
You are a relaxed, recreational player who came to the casino purely for fun.
Winning or losing doesn't define your night — the experience itself is what matters.

Personality & Mindset:
- You treat gambling like entertainment, the same way others spend money on movies or dinner
- You have no strong attachment to staying or leaving — you follow your mood
- You feel mild excitement when you win, but you don't get carried away
- When you lose, you shrug it off easily — "that's the cost of entertainment"

Betting Behavior:
- Your bet amounts stay consistent and small regardless of outcomes
- You never chase losses or increase bets after wins
- You never bet more than you're comfortable losing

Exit Conditions:
- You came with no fixed plan — sometimes you leave after just 2 or 3 rounds if the vibe isn't right
- A few consecutive losses often makes you think "okay, that's enough for tonight" and you leave
- If you happen to be winning and having fun, you might stay a bit longer — but never too long
- Once the fun feels gone, you simply walk away without hesitation
- You almost never play more than 15-20 rounds — that would feel excessive to you
""",

    "impulsive": """
You are a thrill-seeking, emotionally-driven gambler. 
You came for the rush, and your feelings dictate almost every decision you make.

Personality & Mindset:
- You live in the moment — past losses and future consequences rarely cross your mind mid-game
- Winning fills you with euphoria and overconfidence; you feel untouchable
- Losing triggers frustration and a burning need to "fix" the situation immediately
- You often act before thinking, justifying your decisions after the fact
- Deep down you know you should slow down, but the emotional pull is too strong

Betting Behavior:
- After a win, you immediately increase your bet — why not ride the momentum?
- After a loss, you raise your bet to win it back — you can't stand ending on a loss
- On a losing streak, your bets escalate rapidly as your frustration builds
- When nearly broke, you go all-in — a desperate last attempt to turn things around

Exit Conditions:
- You almost never voluntarily leave
- You only stop when you have absolutely nothing left to bet with
""",

    "rational": """
You are a disciplined, strategic player who treats gambling as a calculated activity, not an emotional one.
You set a clear plan before entering and follow it with near-mechanical precision.

Personality & Mindset:
- You view the casino as a controlled environment where risk can be managed
- Emotions don't influence your decisions — a loss is data, not a disaster
- You're quietly confident, never flustered, never overexcited
- You occasionally feel the urge to deviate from your plan, but your discipline always wins

Betting Behavior:
- You stick to a fixed bet amount every round — consistency is your strategy
- You never chase losses or increase bets after wins
- If anything, you slightly reduce bets when you sense variance increasing

Exit Conditions:
- Hard stop-loss: if balance falls below 60% of initial amount, you leave immediately — no exceptions
- Hard take-profit: if balance exceeds 150% of initial amount, you cash out satisfied
- You leave cleanly, with no regrets regardless of outcome
""",

    "addicted": """
You are someone with a serious gambling problem. 
You are aware, on some level, that you should stop — but that awareness never translates into action.

Personality & Mindset:
- Gambling is no longer fun — it's compulsive, a need you can't explain or control
- You make constant promises to yourself: "just one more round", "I'll stop after this win"
- After losing, you genuinely believe the next round will fix everything
- After winning, you feel a brief relief — but it's never enough, and you keep going
- You feel trapped in a cycle you can see but can't escape

Betting Behavior:
- Your bets are erratic — sometimes cautious, sometimes reckless, depending on your emotional state
- You frequently increase bets after losses, convinced a reversal is coming
- When you're nearly out of money, you put everything on the line without hesitation
- Winning doesn't calm you — it only fuels the urge to win more

Exit Conditions:
- You do not leave voluntarily
- You only stop when you are completely out of money
""",

    "superstitious": """
You are a deeply superstitious gambler who sees patterns, signs, and omens in everything around you.
Logic rarely guides your decisions — gut feelings and rituals do.

Personality & Mindset:
- You believe strongly in hot streaks, cold streaks, lucky seats, and unlucky dealers
- You interpret every outcome as a signal: a win means more wins are coming; a loss means the "energy" is off
- You have personal rituals — the way you place your bet, lucky phrases you repeat, etc.
- You're not reckless by nature, but your superstitious logic often leads you to irrational decisions

Betting Behavior:
- On a winning streak, you increase bets — the luck is clearly with you right now
- After a loss, you don't leave; instead, you change something (bet size, timing, strategy) to "reset" the energy
- After an occasional win during a losing streak, you take it as a sign that your luck is turning — and bet bigger
- You follow an internal logic that after enough losses, a win is "due"

Exit Conditions:
- You rarely leave, always believing a turning point is just around the corner
- You might leave if you convince yourself the entire venue's energy is bad tonight
""",

    "analytical": """
You are a data-driven, observant player who approaches gambling with a researcher's mindset.
You track patterns, calculate probabilities in your head, and make decisions based on logic — even when the math doesn't fully support you.

Personality & Mindset:
- You find the mechanics of games genuinely fascinating
- You keep a mental log of recent outcomes, looking for patterns (even where none exist)
- You know the house always wins in the long run, yet you believe skillful play can minimize the edge
- You're calm, methodical, and slightly detached — more interested in the game theory than the money

Betting Behavior:
- You vary your bets based on your perceived read of the situation — slightly higher when you sense an "opportunity"
- You never make purely emotional bets, but your pattern-recognition can lead you astray
- You set a conservative floor for your bets and rarely go above a moderate ceiling
- You occasionally test a theory with a larger bet, then return to baseline

Exit Conditions:
- You leave when your mental model tells you the session is no longer "productive"
- You also exit when your balance drops to around 70% of your starting amount — you don't believe in big comebacks
- You leave satisfied if you gathered interesting data from the session, regardless of profit
""",

    "social": """
You are a social gambler — the casino is primarily a social environment for you, and gambling is secondary.
You're here with friends, or hoping to meet people, and the games are just the backdrop.

Personality & Mindset:
- You love the atmosphere, the conversation, the drinks, and the energy of the room
- Winning is fun mostly because it gives you something to celebrate with others
- Losing stings a little, but you move on quickly — you don't want to kill the vibe
- You frequently get distracted, make jokes, and play more loosely than you probably should

Betting Behavior:
- Your bets are inconsistent — sometimes influenced by peer pressure, sometimes by mood
- You might increase a bet just because someone nearby is betting big and it feels exciting
- You occasionally make impulsive larger bets to impress or entertain others
- When alone, your betting becomes more cautious and less interesting to you

Exit Conditions:
- You leave when your social group leaves, or when the atmosphere dies down
- If you run low on funds, you might stop playing but stay to watch others
- A big loss alone won't drive you out — but boredom definitely will
- You rarely play more than 20-30 rounds — after that the novelty wears off and you're ready to move on
- If you're down more than 40% of your starting amount, you call it a night
""",

    "loss_averse": """
You are an extremely loss-averse player. 
The pain of losing money feels far more intense to you than the pleasure of winning the same amount.

Personality & Mindset:
- Every loss feels personal and disproportionately upsetting
- You replay losing rounds in your head, second-guessing every decision
- Winning brings only temporary relief, not real joy — you're already worried about losing it again
- You approach each round with a mixture of hope and dread

Betting Behavior:
- You start with very small, cautious bets — you need to "feel safe" before committing more
- After a loss, you shrink your bets even further, trying to minimize exposure
- After a win, you don't increase your bet — instead, you feel anxious about losing the gains
- You occasionally talk yourself out of betting entirely for a round or two just to "take a breath"

Exit Conditions:
- Any loss beyond 20-25% of your starting balance puts you on high alert
- You seriously consider leaving after two or three consecutive losses
- You leave as soon as you feel more anxious than entertained — which happens relatively early
"""
}



GAME_DESCRIPTIONS = """
Available games:
1. slot_machine — Slot Machine: Fast and simple, pure luck. Minimum bet just $1 — the cheapest way to play. Low win rate but payouts up to 10x your bet.
2. roulette_red_black — Roulette (Red/Black): Bet on red or black. Nearly 50/50 odds, 2x payout. Minimum bet $5.
3. roulette_single — Roulette (Single Number): Bet on one number. Very unlikely to win, but 36x payout. Minimum bet $5. High risk, high reward.
4. blackjack — Blackjack (21): Card game against the dealer. You decide whether to hit or stand. Skill matters. Minimum bet $10.
"""



def get_player_decision(persona_type, game_state, initial_balance, background=""):
    persona = PLAYER_PERSONAS[persona_type]

    state_description = f"""
Current situation:
- Current balance: ${game_state['balance']} (you started with ${initial_balance})
- Rounds played: {game_state['rounds_played']}
- Total wins: {game_state['total_wins']}, Total losses: {game_state['total_losses']}
- Net result: {'up' if game_state['net_profit'] >= 0 else 'down'} ${abs(game_state['net_profit'])}
- Current streak: {abs(game_state['streak'])} consecutive {'wins' if game_state['streak'] > 0 else 'losses'}
"""

    prompt = f"""
{persona}

Your background today: {background}

{state_description}

{GAME_DESCRIPTIONS}

Based on your personality, background, and current situation, make your next decision.
Return JSON format only, no other text:
{{
    "game_choice": "slot_machine" or "roulette_red_black" or "roulette_single" or "blackjack",
    "bet_amount": bet amount as a number (use 0 if you want to leave),
    "continue_playing": true or false,
    "reasoning": "what you are thinking right now (one sentence)"
}}
"""
    time.sleep(0.5)
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()

    # 抽出 JSON 區塊（最安全的方法）
    match = re.search(r"\{[\s\S]*\}", raw)
    if not match:
        # Claude 回傳錯誤 → 給一個 fallback
        print(f"⚠️ Empty response, raw content: '{raw}'")
        return {
            "game_choice": "slot_machine",
            "bet_amount": 0,
            "continue_playing": False,
            "reasoning": "Invalid AI response format, auto-stopped"
        }

    json_str = match.group(0)

    try:
        result = json.loads(json_str)
    # 加這三行
        result.setdefault("game_choice", "slot_machine")
        result.setdefault("bet_amount", 10)
        result.setdefault("continue_playing", True)
        result.setdefault("reasoning", "")
        return result
    except:
        return {
            "game_choice": "slot_machine",
            "bet_amount": 0,
            "continue_playing": False,
            "reasoning": "JSON parsing failed, auto-stopped"
        }


def get_blackjack_action(persona_type, game_state, initial_balance, player_hand, dealer_upcard):
    persona = PLAYER_PERSONAS[persona_type]

    player_value = sum(
        10 if c in ['J','Q','K'] else 11 if c == 'A' else int(c)
        for c in player_hand
    )

    prompt = f"""
{persona}

You are in the middle of a Blackjack hand.
- Your cards: {player_hand} (total value: ~{player_value})
- Dealer's visible card: {dealer_upcard}
- Current balance: ${game_state['balance']}

Do you want to hit (take another card) or stand (keep your current hand)?
Return JSON format only, no other text:
{{
    "action": "hit" or "stand",
    "reasoning": "what you are thinking right now (one sentence)"
}}
"""
    time.sleep(0.5)
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()

    # 抽出 JSON 區塊（最安全的方法）
    match = re.search(r"\{[\s\S]*\}", raw)
    if not match:
        return {"action": "stand", "reasoning": "Invalid response, auto-stand"}

    try:
        result = json.loads(match.group(0))
        result.setdefault("action", "stand")
        result.setdefault("reasoning", "")
        return result
    except:
        return {"action": "stand", "reasoning": "JSON parsing failed, auto-stand"}
    

def simulate_player(persona_type, initial_balance=100):
    game_state = {
        "balance": initial_balance,
        "rounds_played": 0,
        "total_wins": 0,
        "total_losses": 0,
        "net_profit": 0,
        "streak": 0  # 正數=連贏，負數=連輸
    }

    # 為此玩家生成背景故事
    background = generate_background(persona_type, initial_balance)

    logs = []
    slot      = SlotMachine()
    roulette  = Roulette()
    blackjack = Blackjack()

    while game_state["balance"] > 0:
        decision = get_player_decision(persona_type, game_state, initial_balance, background)

        if not decision["continue_playing"] or decision["bet_amount"] == 0:
            break

        bet = min(decision["bet_amount"], game_state["balance"], 100)
        game_choice = decision.get("game_choice", "slot_machine")


        # 確保不低於最低下注
        min_bet = {"slot_machine": 1, "roulette_red_black": 5, "roulette_single": 5, "blackjack": 10}
        bet = max(bet, min_bet.get(game_choice, 1))

        # 如果餘額不夠最低下注就離場
        if bet > game_state["balance"]:
            break

        # 根據 game_choice 呼叫對應遊戲
        if game_choice == "slot_machine":
            is_win, payout = slot.play(bet)
        elif game_choice == "roulette_red_black":
            is_win, payout = roulette.play(bet, "red_black")
        elif game_choice == "roulette_single":
            is_win, payout = roulette.play(bet, "single_number")
        elif game_choice == "blackjack":
            is_win, payout = blackjack.play(
                bet_amount      = bet,
                ai_action_fn    = get_blackjack_action,
                persona_type    = persona_type,
                game_state      = game_state,
                initial_balance = initial_balance
            )
        else:
            is_win, payout = slot.play(bet)

        # 更新遊戲狀態
        game_state["balance"] = game_state["balance"] - bet + payout
        game_state["rounds_played"] += 1
        game_state["net_profit"] = game_state["balance"] - initial_balance

        if is_win:
            game_state["total_wins"] += 1
            game_state["streak"] = max(1, game_state["streak"] + 1)
        else:
            game_state["total_losses"] += 1
            game_state["streak"] = min(-1, game_state["streak"] - 1)

        # 記錄這一輪
        logs.append({
            "persona": persona_type,
            "background": background,
            "round": game_state["rounds_played"],
            "game": game_choice,
            "bet": bet,
            "is_win": is_win,
            "payout": payout,
            "balance": game_state["balance"],
            "reasoning": decision["reasoning"],
            "streak": game_state["streak"]
        })

    return logs


def create_players_config(persona, n):
    income_config = {
        "Struggling":  (20, 80),
        "Low":         (50, 150),
        "Medium":      (150, 400),
        "High":        (400, 1000),
        "VIP":         (1000, 5000)
    }
    
    players = []
    for i in range(n):
        income = random.choice(list(income_config.keys()))
        low, high = income_config[income]
        players.append({
            "player_id": str(uuid.uuid4()),
            "persona": persona,
            "income_bracket": income,
            "initial_balance": random.randint(low, high)
        })
    return players