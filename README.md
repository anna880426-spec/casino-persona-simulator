# 🎰 Casino Persona Simulator

<br>

> **Can we identify psychological risk signals from language — before dangerous behavior even occurs?**

<br>

This project uses Claude AI to simulate 360 casino players across 8 personality types. Each agent makes real-time decisions and records their inner thoughts every round — giving us behavioral data, NLP signals, and psychology to analyze.

**[Try the interactive quiz](https://casino-persona-simulator-pnhaymasntf2th9fr6ffpr.streamlit.app/)** — discover your casino persona


---

##  Business Problem

How can casino operators and regulators identify at-risk players earlier — before the damage is done?


---

##  Business Value

| Description | Use Case |
|---|---|
**Early Risk Identification** — identify at-risk players and intervene before harm escalates | casino |
**No Real Data Needed** — a low-cost simulation tool for regulators and researchers | regulatory authority|
**Transferable Framework** — same pipeline applicable to finance and trading to monitor investors or transactors | fintech/finance |
**Educational Tool** — seeing someone with your own mindset go broke is more impactful than any warning label | eduation |

*Ironically, the casino industry itself may not be the most motivated adopter — but regulators, responsible gambling organizations, and mental health researchers might be.*

---

##  Key Findings

- **Words predict risk better than actions** — sentiment score and danger word rate were stronger classifier signals than bet size
- **Specific phrases = danger signals** — rounds containing phrases like *"losses row"* showed **3.46x higher bets** and **8.3x higher bankruptcy risk** within 3 rounds
- **Safe language = safe outcomes** — players using phrases like *"stop loss"* had a **0% bankruptcy rate** within 3 rounds
- **Discipline > luck** — Rational players survived the longest (avg 104 rounds) while losing only 21.7%

---

## 8 Persona Types

| Persona | Risk Level | Key Trait |
|---|---|---|
| 😊 Casual | 🟢 Low | Here for fun, leaves early |
| 😟 Loss Averse | 🟢 Very Low | Minimum bets, leaves at first loss |
| 🧠 Rational | 🟡 Moderate | Strict stop-loss and take-profit rules |
| 📊 Analytical | 🟡 Moderate | Pattern-tracking, skill-based games |
| 🎉 Social | 🟠 Moderate-High | Atmosphere-driven, inconsistent bets |
| 🔥 Impulsive | 🔴 High | Chases losses, emotionally driven |
| 🔮 Superstitious | 🔴 High | Ritual-based, rarely leaves |
| 😰 Addicted | 🔴 Very High | Plays until broke, can't stop |

---
## 🏗 Architecture

**Data Generation** → **Analysis** → **Application**

- `games.py` + `simulation.py` + `Generate_all.py` — LLM Agent Simulation
- `Analysis.ipynb` — Behavioral Analysis, NLP, Clustering, Random Forest
- `app.py` — Streamlit Interactive App


---

##  Project Structure

```
casino-persona-simulator/
├── app.py                 # Streamlit interactive app
├── games.py               # Casino game logic (Blackjack, Roulette, Slots)
├── simulation.py          # AI agent simulation engine
├── Generate_all.py        # Data generation pipeline
├── Analysis.ipynb         # Full analysis & findings
├── data.csv               # Simulated dataset (360 players, 20,000+ rounds)
└── requirements.txt       # Dependencies
```

---

## Limitations

- **Synthetic data** — all behavior is AI-generated; real human behavior is far more complex
- **Circular logic** — personas are defined by behavioral rules, so the classifier partially learns these rules rather than discovering novel patterns
- **Language gap** — NLP signals rely on verbalized reasoning, which isn't available in real-world settings
- **Sample size** — 360 simulated players is a starting point, not a statistically robust dataset
- **Overfitting** — Random Forest shows train-test gap (F1: 0.97 vs 0.80)

---

##  Future Work

- Validate behavioral patterns against real-world anonymized data
- Expand framework to financial trading and investment scenarios
- Build real-time risk monitoring system
- Increase persona diversity and prompt complexity

---

##  How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

Add your Anthropic API key to a `.env` file:
ANTHROPIC_API_KEY=your_key_here


---

##  Links

- **Live App:** [Casino Persona Simulator](https://casino-persona-simulator-pnhaymasntf2th9fr6ffpr.streamlit.app/)
- **Full Analysis on Githuib:** [View on GitHub](./Analysis.ipynb)
- **Full Analysis on Google Colab:** [Open in Colab](https://drive.google.com/file/d/10ddebGg0JPlrG-v_Km30-Hm-fULNL6bW/view?usp=sharing) 


---

##  Interactive App

A quiz-based Streamlit app where you answer 5 questions and discover your casino persona — based on behavioral patterns from 360 AI-simulated players.

**How it works:**

**Step 1 — Tell us about yourself**
Fill in your profile: age, gender, occupation, budget, outfit, mood, and reason for visiting.

![input_data.png](screenshots/input_data.png)

**Step 2 — Answer 5 behavioral questions**
- What are you here for tonight?
- You've lost 3 rounds in a row — what do you do?
- You just doubled your money — what's next?
- You're almost out of money — what do you do?
- How do you feel about luck tonight?

![question.png](screenshots/question.png)

**Step 3 — See your results**
- Your personalized story tonight

![persona_story.png](screenshots/persona_story.png)

- Balance journey chart

![journey.png](screenshots/journey.png)

- Your result

![game_result.png](screenshots/game_result.png)

- Your persona category

![personal.png](screenshots/personal.png)

- How someone just like you played — round by round with inner thoughts

![other_same_persona.png](screenshots/other_same_persona.png)


- Comparison - the bankruptcy rate and safest players ranking

![comparison.png](screenshots/comparison.png)


---

##  About

Built by a MDSI student at UTS as a learning side project.
Inspired by how companies use AI to simulate customer reactions — applied to human decision-making under pressure.
Connect with me on [LinkedIn](https://www.linkedin.com/in/albee-tsai)

*Still learning, still building — feedback always welcome!* 🙏
