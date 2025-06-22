import tkinter as t
from tkinter import ttk
from PIL import Image, ImageTk


class Tela_Simular(t.Frame):

    def __init__(self,parent_frame,controller):

        super().__init__(parent_frame)
        self.controller = controller

        # Fazer