"""
Ponto de entrada da aplicação.

Escolhe a interface a executar com base nos argumentos da linha de comando:
    python main.py        → interface de terminal (CLI)
    python main.py --gui  → interface gráfica (Tkinter)

Sempre inicializa o banco de dados antes de lançar a interface.

Chama:
    infrastructure/database.py → criar_tabelas()
    ui/cli.py                  → executar()
    ui/gui.py                  → iniciar_gui()
"""
import sys


def main():
    """Inicializa o banco e lança a interface escolhida pelo argumento --gui."""
    criar_tabelas()

    if "--gui" in sys.argv:
        from ui.gui import iniciar_gui
        iniciar_gui()
    else:
        from ui.cli import executar
        executar()


if __name__ == "__main__":
    main()
