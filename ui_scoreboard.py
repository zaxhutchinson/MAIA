import tkinter as tk
import ui_widgets as uiw


class ScoreboardFrame(tk.Frame):
    def __init__(
        self,
        teams_scores_dict,
        controller,
        ui_sim,
        sim,
        master=None
    ):
        """Sets window and frame information and calls function to build UI"""

        super().__init__(master)
        self.master = master
        self.teams_scores_dict = teams_scores_dict
        self.controller = controller
        self.sim = sim
        self.ui_sim = ui_sim

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

        self.build_ui()

    def build_ui(self):
        """Generates UI of scoreboard

        Sets score data, places labels,
        places home button
        """
        # This converts the dictionary to tuples
        teams_scores = [
            (team, details["total"])
            for team, details in self.teams_scores_dict.items()
        ]

        # Sort tuples in descending order
        self.teams_scores_sorted = sorted(
            teams_scores, key=lambda x: x[1], reverse=True
        )

        # Title
        title_label = uiw.uiLabel(
            master=self, text="Final Scores", font=("Arial", 16)
        )
        title_label.config(highlightthickness=0)
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Scores
        for index, (team, score) in enumerate(
            self.teams_scores_sorted, start=1
        ):
            team_label = uiw.uiLabel(
                master=self, text=f"{team}", font=("Arial", 14)
            )
            team_label.config(highlightthickness=0)
            score_label = uiw.uiLabel(
                master=self, text=f"{score}", font=("Arial", 14)
            )
            score_label.config(highlightthickness=0)
            team_label.grid(row=index, column=0, columnspan=2, sticky="w")
            score_label.grid(row=index, column=1, columnspan=2, sticky="e")

        home_button = uiw.uiButton(
            master=self, command=self.home_page, text="Home"
        )
        home_button.grid(row=index + 1, column=0)

    def home_page(self):
        """Shows homepage and destroys sim instance"""
        self.controller.show_frame("home_page")
        self.ui_sim.destroy()
