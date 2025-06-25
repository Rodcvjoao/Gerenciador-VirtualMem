import tkinter as t
import sys
import os
from pagemanager import PageManager
from ui_pagina_inicial import Tela_Inicial
from ui_pagina_configurar import Tela_Configurar
from ui_pagina_input import Tela_Input
from ui_pagina_simular import Tela_Simular

# Adiciona o diretório atual ao sys.path para importar os módulos corretamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class App(t.Tk):
    def __init__(self):
        super().__init__()

        self.title("GMV - Trabalho de Sistemas Operacionais")
        self.minsize(700,500)
        self.maxsize(700,500)
        self.configure(background= '#181f30')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.page_manager = PageManager(self) 

        self.page_manager.add_page(Tela_Inicial, "ui_pagina_inicial.py", controller=self.page_manager)
        self.page_manager.add_page(Tela_Configurar, "ui_pagina_configurar.py", controller=self.page_manager)
        self.page_manager.add_page(Tela_Input, "ui_pagina_input.py", controller= self.page_manager)
        self.page_manager.add_page(Tela_Simular, "ui_pagina_simular.py", controller=self.page_manager)

        self.page_manager.show_page("ui_pagina_inicial.py")

if __name__ == "__main__":
    app = App()
    app.mainloop()