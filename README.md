# 🎰 Casino Persona Simulator

> **Can we identify psychological risk signals from language — before dangerous behavior even occurs?**

This project uses Claude AI to simulate 360 casino players across 8 personality types. Each agent makes real-time decisions and records their inner thoughts every round — giving us behavioral data, NLP signals, and psychology to analyze.

🎮 **[Try the interactive quiz](https://casino-persona-simulator-pnhaymasntf2th9fr6ffpr.streamlit.app/)** — discover your casino persona

---

## 🎯 Business Problem

Traditional player monitoring only tracks behavior (bet size, frequency). By the time dangerous behavior appears, it's often too late.

> **Behavior tells you what players did. Language tells you what they're about to do.**

---

## 💡 Business Value

| | Use Case |
|---|---|
| 🎰 | **Early Risk Identification** — identify at-risk players and intervene before harm escalates |
| 🏛 | **No Real Data Needed** — a low-cost simulation tool for regulators and researchers |
| 💹 | **Transferable Framework** — same pipeline applicable to finance and trading |
| 📚 | **Educational Tool** — seeing someone with your own mindset go broke is more impactful than any warning label |

*Ironically, the casino industry itself may not be the most motivated adopter — but regulators, responsible gambling organizations, and mental health researchers might be.*

---

## 📊 Key Findings

- **Words predict risk better than actions** — sentiment score and danger word rate were stronger classifier signals than bet size
- **Specific phrases = danger signals** — rounds containing phrases like *"losses row"* showed **3.46x higher bets** and **8.3x higher bankruptcy risk** within 3 rounds
- **Safe language = safe outcomes** — players using phrases like *"stop loss"* had a **0% bankruptcy rate** within 3 rounds
- **Discipline > luck** — Rational players survived the longest (avg 104 rounds) while losing only 21.7%

---

## 🧠 8 Persona Types

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
