import tkinter as tk


def displayScoreboard():
    root = tk.Tk()
    root.title("Final Scores")
    root.geometry("400x300")

    # This is a placeholder until I can figure out how to get the getPointsData here.
    for i in range(1, 11):
        label = tk.Label(root, text=str(i), font=("Arial", 24))
        label.pack()

    root.mainloop()


if __name__ == "__main__":
    displayScoreboard()
