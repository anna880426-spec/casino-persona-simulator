import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt   #   streamlit run app.py
import glob
import random



# ==============================
# Page Config
# ==============================
st.set_page_config(
    page_title="Casino Persona Quiz",
    page_icon="🎰",
    layout="wide"
)


st.markdown("""
<style>
[data-testid="column"]:nth-child(1) {
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# Load Dataset
# ==============================
@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")
    return df

df = load_data()

# ==============================
# Story Generator
# ==============================
def generate_story(age, gender, job, outfit, mood, reason):
    job_str = job if job else "professional"
    gender_str = "He" if gender == "Male" else "She" if gender == "Female" else "They"
    gender_str2 = "his" if gender == "Male" else "her" if gender == "Female" else "their"

    openings = [
        f"A {age}-year-old {job_str} pushed open the casino doors tonight.",
        f"Tonight's visitor: a {age}-year-old whose day job was {job_str}.",
        f"At {age}, working as a {job_str}, {gender_str.lower()} decided tonight was the night.",
        f"The {job_str} had been planning this for a while. At {age}, {gender_str.lower()} finally walked in.",
        f"{gender_str}'d just turned {age}. {gender_str} worked as a {job_str}. And tonight, {gender_str.lower()} chose the casino.",
        f"A {job_str} in {gender_str2} {age}s stepped through the entrance, eyes adjusting to the lights.",
        f"Not everyone walks into a casino with a plan. This {age}-year-old {job_str} was one of them.",
        f"{gender_str} was {age}, a {job_str} by day — but tonight was different.",
        f"The {job_str} checked {gender_str2} watch. {age} years old, and still chasing something.",
        f"For a {age}-year-old {job_str}, the casino felt like uncharted territory — or maybe a homecoming.",
    ]

    mood_lines = {
        "Happy": [
            f"{gender_str} was in a genuinely good mood — the kind that makes everything feel possible.",
            f"Something had gone right today, and {gender_str.lower()} was riding that feeling all the way here.",
            f"The smile hadn't left {gender_str2} face all evening. Tonight felt lucky.",
            f"{gender_str} hadn't felt this light in weeks. The casino seemed like the perfect place to celebrate.",
            f"Good days deserved good nights. {gender_str} was here to make the most of both.",
        ],
        "Stressed": [
            f"The week had been relentless. {gender_str} needed something — anything — to switch off.",
            f"Work had piled up, and {gender_str2} head was full. The casino noise felt almost soothing.",
            f"{gender_str} wasn't sure this was the best idea, but {gender_str.lower()} needed to be somewhere else tonight.",
            f"The stress had been building for days. {gender_str} figured a distraction was better than sitting at home.",
            f"There was a tension in {gender_str2} shoulders that hadn't gone away all week. Maybe tonight would help.",
        ],
        "Excited": [
            f"There was something electric in the air, and {gender_str} had felt it all day.",
            f"{gender_str} could barely sit still on the drive over. Tonight had a different kind of energy.",
            f"The anticipation had been building since morning. {gender_str} was practically buzzing walking in.",
            f"Some nights you just know. This was one of those nights for {gender_str2}.",
            f"{gender_str} had been looking forward to this all week. The excitement was hard to contain.",
        ],
        "Anxious": [
            f"{gender_str} wasn't sure why {gender_str.lower()} came. {gender_str2} hands were already a little cold.",
            f"The nerves hadn't settled since {gender_str.lower()} left home. {gender_str} second-guessed every step.",
            f"Part of {gender_str2} wanted to turn around. The other part kept walking toward the tables.",
            f"{gender_str} took a slow breath at the entrance. It didn't really help.",
            f"The lights and sounds hit {gender_str2} all at once. {gender_str} reminded {gender_str2}self to stay calm.",
        ],
        "Bored": [
            f"It wasn't really a plan — more like something to do on a night that had nothing else going on.",
            f"{gender_str} had scrolled through {gender_str2} phone for an hour before deciding to just go out.",
            f"Nothing on TV, no one to call. The casino was at least something different.",
            f"{gender_str} shrugged as {gender_str.lower()} walked in. Why not? It wasn't like {gender_str.lower()} had anywhere better to be.",
            f"Boredom had a way of leading people to interesting places. Tonight, it led {gender_str2} here.",
        ],
        "Celebrating": [
            f"Tonight was a celebration, and {gender_str} wanted somewhere that matched the energy.",
            f"Something good had happened — the kind of thing worth marking properly.",
            f"{gender_str} was in full celebration mode. The casino felt like the right stage for it.",
            f"The champagne had already happened. Now {gender_str.lower()} wanted to push the night a little further.",
            f"Not every win happens at a table. But {gender_str} was here to add one more to the night.",
        ],
        "Normal": [
            f"Nothing special had happened today. {gender_str} just felt like doing something a little different.",
            f"It was a regular evening and {gender_str} wanted to break the routine.",
            f"{gender_str} wasn't chasing anything in particular. Just a night out.",
            f"The day had been fine. Nothing more, nothing less. The casino was just a change of scenery.",
            f"{gender_str} felt steady, calm, neither up nor down. A good state to walk into a casino, really.",
        ],
    }

    reason_lines = {
        "Just for fun": [
            f"{gender_str} wasn't here to get rich. Just to have a good time and see what happened.",
            f"The whole point was to enjoy it — win or lose, it didn't really matter.",
            f"{gender_str} had budgeted for fun. That's what this was.",
            f"No pressure, no plan. Just {gender_str2} and the games.",
            f"{gender_str} treated it like any other entertainment — something to enjoy, not to obsess over.",
        ],
        "With friends": [
            f"{gender_str} hadn't even really wanted to come — but the group had decided, and here {gender_str.lower()} was.",
            f"The friends were somewhere nearby, probably already arguing over which table to hit first.",
            f"It was a group decision. {gender_str} just went along for the ride.",
            f"Honestly, the company mattered more than the games. {gender_str} was just here to be part of the night.",
            f"The group chat had been buzzing all week about this. {gender_str} was finally here.",
        ],
        "Want to win money": [
            f"{gender_str} had done the mental math. {gender_str} wasn't walking out without making something.",
            f"There was a number in {gender_str2} head — a target. {gender_str} wasn't leaving until {gender_str.lower()} hit it.",
            f"The plan was simple: win, leave, don't look back.",
            f"{gender_str} had been thinking about this all week. The potential payout felt very real.",
            f"This wasn't about fun. This was about walking out ahead.",
        ],
        "Need to escape": [
            f"The outside world could wait. {gender_str} just needed to be somewhere that wasn't real life.",
            f"Sometimes you need a place where nothing outside matters. This was that place.",
            f"{gender_str} wasn't running away — just pausing. At least, that's what {gender_str.lower()} told {gender_str2}self.",
            f"The noise and lights were almost comforting. A good way to drown everything else out.",
            f"{gender_str} didn't want to think about any of it tonight. The casino made that easy.",
        ],
        "Celebrating": [
            f"Tonight was about marking the moment — and {gender_str} wanted to do it somewhere that felt alive.",
            f"The occasion called for something memorable. {gender_str} figured this qualified.",
            f"A good reason to spend a little, risk a little, and enjoy the night.",
            f"{gender_str} was treating {gender_str2}self. {gender_str} had earned it.",
            f"Celebration had brought {gender_str2} here. Whatever happened next was just part of the story.",
        ],
        "First time": [
            f"{gender_str} had never done this before. Everything was new — the sounds, the people, the feeling.",
            f"First times are strange. {gender_str} wasn't sure what to expect, which was exactly why {gender_str.lower()} came.",
            f"{gender_str} looked around slowly, taking it all in. {gender_str2} first casino.",
            f"Everyone has a first time. This was {gender_str2}.",
            f"{gender_str} had always been curious. Tonight, curiosity won.",
        ],
        "Just broke up": [
            f"The breakup was fresh. {gender_str} needed somewhere loud enough to drown out the thoughts.",
            f"{gender_str} wasn't sad exactly. Just in that strange in-between space, looking for something to do with it.",
            f"Sitting at home wasn't an option tonight. The casino was at least a decision.",
            f"{gender_str} figured: if the night was going to be a loss anyway, might as well make it interesting.",
            f"Some people call friends after a breakup. {gender_str} came here instead.",
        ],
        "For vacation": [
            f"{gender_str} was on vacation and figured: why not? It was practically required.",
            f"The hotel was nearby, the night was young, and {gender_str.lower()} was in full tourist mode.",
            f"Vacation meant doing things you wouldn't normally do. This qualified.",
            f"{gender_str} had promised {gender_str2}self one casino night this trip. Tonight was it.",
            f"It wasn't home. It wasn't work. It was vacation, and {gender_str.lower()} was going to enjoy it.",
        ],
    }

    outfit_lines_with = [
        f"{gender_str} had put on {outfit} — whether for luck or just because it felt right, {gender_str.lower()} wasn't sure.",
        f"The {outfit} had been a deliberate choice. {gender_str} felt good in it.",
        f"Dressed in {outfit}, {gender_str.lower()} blended into the crowd just enough.",
        f"{gender_str} straightened {gender_str2} {outfit} at the entrance and walked in.",
        f"The {outfit} had seemed like the right call. {gender_str} hoped it was.",
    ]

    outfit_lines_without = [
        f"{gender_str} hadn't dressed up. Didn't feel the need to.",
        f"Just casual tonight — no fuss, no ceremony.",
        f"{gender_str} kept it simple. The outfit wasn't the point.",
    ]

    opening = random.choice(openings)
    mood_line = random.choice(mood_lines.get(mood, mood_lines["Normal"]))
    reason_line = random.choice(reason_lines.get(reason, reason_lines["Just for fun"]))
    outfit_line = random.choice(outfit_lines_with if outfit else outfit_lines_without)

    return f"{opening} {mood_line} {reason_line} {outfit_line}"


# ==============================
# Persona Info
# ==============================
persona_info = {
    "casual": {
        "emoji": "😊",
        "name": "The Casual Player",
        "color": "#2ecc71",
        "description": "You're here for the experience, not the money. You play conservatively, enjoy the atmosphere, and know when to walk away.",
        "traits": ["Low average bet", "Leaves early", "Not affected by losses", "Prefers low-risk games"],
        "risk_level": "🟢 Low Risk"
    },
    "impulsive": {
        "emoji": "🔥",
        "name": "The Impulsive Player",
        "color": "#e74c3c",
        "description": "Emotions drive every decision. You chase losses, go all-in when frustrated, and ride the highs of winning streaks.",
        "traits": ["High bets after losses", "Chases losses", "Emotionally driven", "Almost never leaves voluntarily"],
        "risk_level": "🔴 High Risk"
    },
    "rational": {
        "emoji": "🧠",
        "name": "The Rational Player",
        "color": "#3498db",
        "description": "You came with a plan and you'll stick to it. Stop-loss and take-profit rules guide every decision.",
        "traits": ["Fixed bet amounts", "Strict stop-loss rules", "Unaffected by streaks", "Leaves at planned thresholds"],
        "risk_level": "🟡 Moderate Risk"
    },
    "addicted": {
        "emoji": "😰",
        "name": "The Compulsive Player",
        "color": "#c0392b",
        "description": "You know you should stop, but you can't. Every loss feels like it's just one win away from being fixed.",
        "traits": ["Can't leave voluntarily", "Always 'one more round'", "Escalating bets", "Plays until broke"],
        "risk_level": "🔴 Very High Risk"
    },
    "loss_averse": {
        "emoji": "😟",
        "name": "The Loss Averse Player",
        "color": "#27ae60",
        "description": "Losing hurts more than winning feels good. You play with extreme caution and leave at the first sign of trouble.",
        "traits": ["Minimum bets only", "Leaves after small losses", "Very anxious when losing", "Rarely takes risks"],
        "risk_level": "🟢 Very Low Risk"
    },
    "analytical": {
        "emoji": "📊",
        "name": "The Analytical Player",
        "color": "#2980b9",
        "description": "You track patterns, calculate odds, and make data-driven decisions. You believe skill can beat the house.",
        "traits": ["Pattern tracking", "Prefers skill-based games", "Methodical betting", "Exits when model says so"],
        "risk_level": "🟡 Moderate Risk"
    },
    "social": {
        "emoji": "🎉",
        "name": "The Social Player",
        "color": "#e67e22",
        "description": "The casino is a social venue for you. Games are just the backdrop for conversations and good vibes.",
        "traits": ["Influenced by others", "Prefers lively tables", "Inconsistent bets", "Leaves when bored"],
        "risk_level": "🟠 Moderate-High Risk"
    },
    "superstitious": {
        "emoji": "🔮",
        "name": "The Superstitious Player",
        "color": "#8e44ad",
        "description": "Signs, omens, and rituals guide your play. You're always one round away from the universe delivering your win.",
        "traits": ["Ritual-based decisions", "Believes in streaks", "Rarely leaves", "High variance bets"],
        "risk_level": "🔴 High Risk"
    }
}

# ==============================
# Scoring Logic
# ==============================
def map_answers_to_persona(q1, q2, q3, q4, q5):
    scores = {p: 0 for p in persona_info.keys()}

    q1_map = {
        "🎉 Just have fun and enjoy the atmosphere": {"casual": 2, "social": 1},
        "💰 Win big and go home rich": {"impulsive": 2, "addicted": 1},
        "🧠 Test my strategy and see how it goes": {"rational": 1, "analytical": 2},
        "😮‍💨 Escape from stress and clear my head": {"impulsive": 1, "addicted": 2}
    }
    q2_map = {
        "😄 No big deal, that's part of the game": {"casual": 2},
        "😤 I need to win it back NOW": {"impulsive": 2, "addicted": 1},
        "📊 Check if I've hit my stop-loss limit": {"rational": 2},
        "😰 I'm starting to feel very anxious": {"loss_averse": 2}
    }
    q3_map = {
        "🏠 Cash out and go home happy": {"rational": 2, "casual": 1},
        "🔥 All in on the next round": {"impulsive": 2, "addicted": 1},
        "👀 Wait and observe before deciding": {"analytical": 2},
        "🎲 Spread across smaller bets": {"rational": 1, "analytical": 1}
    }
    q4_map = {
        "🚪 Pack up and leave": {"casual": 1, "rational": 2, "loss_averse": 1},
        "💳 Go to the ATM for more": {"addicted": 3},
        "🎯 Put everything on one last big bet": {"impulsive": 2, "addicted": 1},
        "🔢 Calculate if I can still recover": {"analytical": 2}
    }
    q5_map = {
        "⭐ I have a lucky feeling tonight": {"superstitious": 2},
        "📉 Just average, nothing special": {"casual": 1, "rational": 1},
        "🔮 The signs are all pointing to a big win": {"superstitious": 3},
        "🤷 Luck doesn't matter, skill does": {"analytical": 2, "rational": 1}
    }

    for q, q_map in [(q1, q1_map), (q2, q2_map), (q3, q3_map),
                     (q4, q4_map), (q5, q5_map)]:
        if q in q_map:
            for persona, score in q_map[q].items():
                scores[persona] += score

    return max(scores, key=scores.get), scores


# ==============================
# Get Random Player
# ==============================
def get_random_player(persona, df):
    persona_players = df[df['persona'] == persona]['player_id'].unique()
    selected_id = random.choice(persona_players)
    player_df = df[df['player_id'] == selected_id].copy()
    return player_df, selected_id


# ==============================
# App State
# ==============================
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'results' not in st.session_state:
    st.session_state.results = None

# ==============================
# Title
# ==============================
st.title("🎰 What's Your Casino Persona?")
st.markdown("*Based on behavioral patterns discovered from 360 AI-simulated casino players across 8 personality types.*")
st.markdown("---")

# ==============================
# Two Column Layout
# ==============================
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("👤 Tell us about yourself")

    with st.form("quiz_form"):
        age = st.number_input("Age", min_value=18, max_value=99, value=25, key="age_input")
        gender = st.selectbox("Gender", ["Male", "Female", "Non-binary / Other"])
        job = st.text_input("Occupation", placeholder="e.g. engineer, teacher...")
        budget = st.number_input("💵 Budget tonight ($)", min_value=20, max_value=5000, value=100, step=10)
        outfit = st.text_input("👗 What are you wearing?", placeholder="e.g. my lucky red jacket...")

        mood = st.selectbox("😊 How are you feeling tonight?",
                    ["Normal", "Happy", "Stressed", "Excited", "Anxious", "Bored", "Celebrating"],
                    key="mood_select")
        reason = st.selectbox("🎯 Why are you visiting?",
            ["Just for fun", "With friends", "Want to win money",
             "Need to escape", "Celebrating", "First time",
                    "Just broke up", "For vacation"],
                    key="reason_select")

        st.markdown("---")
        st.markdown("**🎲 Quick Questions**")

        q1 = st.selectbox("Q1. What are you here for tonight?",
            [None,
             "🎉 Just have fun and enjoy the atmosphere",
             "💰 Win big and go home rich",
             "🧠 Test my strategy and see how it goes",
             "😮‍💨 Escape from stress and clear my head"],
            format_func=lambda x: "Select an answer..." if x is None else x)

        q2 = st.selectbox("Q2. You've lost 3 rounds in a row. What do you do?",
            [None,
             "😄 No big deal, that's part of the game",
             "😤 I need to win it back NOW",
             "📊 Check if I've hit my stop-loss limit",
             "😰 I'm starting to feel very anxious"],
            format_func=lambda x: "Select an answer..." if x is None else x)

        q3 = st.selectbox("Q3. You just won and doubled your money. What's next?",
            [None,
             "🏠 Cash out and go home happy",
             "🔥 All in on the next round",
             "👀 Wait and observe before deciding",
             "🎲 Spread across smaller bets"],
            format_func=lambda x: "Select an answer..." if x is None else x)

        q4 = st.selectbox("Q4. You're almost out of money. What do you do?",
            [None,
             "🚪 Pack up and leave",
             "💳 Go to the ATM for more",
             "🎯 Put everything on one last big bet",
             "🔢 Calculate if I can still recover"],
            format_func=lambda x: "Select an answer..." if x is None else x)

        q5 = st.selectbox("Q5. How do you feel about luck tonight?",
            [None,
             "⭐ I have a lucky feeling tonight",
             "📉 Just average, nothing special",
             "🔮 The signs are all pointing to a big win",
             "🤷 Luck doesn't matter, skill does"],
            format_func=lambda x: "Select an answer..." if x is None else x)

        all_answered = all([q1, q2, q3, q4, q5])

  
        submitted = st.form_submit_button(
            "🎲 Reveal My Casino Persona",
            use_container_width=True
        )




    if submitted:
        if not all([q1, q2, q3, q4, q5]):
            st.error("⚠️ Please answer all 5 questions.")
        else:
            persona, scores = map_answers_to_persona(q1, q2, q3, q4, q5)
            player_df, player_id = get_random_player(persona, df)
            story = generate_story(age, gender, job, outfit, mood, reason)
            st.session_state.submitted = True
            st.session_state.results = {
                'persona': persona,
                'scores': scores,
                'player_df': player_df,
                'story': story,
                'budget': budget,
                'mood': mood,
                'reason': reason
            }

# ==============================
# Right Column — Results
# ==============================
with col_right:
    if st.session_state.submitted and st.session_state.results:
        results = st.session_state.results
        persona = results['persona']
        scores = results['scores']
        player_df = results['player_df']
        story = results['story']
        info = persona_info[persona]

        initial_balance = player_df['initial_balance'].iloc[0]
        final_balance = player_df['balance'].iloc[-1]
        net_profit = final_balance - initial_balance
        total_rounds = len(player_df)
        win_rate = player_df['is_win'].mean()

        # Persona Reveal
        st.balloons()
        st.markdown(f"## {info['emoji']} You are... **{info['name']}**")
        st.markdown(f"*{info['description']}*")
        st.markdown(f"**Risk Level:** {info['risk_level']}")

        # Traits
        for trait in info['traits']:
            st.markdown(f"- {trait}")

        st.markdown("---")

        # Story
        st.subheader("📖 Your Story Tonight")
        st.info(story)

        # Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Starting Budget", f"${initial_balance}")
        c2.metric("Final Balance", f"${final_balance:.0f}", f"{net_profit:+.0f}")
        c3.metric("Rounds Played", total_rounds)
        c4.metric("Win Rate", f"{win_rate*100:.0f}%")

        # Balance Chart
        st.subheader("💰 Balance Journey")
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(player_df['round'], player_df['balance'],
                color=info['color'], linewidth=2, marker='o', markersize=3)
        ax.axhline(y=initial_balance, color='gray', linestyle='--', alpha=0.5)
        ax.fill_between(player_df['round'], player_df['balance'], initial_balance,
                       where=player_df['balance'] >= initial_balance,
                       color='green', alpha=0.1)
        ax.fill_between(player_df['round'], player_df['balance'], initial_balance,
                       where=player_df['balance'] < initial_balance,
                       color='red', alpha=0.1)
        ax.set_xlabel('Round')
        ax.set_ylabel('Balance ($)')
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        st.pyplot(fig)

        # Round by Round
        st.subheader("🎲 Round by Round")
        display_df = player_df[['round', 'game', 'bet', 'is_win', 'balance', 'reasoning']].copy()
        display_df['result'] = display_df['is_win'].apply(lambda x: '✅ WIN' if x else '❌ LOSE')
        display_df = display_df[['round', 'game', 'bet', 'result', 'balance', 'reasoning']]
        display_df.columns = ['Round', 'Game', 'Bet ($)', 'Result', 'Balance ($)', 'Inner Thoughts']
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # Dataset Insights
        st.subheader("📊 What our data says")
        persona_stats = df[df['persona'] == persona].groupby('player_id').agg(
            win_rate=('is_win', 'mean'),
            total_rounds=('round', 'max'),
            final_balance=('balance', 'last'),
            initial_balance=('initial_balance', 'first')
        )
        persona_stats['net_profit_pct'] = (
            (persona_stats['final_balance'] - persona_stats['initial_balance']) /
            persona_stats['initial_balance'] * 100
        )

        d1, d2, d3 = st.columns(3)
        d1.metric("Avg Rounds", f"{persona_stats['total_rounds'].mean():.0f}")
        d2.metric("Avg Win Rate", f"{persona_stats['win_rate'].mean()*100:.0f}%")
        d3.metric("Avg Net Profit", f"{persona_stats['net_profit_pct'].mean():.0f}%")

        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.submitted = False
            st.session_state.results = None
            st.rerun()

    else:
        st.markdown("### 👈 Fill in your details and answer the questions to discover your casino persona!")
        st.markdown("")
        st.markdown("Based on **behavioral patterns** discovered from **360 AI-simulated casino players** across **8 personality types**, this quiz will reveal how you'd behave in a real casino.")
        st.markdown("")
        st.markdown("**What you'll discover:**")
        st.markdown("- 🎭 Your casino personality type")
        st.markdown("- 💰 How someone like you plays and bets")
        st.markdown("- 📊 Risk level and behavioral patterns")
        st.markdown("- 🎲 A real simulated game session from our dataset")