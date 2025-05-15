import tkinter as tk
from tkinter import messagebox
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import teams
import pandas as pd
import os

currentSeason = "2024-25"

def get_team_ids():
    all_teams = teams.get_teams()
    return {team['full_name']: team['id'] for team in all_teams}

team_ids = get_team_ids()

def get_Last7(team_name, season=currentSeason):
    if team_name not in team_ids:
        print(f"Invalid Team Name: {team_name}")
        return None
    team_id = team_ids[team_name]
    game_finder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id, season_nullable=season)
    games = game_finder.get_data_frames()[0]
    if games.empty:
        print(f"No games found for {team_name}")
        return None
    games['GAME_DATE'] = pd.to_datetime(games['GAME_DATE'])
    recent_games = games.sort_values('GAME_DATE', ascending=False).head(7)
    recent_games['PTS_ALLOWED'] = recent_games['PTS'] - recent_games['PLUS_MINUS']
    return recent_games

def calculate_averages(df):
    if df is None or df.empty:
        return None
    stat_cols = ['PTS', 'AST', 'BLK', 'FTA', 'FT_PCT', 'FG3A', 'FG3_PCT', 'TOV', 'OREB', 'DREB', 'PTS_ALLOWED']
    return df[stat_cols].mean().to_dict()

def calculate_custom_score(avg_stats):
    score = (
        0.25 * avg_stats['PTS'] + 0.15 * avg_stats['AST'] + 0.05 * avg_stats['BLK'] +
        0.15 * (avg_stats['FTA'] * avg_stats['FT_PCT']) +
        0.2 * (avg_stats['FG3A'] * avg_stats['FG3_PCT']) +
        0.1 * avg_stats['OREB'] + 0.075 * avg_stats['DREB'] -
        (0.2 * avg_stats['TOV'] + 0.75 * (avg_stats['PTS_ALLOWED'] - avg_stats['PTS']))
    )
    return round(score, 2)

def print_team_averages(team_name, averages):
    print(f"\n{team_name} - Last 7 Game Averages:")
    print("-" * 45)
    for stat, value in averages.items():
        print(f"{stat:<15}: {value:.2f}")
    print("-" * 45)

def predict_matchup(team1, team2):
    team1_avg = calculate_averages(get_Last7(team1))
    team2_avg = calculate_averages(get_Last7(team2))

    team1_score = calculate_custom_score(team1_avg) * 1.075
    team2_score = calculate_custom_score(team2_avg)

    print_team_averages(team1, team1_avg)
    print_team_averages(team2, team2_avg)

    print(f"{team1} score: {team1_score:.2f}")
    print(f"{team2} score: {team2_score:.2f}")
    print("---------------------------------------------")

    if team1_score >= team2_score:
        print(f"Predicted winner: {team1}")
        predicted_Score = ((team1_score) / (team2_score)) * ((team1_score) - team2_score)**(6/7)
    else:
        print(f"Predicted winner: {team2}")
        predicted_Score = ((team2_score) / (team1_score)) * ((team2_score) - (team1_score))**(6/7)

    print(f"Predicted Point Differential: {predicted_Score:.0f}")


'''---------------------------------------------------|GUI|------------------------------------------------------------'''
root = tk.Tk()
root.title("Select Home and Away Teams")

selected = []

def select_team(team_name, button):
    if team_name in selected:
        return

    if len(selected) == 0:
        selected.append(team_name)
        button.config(bg='lightblue', borderwidth=5, relief="solid", highlightbackground='lime', highlightthickness=.2)
    elif len(selected) == 1:
        selected.append(team_name)
        button.config(bg='lightcoral', borderwidth=5, relief="solid", highlightbackground='red', highlightthickness=.2)
        home, away = selected

        def delayed_action():
            messagebox.showinfo("Teams Selected", f"Home: {home}\nAway: {away}")
            root.destroy()
            predict_matchup(home, away)

        root.after(750, delayed_action)


teams_list = [
    "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", "Chicago Bulls",
    "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons",
    "Golden State Warriors", "Houston Rockets", "Indiana Pacers", "Los Angeles Clippers",
    "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat", "Milwaukee Bucks",
    "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks",
    "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns",
    "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors",
    "Utah Jazz", "Washington Wizards"
]

buttons_frame = tk.Frame(root)
buttons_frame.pack()

images = {}
btn_dict = {}

for index, team in enumerate(teams_list):
    logo_path = os.path.join("NBA Logos", f"{team}.png")
    if os.path.exists(logo_path):
        img = tk.PhotoImage(file=logo_path).subsample(10, 10)
    else:
        img = None
    images[team] = img

    row = index // 6  
    col = index % 6

    btn = tk.Button(
        buttons_frame,
        text=team,
        image=images[team],
        compound='top',
        font=("Helvetica", 9),  
        width=140,
        height=140,
        wraplength=120,
        justify='center',
        command=lambda t=team: select_team(t, btn_dict[t])
    )
    btn.grid(row=row, column=col, padx=5, pady=5)
    btn_dict[team] = btn


root.mainloop()
