import sys


def main():
    if "--gui" in sys.argv:
        from ui.gui import iniciar_gui
        iniciar_gui()
    else:
        from ui.cli import executar
        executar()


if __name__ == "__main__":
    main()
