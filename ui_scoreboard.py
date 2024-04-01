import tkinter as tk


class ScoreboardFrame(tk.Frame):
    def __init__(self, teams_scores_dict, master=None):
        super().__init__(master)
        self.master = master
        self.teams_scores_dict = teams_scores_dict

        # self.geometry("1400x700")
        # self.minsize(width=1400, height=700)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_rowconfigure(8, weight=1)

        self.BuildUI()

    def BuildUI(self):
        # This converts the dictionary to tuples
        teams_scores = [
            (team, details["total"]) for team, details in self.teams_scores_dict.items()
        ]

        # Sort tuples in descending order
        self.teams_scores_sorted = sorted(
            teams_scores, key=lambda x: x[1], reverse=True
        )

        # Title
        title_label = tk.Label(self, text="Final Scores", font=("Arial", 16))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Scores
        for index, (team, score) in enumerate(self.teams_scores_sorted, start=1):
            team_label = tk.Label(self, text=f"{team}", font=("Arial", 14))
            score_label = tk.Label(self, text=f"{score}", font=("Arial", 14))
            team_label.grid(row=index, column=0, columnspan=2, sticky="w")
            score_label.grid(row=index, column=1, columnspan=2, sticky="e")
