import os, sys
sys.path.insert(0, os.path.dirname(__file__))  # ensure local packages are importable

from tkinter import Tk
from data import config_repo
from ui.app import ModDockApp as App  # App is a tk.Frame

def main():
    root = Tk()
    root.title("ModDock Server Manager")

    # Load mods from single config
    mods = config_repo.get_mods()

    # Mount the app frame
    app = App(root, mods)
    app.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
