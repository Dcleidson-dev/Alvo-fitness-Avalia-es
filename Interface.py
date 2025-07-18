#importação das bibliotecas que auxiliaram o app para a formatação da interface gráfica, tratamento dos dados no formato utf-8, tratamento das horas, suporte para os sistemas operacionais.
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import os
import unicodedata


#Função para padronizar nome
def padronizar_nome(nome):
    nome = nome.strip().lower()
    nome = unicodedata.normalize('NFD', nome)
    nome = nome.encode('ascii', 'ignore').decode('utf-8')
    nome = nome.replace(" ", "_")
    return nome

# Dicionário dos objetivos dos exercícios 
exercicios_objetivo = {
    "emagrecimento": [
        ("Esteira", 300),
        ("Bicicleta", 250),
        ("HIIT", 400),
        ("Circuito funcional", 350)
    ],
    "hipertrofia": [
        ("Musculação - Peito", 200),
        ("Musculação - Costas", 220),
        ("Musculação - Pernas", 250),
        ("Musculação - Bíceps/Tríceps", 180)
    ],
    "funcional": [
        ("Treinamento Funcional", 320),
        ("Pliometria", 280),
        ("Agilidade", 260),
        ("Core", 230)
    ]
}

metas_kcal = {
    "emagrecimento": 0,
    "hipertrofia": 56,
    "funcional": 12
}

#Função para clcular metas de emagreciemnto
def calcular_meta_emagrecimento(peso, altura):
    peso_ideal = 24.9 * (altura ** 2)
    if peso <= peso_ideal:
        return 0
    diferenca = peso - peso_ideal
    return round(diferenca * 7700, 2)

#Função para calcular Indice de Massa Corpórea (IMC)y
def calcular_imc(peso, altura):
    return round(peso / (altura ** 2), 2)

#Função para realizar a avaliação do IMC com uso de condicionais
def avaliar_imc(imc):
    if 0 < imc < 18.5:
        return "Abaixo do peso"
    elif 18.5 <= imc < 25:
        return "Peso normal"
    elif 25 <= imc < 30:
        return "Sobrepeso"
    elif 30<= imc < 35:
        return "Obesidade grau I"
    elif 35<= imc < 40:
        return "Obesidade grau II"
    else:
        return "Obesidade grau III"

#Função calcular gasto com uso lista, estrutura de decisão for e adicioanr elementos a lista
def calcular_gasto(exercicios, tempo_total, sexo):
    tempo_por_ex = tempo_total / len(exercicios)
    total = 0
    detalhes = []

    fator = 1.0 if sexo == "masculino" else 0.9

    for nome_ex, kcal_hora in exercicios:
        gasto = (kcal_hora / 60) * tempo_por_ex * fator
        total += gasto
        detalhes.append(f"{nome_ex}: {gasto:.2f} kcal em {tempo_por_ex:.0f} min")
    return round(total, 2), detalhes

#Função salvar treino com uso de arquivos com abertura no modo "a" para que os dados sejam salvos  em continuidade sem ser apagado na geração de outro relatorio, uso de estrutura de decisão for, salvando o arqeuivo com nome do aluno.
def salvar_treino(nome, imc, situacao, objetivo, tempo, gasto, detalhes):
    data = datetime.now().strftime("%Y-%m-%d")
    nome_padrao = padronizar_nome(nome)
    filename = f"{nome_padrao}.txt"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\n--- {data} ---\n")
        f.write(f"IMC: {imc}\n")
        f.write(f"Situação: {situacao}\n")
        f.write(f"Objetivo: {objetivo}\n")
        f.write(f"Tempo: {tempo} minutos\n")
        for d in detalhes:
            f.write(f"- {d}\n")
        f.write(f"Gasto calórico total: {gasto} kcal\n")
        f.write("-" * 40 + "\n")

#Funçao total_gasto com uso de arquivos com abertura no modo "r", uso de condicionais, salvando o arqeuivo com nome do aluno. 
def total_gasto(nome):
    nome_padrao = padronizar_nome(nome)
    filename = f"{nome_padrao}.txt"
    if not os.path.exists(filename):
        return 0

    total_kcal = 0
    with open(filename, "r", encoding="utf-8") as f:
        for linha in f:
            if "Gasto calórico total" in linha:
                valor = linha.split(":")[1].replace("kcal", "").strip()
                total_kcal += float(valor)
    return total_kcal


def contar_treinos(nome):
    nome_padrao = padronizar_nome(nome)
    filename = f"{nome_padrao}.txt"
    if not os.path.exists(filename):
        return 0

    count = 0
    with open(filename, "a", encoding="utf-8") as f:
        for linha in f:
            if "Gasto calórico total" in linha:
                count += 1
    return count

def estimar_meta(nome, objetivo, gasto, peso=None, altura=None):
    total_atual = total_gasto(nome)
    
    if objetivo == "emagrecimento":
        if peso is None or altura is None:
            return "🚫 Peso e altura necessários para cálculo da meta de emagrecimento."
        meta = calcular_meta_emagrecimento(peso, altura)
        if meta == 0:
            return "✅ Você já está no peso ideal ou abaixo!"
        restante = max(meta - total_atual, 0)
        if gasto <= 0:
            return "🚫 Não foi possível calcular a meta."
        dias = restante / gasto if gasto > 0 else 0
        return (f"🔥 Estimativa: {round(dias)} dias para atingir o peso ideal.\n"
                f"✅ Você já gastou {total_atual:.2f} kcal.\n"
                f"⏳ Falta gastar {restante:.2f} kcal para a meta.")

    elif objetivo == "hipertrofia":
        meta = metas_kcal[objetivo]
        total_treinos = contar_treinos(nome)
        restante = max(meta - total_treinos, 0)
        return (f"💪 Meta: 56 treinos.\n"
                f"✅ Você já completou {total_treinos} treinos.\n"
                f"⏳ Falta completar {restante} treinos.")

    elif objetivo == "funcional":
        meta = metas_kcal[objetivo]
        total_treinos = contar_treinos(nome)
        restante = max(meta - total_treinos, 0)
        return (f"🏃 Meta: 12 treinos.\n"
                f"✅ Você já completou {total_treinos} treinos.\n"
                f"⏳ Falta completar {restante} treinos.")

    return ""

def ler_historico(nome):
    nome_padrao = padronizar_nome(nome)
    filename = f"{nome_padrao}.txt"
    if not os.path.exists(filename):
        return None

    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

#Interface gráfica

#Uso de classe para a formatação da tela de apresentação da tela inicial da interface do App e formatação da tela com nome do app e sua area gráfica e introdução de label e botões com suas respectivas configurações; funções para abrir cadastro, abrir relatorio e voltar ao menu com o uso do SELF que instancia objeto para acessar variaveis que pertence a uma determianda classe
class AcademiaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Alvo Fitness Avaliações - Academia")
        self.geometry("450x500")
        self.resizable(False, False)

        # Menu inicial
        self.frame_menu = ttk.Frame(self)
        self.frame_menu.pack(pady=40)

        ttk.Label(self.frame_menu, text="📌 MENU", font=("Helvetica", 16, "bold")).pack(pady=10)

        ttk.Button(self.frame_menu, text="Registrar novo treino", width=25, command=self.abrir_cadastro).pack(pady=10)
        ttk.Button(self.frame_menu, text="Ver relatório do aluno", width=25, command=self.abrir_relatorio).pack(pady=10)
        ttk.Button(self.frame_menu, text="Sair", width=25, command=self.quit).pack(pady=10)

    def abrir_cadastro(self):
        self.frame_menu.pack_forget()
        self.cadastro_frame = CadastroFrame(self)
        self.cadastro_frame.pack(pady=10, padx=10)

    def abrir_relatorio(self):
        self.frame_menu.pack_forget()
        self.relatorio_frame = RelatorioFrame(self)
        self.relatorio_frame.pack(pady=10, padx=10)

    def voltar_menu(self, frame):
        frame.pack_forget()
        self.frame_menu.pack(pady=40)

#Uso de classe para a formatação da tela de apresentação da tela inicial da interface do App com nome do app e sua area gráfica e udo de label e botões com suas respectivas configurações; funções para abrir cadastro, abrir relatorio e voltar ao menu com o uso do SELF que instancia objeto para acessar variaveis que pertence a uma determianda classe
class CadastroFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

# Variáveis
        self.nome_var = tk.StringVar()
        self.sexo_var = tk.StringVar()
        self.peso_var = tk.StringVar()
        self.altura_var = tk.StringVar()
        self.objetivo_var = tk.StringVar()
        self.tempo_var = tk.StringVar()

        ttk.Label(self, text="Registrar Novo Treino", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self, text="Nome do aluno:").grid(row=1, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.nome_var, width=30).grid(row=1, column=1, pady=5)

        ttk.Label(self, text="Sexo (masculino/feminino):").grid(row=2, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.sexo_var, width=30).grid(row=2, column=1, pady=5)

        ttk.Label(self, text="Peso (kg):").grid(row=3, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.peso_var, width=30).grid(row=3, column=1, pady=5)

        ttk.Label(self, text="Altura (m):").grid(row=4, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.altura_var, width=30).grid(row=4, column=1, pady=5)

        ttk.Label(self, text="Objetivo (emagrecimento/hipertrofia/funcional):").grid(row=5, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.objetivo_var, width=30).grid(row=5, column=1, pady=5)

        ttk.Label(self, text="Tempo de treino (min):").grid(row=6, column=0, sticky="w")
        ttk.Entry(self, textvariable=self.tempo_var, width=30).grid(row=6, column=1, pady=5)

        ttk.Button(self, text="Registrar treino", command=self.registrar_treino).grid(row=7, column=0, columnspan=2, pady=15)
        ttk.Button(self, text="Voltar ao menu", command=lambda: parent.voltar_menu(self)).grid(row=8, column=0, columnspan=2)

        self.resultado_text = tk.Text(self, height=10, width=55, state="disabled", bg="#f0f0f0")
        self.resultado_text.grid(row=9, column=0, columnspan=2, pady=10)

    def registrar_treino(self):
        nome = self.nome_var.get().strip()
        sexo = self.sexo_var.get().strip().lower()
        peso_str = self.peso_var.get().replace(",", ".").strip()
        altura_str = self.altura_var.get().replace(",", ".").strip()
        objetivo = self.objetivo_var.get().strip().lower()
        tempo_str = self.tempo_var.get().strip()

# Validações das informações repassadas para o app, caso dados informados nao cadastrados seja fornecidos, informar erro.
        if not nome:
            messagebox.showerror("Erro", "Informe o nome do aluno.")
            return
        if sexo not in ["masculino", "feminino"]:
            messagebox.showerror("Erro", "Sexo deve ser 'masculino' ou 'feminino'.")
            return
        try:
            peso = float(peso_str)
        except ValueError:
            messagebox.showerror("Erro", "Peso inválido. Informe um número válido.")
            return
        try:
            altura = float(altura_str)
        except ValueError:
            messagebox.showerror("Erro", "Altura inválida. Informe um número válido.")
            return
        if objetivo not in exercicios_objetivo:
            messagebox.showerror("Erro", "Objetivo inválido. Use emagrecimento, hipertrofia ou funcional.")
            return
        try:
            tempo = float(tempo_str)
        except ValueError:
            messagebox.showerror("Erro", "Tempo inválido. Informe um número válido.")
            return

        imc = calcular_imc(peso, altura)
        situacao = avaliar_imc(imc)
        exercicios = exercicios_objetivo[objetivo]
        gasto, detalhes = calcular_gasto(exercicios, tempo, sexo)

        meta_text = estimar_meta(nome, objetivo, gasto, peso, altura)

        salvar_treino(nome, imc, situacao, objetivo, tempo, gasto, detalhes)

# Mostrar resultado com uso da estrutura de repetição for 
        texto = (f"✅ IMC: {imc}\n"
                 f"📌 Situação: {situacao}\n\n")

        for d in detalhes:
            texto += d + "\n"
        texto += f"\n🔥 Gasto calórico: {gasto} kcal\n\n"
        texto += meta_text + "\n"
        texto += "✔ Treino registrado com sucesso!"

        self.resultado_text.config(state="normal")
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.insert(tk.END, texto)
        self.resultado_text.config(state="disabled")

#Classe relatório com uso de d biblioteca tkinter que auxilia na geração do label e campo para usuário digitar suas informações como seu nome, gerar relatório, em conjunto funções para proporcionar o relatorio e mostrar o relatório em tela da interface gráfica e tratamento de erro caso o usuário digite dados que não foram cadaastrados
class RelatorioFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self, text="Relatório do Aluno", font=("Helvetica", 14, "bold")).pack(pady=10)

        self.nome_var = tk.StringVar()
        frame_entrada = ttk.Frame(self)
        frame_entrada.pack(pady=5)

        ttk.Label(frame_entrada, text="Nome do aluno:").pack(side="left")
        ttk.Entry(frame_entrada, textvariable=self.nome_var, width=30).pack(side="left", padx=5)
        ttk.Button(frame_entrada, text="Buscar", command=self.mostrar_relatorio).pack(side="left")

        self.text_relatorio = scrolledtext.ScrolledText(self, width=55, height=20, state="disabled")
        self.text_relatorio.pack(pady=10)

        ttk.Button(self, text="Voltar ao menu", command=lambda: parent.voltar_menu(self)).pack(pady=5)

    def mostrar_relatorio(self):
        nome = self.nome_var.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Informe o nome do aluno.")
            return
        texto = ler_historico(nome)
        if texto is None:
            texto = "Nenhum histórico encontrado."

        self.text_relatorio.config(state="normal")
        self.text_relatorio.delete(1.0, tk.END)
        self.text_relatorio.insert(tk.END, texto)
        self.text_relatorio.config(state="disabled")

#Importação dos dados e gerenciamento da interface do app
if __name__ == "__main__":
    app = AcademiaApp()
    app.mainloop()

