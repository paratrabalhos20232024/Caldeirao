import json
import random
import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Para carregar imagens

# Configuração do arquivo de estado
ARQUIVO_ESTADO = "estado.json"

# Perguntas do dia
perguntas = [
    "Como será meu dia hoje?",
    "O que devo focar hoje?",
    "Qual será meu humor do dia?"
]

# Ingredientes e seus efeitos
ingredientes = {
    "Pó de estrela": "Sorte",
    "Lágrima de fada": "Alegria",
    "Raiz de mandrágora": "Desafios",
    "Pó de lua": "Mistério",
    "Essência de sol": "Energia",
    "Gotas de sombra": "Cansaço"
}

# Função para carregar o estado do jogo
def carregar_estado():
    try:
        with open(ARQUIVO_ESTADO, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"ultima_jogada": None}

# Função para salvar o estado do jogo
def salvar_estado():
    estado = {"ultima_jogada": datetime.date.today().isoformat()}
    with open(ARQUIVO_ESTADO, "w") as file:
        json.dump(estado, file)

# Verifica se o jogador já jogou hoje
estado = carregar_estado()
ultima_jogada = estado.get("ultima_jogada")

if ultima_jogada == datetime.date.today().isoformat():
    messagebox.showinfo("Aviso", "⚠️ Você já fez uma pergunta hoje! Volte amanhã! ⚠️")
    exit()

# Inicia a interface gráfica
root = tk.Tk()
root.title("Caldeirão Mágico")
root.geometry("500x600")

# Escolhe uma pergunta do dia
pergunta = random.choice(perguntas)

# Lista de ingredientes escolhidos
ingredientes_escolhidos = []

# Função para adicionar ingrediente
def adicionar_ingrediente(ingrediente):
    if len(ingredientes_escolhidos) < 3:
        ingredientes_escolhidos.append(ingrediente)
        atualizar_interface()
    else:
        messagebox.showwarning("Limite atingido", "Você só pode escolher até 3 ingredientes!")

# Função para misturar ingredientes
def misturar():
    if not ingredientes_escolhidos:
        resultado_label.config(text="O dia será um mistério!")
    else:
        efeitos = [ingredientes[ing] for ing in ingredientes_escolhidos]
        resultado = " e ".join(efeitos)
        resultado_label.config(text=f"Resultado: {resultado}")
        salvar_estado()

# Função para atualizar a interface
def atualizar_interface():
    ingredientes_label.config(text=f"Escolhidos: {', '.join(ingredientes_escolhidos)}")

# Exibe a pergunta do dia
pergunta_label = tk.Label(root, text=f"Pergunta do dia:\n{pergunta}", font=("Arial", 14), wraplength=400)
pergunta_label.pack(pady=10)

# Exibe a imagem do caldeirão
imagem = Image.open("caldeirao.png")  # Troque pela imagem do caldeirão
imagem = imagem.resize((200, 200), Image.Resampling.LANCZOS)
imagem_tk = ImageTk.PhotoImage(imagem)
caldeirao_label = tk.Label(root, image=imagem_tk)
caldeirao_label.pack()

# Botões para selecionar ingredientes
for ingrediente in ingredientes.keys():
    btn = tk.Button(root, text=ingrediente, command=lambda ing=ingrediente: adicionar_ingrediente(ing))
    btn.pack(pady=5)

# Exibe os ingredientes escolhidos
ingredientes_label = tk.Label(root, text="Escolhidos: Nenhum", font=("Arial", 12))
ingredientes_label.pack(pady=10)

# Botão de misturar
misturar_btn = tk.Button(root, text="Misturar!", font=("Arial", 14), command=misturar, bg="purple", fg="white")
misturar_btn.pack(pady=20)

# Exibe o resultado
resultado_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
resultado_label.pack(pady=10)

# Inicia a interface
root.mainloop()
