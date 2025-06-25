import tkinter as t
from tkinter import ttk, scrolledtext, messagebox
import io
import sys
import os

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
diretorio_pai = os.path.dirname(diretorio_atual)
sys.path.insert(0, diretorio_pai)

from main import executar_simulacao

class Tela_Simular(t.Frame):

    def __init__(self, parent_frame, controller):
        super().__init__(parent_frame)
        self.controller = controller
        self.configure(background='#181f30')

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Título
        label_titulo = t.Label(self, text="Resultado da Simulação", font=("monospace", 16, "bold"), bg='#181f30', fg='white')
        label_titulo.grid(row=0, column=0, pady=10, padx=10)

        # Área de texto para exibir a saída da simulação
        self.output_text = scrolledtext.ScrolledText(self, wrap=t.WORD, bg="black", fg="lime green", font=("monospace", 10))
        self.output_text.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        self.output_text.configure(state='disabled')

        t.Button(
            self,
            text="Fechar Simulação",
            height=2,
            width=20,
            fg="#FFFFFF",
            bg="#c1121f",
            font=("monospace", 10, "bold"),
            command=parent_frame.master.destroy, # Comando para fechar a janela principal
        ).grid(row=2, column=0, pady=(10, 20))

    def rodar_e_mostrar_simulacao(self, caminho_arquivo): # Adicionado o parâmetro
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()

        try:
            executar_simulacao(caminho_arquivo) # Passa o caminho para a função
            resultado = captured_output.getvalue()
        except Exception as e:
            resultado = f"Ocorreu um erro crítico durante a simulação:\n\n{e}"
            messagebox.showerror("Erro na Simulação", resultado)
        finally:
            sys.stdout = old_stdout

        self.output_text.configure(state='normal')
        self.output_text.delete('1.0', t.END)
        self.output_text.insert(t.END, resultado)
        self.output_text.configure(state='disabled')