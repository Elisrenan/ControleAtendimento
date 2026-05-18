import sys


def main():
    from infrastructure.database import criar_tabelas
    criar_tabelas()

    if "--gui" in sys.argv:
        from ui.gui import iniciar_gui
        iniciar_gui()
    else:
        from ui.cli import executar
        executar()


if __name__ == "__main__":
    main()
