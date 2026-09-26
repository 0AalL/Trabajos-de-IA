import tkinter as tk

from interfaz import Aplicacion


# =========================================================
# MAIN
# =========================================================

def main():

    root = tk.Tk()

    app = Aplicacion(
        root
    )

    root.mainloop()


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":

    main()