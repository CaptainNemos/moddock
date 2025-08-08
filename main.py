# Ensures imports work both in PyInstaller and when running from source.
import os, sys

# When running as a script from the moddock folder, make this dir importable
sys.path.append(os.path.dirname(__file__))

# When frozen by PyInstaller, ensure the temp bundle path is visible
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    sys.path.append(sys._MEIPASS)

from ui.app import ModDockApp

def main():
    app = ModDockApp()
    app.mainloop()

if __name__ == "__main__":
    main()
