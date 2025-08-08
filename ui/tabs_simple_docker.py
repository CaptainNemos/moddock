import tkinter as tk

class DockerTab(tk.Frame):
    def __init__(self, master, on_compose_action):
        super().__init__(master)
        tk.Label(self, text="Docker Control", font=("Arial", 12)).pack(pady=(10,0))
        frame = tk.Frame(self)
        frame.pack(pady=10)
        for label, action in [("Start","start"),("Stop","stop"),("Restart","restart")]:
            tk.Button(frame, text=label, command=lambda a=action: on_compose_action(a)).pack(side="left", padx=6)
        tk.Label(self, text="Make sure docker-compose.yml is in the app folder.", fg="#555").pack(pady=(6,0))
