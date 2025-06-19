import tkinter as t
from pagemanager import PageManager
from ui_pagina_inicial import Tela_Inicial
from ui_pagina_configurar import Tela_Configurar
from ui_pagina_input import Tela_Input
from ui_pagina_simular import Tela_Simular

class App(t.Tk): # Herda de tk.Tk

    def __init__(self):
        super().__init__()

        self.title("GMV - Trabalho de Sistemas Operacionais")
        self.minsize(700,500)
        self.maxsize(700,500)
        self.configure(background= '#181f30') # Fundo da janela principal

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Inicializa o gerenciador de páginas
        self.page_manager = PageManager(self) 

        # Adiciona as páginas ao gerenciador
        # Cada página recebe o 'self.page_manager' como seu 'controller'
        self.page_manager.add_page(Tela_Inicial, "ui_pagina_inicial.py", controller=self.page_manager)
        self.page_manager.add_page(Tela_Configurar, "ui_pagina_configurar.py", controller=self.page_manager)
        self.page_manager.add_page(Tela_Input, "ui_pagina_input.py", controller= self.page_manager)
        self.page_manager.add_page(Tela_Simular, "ui_pagina_simular.py", controller=self.page_manager)


        # Exibe a página inicial ao iniciar
        self.page_manager.show_page("ui_pagina_inicial.py")


# --- Execução da Aplicação ---
if __name__ == "__main__":
    app = App()
    app.mainloop()