import tkinter as t

class Tela_Simular(t.Frame):

    def __init__(self, parent_frame, controller):
        super().__init__(parent_frame)
        self.controller = controller
        self.configure(background='#181f30')

        #Fazer