import tkinter as tk
from tkinter import simpledialog, colorchooser, messagebox
import random


class MindMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mapa Mental")
        self.canvas = tk.Canvas(
            root, width=800, height=600, bg="#003366"
        )  # Azul escuro
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.nodes = []
        self.node_color = "lightblue"
        self.selected_node = None

        # Barra de ferramentas
        self.toolbar = tk.Frame(root)
        self.toolbar.pack(fill=tk.X)

        self.add_node_button = tk.Button(
            self.toolbar, text="Adicionar Nó", command=self.add_node
        )
        self.add_node_button.pack(side=tk.LEFT)

        self.color_button = tk.Button(
            self.toolbar, text="Selecionar Cor", command=self.choose_color
        )
        self.color_button.pack(side=tk.LEFT)

        self.remove_node_button = tk.Button(
            self.toolbar, text="Remover Nó", command=self.remove_node
        )
        self.remove_node_button.pack(side=tk.LEFT)

        self.create_node("Central", 400, 300)

        self.canvas.bind("<Button-1>", self.select_node)
        self.canvas.bind("<B1-Motion>", self.move_node)

    def create_node(self, text, x, y):
        node = self.canvas.create_oval(
            x - 50, y - 25, x + 50, y + 25, fill=self.node_color, tags="node"
        )
        text_id = self.canvas.create_text(
            x, y, text=text, tags="text", fill="black", font=("Helvetica", 10, "bold")
        )  # Texto em preto e negrito
        self.nodes.append((node, text_id))

    def add_node(self):
        text = simpledialog.askstring("Input", "Nome do Nó:")
        if text:
            if self.selected_node:
                # Posição relativa ao nó selecionado
                x1, y1, x2, y2 = self.canvas.coords(self.selected_node)
                x = (x1 + x2) / 2 + random.randint(
                    -100, 100
                )  # Adiciona um deslocamento aleatório
                y = (y1 + y2) / 2 + random.randint(-100, 100)
            else:
                # Posição padrão no centro da tela
                x, y = 400, 300

            self.create_node(text, x, y)

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.node_color = color

    def select_node(self, event):
        x, y = event.x, event.y
        overlapping = self.canvas.find_overlapping(x - 5, y - 5, x + 5, y + 5)

        for node_id in overlapping:
            if self.canvas.gettags(node_id) == ("node",):
                if self.selected_node:
                    self.canvas.itemconfig(self.selected_node, outline="", width=1)
                self.selected_node = node_id
                self.canvas.itemconfig(node_id, outline="red", width=2)
                return

        if self.selected_node:
            self.canvas.itemconfig(self.selected_node, outline="", width=1)
            self.selected_node = None

    def move_node(self, event):
        if self.selected_node:
            x, y = event.x, event.y
            self.canvas.coords(self.selected_node, x - 50, y - 25, x + 50, y + 25)
            text_id = (
                self.canvas.find_withtag(self.selected_node)[0] + 1
            )  # Assuming text is right after node
            self.canvas.coords(text_id, x, y)

    def remove_node(self):
        if self.selected_node:
            self.canvas.delete(self.selected_node)
            text_id = (
                self.canvas.find_withtag(self.selected_node)[0] + 1
            )  # Assuming text is right after node
            self.canvas.delete(text_id)
            self.selected_node = None
        else:
            messagebox.showinfo("Info", "Selecione um nó para remover.")


if __name__ == "__main__":
    root = tk.Tk()
    app = MindMapApp(root)
    root.mainloop()
