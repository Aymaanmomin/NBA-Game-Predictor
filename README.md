# 🏀 NBA Matchup Predictor

A Python-based desktop application using **Tkinter** and the **nba_api** that predicts the outcome of an NBA matchup based on the **last 7 games** of each team.

---

## 📌 Features

- Interactive GUI for selecting **Home** and **Away** teams (with team logos).
- Automatically pulls game data from the NBA API (`nba_api`) for the current season.
- Calculates and displays:
  - Key stat averages (PTS, AST, REB, etc.)
  - Predicted team scores
  - Predicted point differential
  - Projected winner

---

## 🚀 How It Works

1. Launch the GUI.
2. Click on two teams (first is **Home**, second is **Away**).
3. The app fetches each team's last 7 games.
4. Computes stat averages and a custom score based on weighted metrics.
5. Displays predictions in the terminal.

---

## 🛠 Tech Stack

- **Python 3**
- **Tkinter** (GUI)
- **nba_api** (NBA stats)
- **Pandas** (data analysis)

---

## 🖼 Requirements

- Python 3.8+
- [nba_api](https://pypi.org/project/nba-api/)
- `NBA Logos/` directory containing 140x140 PNG images named after team full names (e.g., `Boston Celtics.png`).

---

## 📦 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
