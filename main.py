"""Ponto de entrada da aplicação.

Monta as dependências via ``container.criar_container`` e repassa os
serviços para a interface escolhida (CLI ou GUI). Nenhuma lógica de
negócio ou acesso a banco deve residir aqui.

Uso::

    python main.py          # interface de terminal (padrão)
    python main.py --gui    # interface gráfica (Tkinter)
"""

import sys

from config import DB_PATH
from container import criar_container


def main() -> None:
    """Inicializa o container de dependências e executa a interface selecionada.

    Verifica o argumento ``--gui`` em ``sys.argv`` para escolher entre
    a interface gráfica (Tkinter) e a interface de terminal (CLI).
    """
    pessoa_svc, atendimento_svc = criar_container(DB_PATH)

    if "--gui" in sys.argv:
        from ui.gui import iniciar_gui
        iniciar_gui(pessoa_svc, atendimento_svc)
    else:
        from ui.cli import executar
        executar(pessoa_svc, atendimento_svc)


if __name__ == "__main__":
    main()

