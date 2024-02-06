import tkinter as tk
import random

class ScoreboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scoreboard")

        self.generate_random_scores()
        self.setup_ui()

    def setup_ui(self):

        self.high_score_frame = tk.Frame(self.root)
        self.high_score_frame.pack(pady=10)

        self.scores_frame = tk.Frame(self.root)
        self.scores_frame.pack(pady=10)

        #probably wont keep this, probs will replace with homepage
        tk.Button(self.root, text="Refresh Scores", command=self.refresh_scores).pack(pady=10)

        self.display_scores()


    #this is a temporary placeholder for random scores
    def generate_random_scores(self):
        self.teams = {}
        for i in range(1, 11):
            team_name = f"Team {i}"
            team_score = random.randint(1, 100)
            self.teams[team_name] = team_score

    def display_scores(self):
        for widget in self.high_score_frame.winfo_children():
            widget.destroy()
        for widget in self.scores_frame.winfo_children():
            widget.destroy()

        #highest score
        highest_scoring_team = max(self.teams, key=self.teams.get)
        highest_score = self.teams[highest_scoring_team]
        tk.Label(self.high_score_frame, text=f"Top Score: {highest_scoring_team} - {highest_score}", font=("Arial", 16, "bold")).pack()

        #all scores
        for team, score in sorted(self.teams.items(), key=lambda item: item[1], reverse=True):
            tk.Label(self.scores_frame, text=f"{team} - {score}", font=("Arial", 12)).pack()

    def refresh_scores(self):
        self.generate_random_scores()
        self.display_scores()

    #Need to add a HOME button

root = tk.Tk()
app = ScoreboardApp(root)
root.mainloop()
