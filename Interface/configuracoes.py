# page_manager.py
import tkinter as tk
from tkinter import ttk

class PageManager(tk.Frame):
    """
    Um gerenciador de páginas para aplicações Tkinter.

    Permite a criação e transição entre diferentes "páginas"
    (que são instâncias de tk.Frame ou subclasses),
    ocultando a página atual e exibindo a nova.
    """
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.grid(row=0, column=0, sticky="nsew") # Ocupa toda a janela principal
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self._pages = {}  # Dicionário para armazenar as instâncias das páginas
        self._current_page = None

    def add_page(self, page_class, page_name, *args, **kwargs):
        """
        Adiciona uma nova página ao gerenciador.

        Args:
            page_class (class): A classe da página (deve ser uma subclasse de tk.Frame).
            page_name (str): Um nome único para identificar esta página.
            *args, **kwargs: Argumentos passados para o construtor da página.
        """
        if page_name in self._pages:
            raise ValueError(f"A página '{page_name}' já existe.")

        # Criar a instância da página, passando o PageManager como "parent"
        page_instance = page_class(self, *args, **kwargs)
        page_instance.grid(row=0, column=0, sticky="nsew") # Todas as páginas ficam na mesma célula do grid
        page_instance.grid_remove() # Oculta a página por padrão

        self._pages[page_name] = page_instance
        return page_instance

    def show_page(self, page_name):
        """
        Exibe a página especificada e oculta a página atualmente visível.

        Args:
            page_name (str): O nome da página a ser exibida.
        """
        if page_name not in self._pages:
            raise ValueError(f"A página '{page_name}' não foi encontrada.")

        # Oculta a página atual, se houver
        if self._current_page is not None:
            self._current_page.grid_remove()

        # Exibe a nova página
        self._current_page = self._pages[page_name]
        self._current_page.grid() # Exibe a página

        # Opcional: Levantar a página para garantir que esteja no topo (útil em layouts complexos)
        self._current_page.tkraise()

    def get_page(self, page_name):
        """
        Retorna a instância de uma página pelo seu nome.

        Args:
            page_name (str): O nome da página.

        Returns:
            tk.Frame: A instância da página.
        """
        return self._pages.get(page_name)

    def get_current_page_name(self):
        """
        Retorna o nome da página atualmente visível.
        """
        for name, page in self._pages.items():
            if page == self._current_page:
                return name
        return None