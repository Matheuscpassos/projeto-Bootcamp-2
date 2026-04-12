"""
Gerenciador de Remédios — GUI v2.0
Requer: pip install customtkinter
"""

import datetime
import os
import customtkinter as ctk
from tkinter import messagebox

# ── Configuração do tema ───────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ARQUIVO = "lista.txt"

# ── Dados em memória ───────────────────────────────────────────────────────────
remedios = []   # lista de nomes
dosagens = []   # lista de dosagens formatadas
horarios = []   # lista de listas de horários


# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÕES DE VALIDAÇÃO (mesma lógica do notebook original)
# ══════════════════════════════════════════════════════════════════════════════

def validar_nome(nome: str) -> tuple[bool, str]:
    """Valida o nome do remédio. Retorna (ok, mensagem_de_erro)."""
    nome = nome.strip()
    if not nome:
        return False, "O nome não pode estar vazio."
    if any(c.isdigit() for c in nome):
        return False, "O nome não pode conter números."
    if nome.lower() in [r.lower() for r in remedios]:
        return False, f'"{nome}" já está cadastrado.'
    return True, ""


def formatar_dosagem(dose_str: str) -> tuple[bool, str]:
    """Valida e formata a dosagem. Retorna (ok, valor_formatado_ou_erro)."""
    dose_str = dose_str.strip()
    if not dose_str.isdigit():
        return False, "Digite apenas números inteiros para a dosagem."
    dose_int = int(dose_str)
    if dose_int <= 0:
        return False, "A dosagem deve ser maior que zero."
    if dose_int >= 1000:
        return True, f"{dose_int / 1000:.1f} g"
    return True, f"{dose_int} mg"


def validar_horario(hora: str) -> bool:
    """Valida se o horário está no formato HH:MM."""
    try:
        datetime.datetime.strptime(hora.strip(), "%H:%M")
        return True
    except ValueError:
        return False


# ══════════════════════════════════════════════════════════════════════════════
# FUNÇÕES DE PERSISTÊNCIA
# ══════════════════════════════════════════════════════════════════════════════

def salvar_tudo():
    """Reescreve lista.txt com todos os remédios em memória."""
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        for i in range(len(remedios)):
            f.write(f"Remédio: {remedios[i]}\n")
            f.write(f"Dosagem: {dosagens[i]}\n")
            f.write(f"Horários: {', '.join(horarios[i])}\n")
            f.write("\n")


def carregar_arquivo():
    """Carrega lista.txt para as listas em memória ao iniciar."""
    if not os.path.exists(ARQUIVO):
        return
    with open(ARQUIVO, encoding="utf-8") as f:
        bloco_nome = bloco_dose = bloco_hora = None
        for linha in f:
            linha = linha.strip()
            if linha.startswith("Remédio:"):
                bloco_nome = linha.replace("Remédio:", "").strip()
            elif linha.startswith("Dosagem:"):
                bloco_dose = linha.replace("Dosagem:", "").strip()
            elif linha.startswith("Horários:"):
                bloco_hora = [h.strip() for h in linha.replace("Horários:", "").split(",")]
            elif linha == "" and bloco_nome:
                remedios.append(bloco_nome)
                dosagens.append(bloco_dose or "—")
                horarios.append(bloco_hora or [])
                bloco_nome = bloco_dose = bloco_hora = None


# ══════════════════════════════════════════════════════════════════════════════
# JANELA PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Remédios")
        self.geometry("820x620")
        self.minsize(700, 500)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_body()
        self._build_status()
        self.atualizar_lista()

    # ── Header ────────────────────────────────────────────────────────────────
    def _build_header(self):
        header = ctk.CTkFrame(self, corner_radius=0, height=60,
                              fg_color=("#1a5fa8", "#0d3d6e"))
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="💊  Gerenciador de Remédios",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="white"
        ).grid(row=0, column=0, pady=12, padx=20, sticky="w")

    # ── Corpo principal (esquerda + direita) ──────────────────────────────────
    def _build_body(self):
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nsew", padx=16, pady=12)
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        self._build_form(body)
        self._build_lista(body)

    # ── Formulário (coluna esquerda) ──────────────────────────────────────────
    def _build_form(self, parent):
        form = ctk.CTkFrame(parent, corner_radius=12)
        form.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        form.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(form, text="Cadastrar remédio",
                     font=ctk.CTkFont(size=15, weight="bold")
                     ).grid(row=0, column=0, pady=(16, 4), padx=16, sticky="w")

        # Nome
        ctk.CTkLabel(form, text="Nome do remédio",
                     font=ctk.CTkFont(size=12),
                     text_color=("gray40", "gray70")
                     ).grid(row=1, column=0, padx=16, sticky="w")
        self.entry_nome = ctk.CTkEntry(form, placeholder_text="Ex: Paracetamol",
                                       height=38, corner_radius=8)
        self.entry_nome.grid(row=2, column=0, padx=16, pady=(2, 10), sticky="ew")

        # Dosagem
        ctk.CTkLabel(form, text="Dosagem (mg)",
                     font=ctk.CTkFont(size=12),
                     text_color=("gray40", "gray70")
                     ).grid(row=3, column=0, padx=16, sticky="w")
        self.entry_dose = ctk.CTkEntry(form, placeholder_text="Ex: 500",
                                       height=38, corner_radius=8)
        self.entry_dose.grid(row=4, column=0, padx=16, pady=(2, 10), sticky="ew")

        # Horários
        ctk.CTkLabel(form, text="Horário(s) — HH:MM, separados por vírgula",
                     font=ctk.CTkFont(size=12),
                     text_color=("gray40", "gray70")
                     ).grid(row=5, column=0, padx=16, sticky="w")
        self.entry_hora = ctk.CTkEntry(form, placeholder_text="Ex: 08:00, 14:00, 22:00",
                                       height=38, corner_radius=8)
        self.entry_hora.grid(row=6, column=0, padx=16, pady=(2, 16), sticky="ew")

        # Botão adicionar
        self.btn_add = ctk.CTkButton(
            form, text="＋  Adicionar remédio",
            height=42, corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.adicionar_remedio
        )
        self.btn_add.grid(row=7, column=0, padx=16, pady=(0, 16), sticky="ew")

        # Separador visual
        ctk.CTkLabel(form, text="─────────────────────",
                     text_color=("gray70", "gray40")
                     ).grid(row=8, column=0)

        # Seção excluir
        ctk.CTkLabel(form, text="Excluir remédio",
                     font=ctk.CTkFont(size=15, weight="bold")
                     ).grid(row=9, column=0, pady=(8, 4), padx=16, sticky="w")

        ctk.CTkLabel(form, text="Nome do remédio a excluir",
                     font=ctk.CTkFont(size=12),
                     text_color=("gray40", "gray70")
                     ).grid(row=10, column=0, padx=16, sticky="w")
        self.entry_excluir = ctk.CTkEntry(form, placeholder_text="Ex: Paracetamol",
                                          height=38, corner_radius=8)
        self.entry_excluir.grid(row=11, column=0, padx=16, pady=(2, 10), sticky="ew")

        self.btn_del = ctk.CTkButton(
            form, text="🗑  Excluir remédio",
            height=42, corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#c0392b", "#922b21"),
            hover_color=("#a93226", "#7b241c"),
            command=self.excluir_remedio
        )
        self.btn_del.grid(row=12, column=0, padx=16, pady=(0, 16), sticky="ew")

    # ── Lista de remédios (coluna direita) ────────────────────────────────────
    def _build_lista(self, parent):
        col = ctk.CTkFrame(parent, fg_color="transparent")
        col.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        col.grid_columnconfigure(0, weight=1)
        col.grid_rowconfigure(1, weight=1)

        topo = ctk.CTkFrame(col, fg_color="transparent")
        topo.grid(row=0, column=0, sticky="ew")
        topo.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(topo, text="Remédios cadastrados",
                     font=ctk.CTkFont(size=15, weight="bold")
                     ).grid(row=0, column=0, sticky="w")

        self.lbl_count = ctk.CTkLabel(topo, text="0 remédios",
                                      font=ctk.CTkFont(size=12),
                                      text_color=("gray40", "gray70"))
        self.lbl_count.grid(row=0, column=1, sticky="e")

        # Área rolável
        self.scroll = ctk.CTkScrollableFrame(col, corner_radius=12, label_text="")
        self.scroll.grid(row=1, column=0, sticky="nsew", pady=(8, 0))
        self.scroll.grid_columnconfigure(0, weight=1)

    # ── Status bar ────────────────────────────────────────────────────────────
    def _build_status(self):
        bar = ctk.CTkFrame(self, corner_radius=0, height=32,
                           fg_color=("gray90", "gray15"))
        bar.grid(row=2, column=0, sticky="ew")
        bar.grid_columnconfigure(0, weight=1)

        self.lbl_status = ctk.CTkLabel(
            bar, text="Pronto.",
            font=ctk.CTkFont(size=11),
            text_color=("gray40", "gray60")
        )
        self.lbl_status.grid(row=0, column=0, padx=12, pady=4, sticky="w")

    # ── Ações ─────────────────────────────────────────────────────────────────
    def adicionar_remedio(self):
        nome  = self.entry_nome.get().strip()
        dose  = self.entry_dose.get().strip()
        horas = self.entry_hora.get().strip()

        # Validar nome
        ok, erro = validar_nome(nome)
        if not ok:
            self._status(f"Erro: {erro}", erro=True)
            messagebox.showerror("Nome inválido", erro)
            return

        # Validar dosagem
        ok, resultado = formatar_dosagem(dose)
        if not ok:
            self._status(f"Erro: {resultado}", erro=True)
            messagebox.showerror("Dosagem inválida", resultado)
            return

        dose_fmt = resultado

        # Validar horários
        lista_horas = [h.strip() for h in horas.split(",") if h.strip()]
        if not lista_horas:
            self._status("Erro: informe ao menos um horário.", erro=True)
            messagebox.showerror("Horário inválido", "Informe ao menos um horário.")
            return

        invalidos = [h for h in lista_horas if not validar_horario(h)]
        if invalidos:
            msg = f"Horário(s) inválido(s): {', '.join(invalidos)}\nUse o formato HH:MM (24h)."
            self._status(f"Erro: horário inválido.", erro=True)
            messagebox.showerror("Horário inválido", msg)
            return

        # Salvar
        remedios.append(nome)
        dosagens.append(dose_fmt)
        horarios.append(lista_horas)

        with open(ARQUIVO, "a", encoding="utf-8") as f:
            f.write(f"Remédio: {nome}\n")
            f.write(f"Dosagem: {dose_fmt}\n")
            f.write(f"Horários: {', '.join(lista_horas)}\n\n")

        # Limpar campos
        self.entry_nome.delete(0, "end")
        self.entry_dose.delete(0, "end")
        self.entry_hora.delete(0, "end")

        self._status(f'"{nome}" adicionado com sucesso.')
        self.atualizar_lista()

    def excluir_remedio(self):
        nome = self.entry_excluir.get().strip()
        if not nome:
            messagebox.showwarning("Campo vazio", "Digite o nome do remédio a excluir.")
            return

        # Busca case-insensitive
        idx = next((i for i, r in enumerate(remedios) if r.lower() == nome.lower()), None)

        if idx is None:
            self._status(f'"{nome}" não encontrado.', erro=True)
            messagebox.showerror("Não encontrado", f'"{nome}" não está na lista.')
            return

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f'Deseja excluir "{remedios[idx]}" ({dosagens[idx]})?'
        )
        if not confirmar:
            return

        nome_excluido = remedios[idx]
        del remedios[idx]
        del dosagens[idx]
        del horarios[idx]

        salvar_tudo()
        self.entry_excluir.delete(0, "end")
        self._status(f'"{nome_excluido}" excluído com sucesso.')
        self.atualizar_lista()

    # ── Renderizar lista ──────────────────────────────────────────────────────
    def atualizar_lista(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()

        self.lbl_count.configure(text=f"{len(remedios)} remédio{'s' if len(remedios) != 1 else ''}")

        if not remedios:
            ctk.CTkLabel(
                self.scroll,
                text="Nenhum remédio cadastrado.\nUse o formulário ao lado para adicionar.",
                font=ctk.CTkFont(size=12),
                text_color=("gray50", "gray60"),
                justify="center"
            ).grid(row=0, column=0, pady=40)
            return

        for i, (nome, dose, horas) in enumerate(zip(remedios, dosagens, horarios)):
            card = ctk.CTkFrame(self.scroll, corner_radius=10,
                                fg_color=("white", "#1e2330"),
                                border_width=1,
                                border_color=("gray80", "gray30"))
            card.grid(row=i, column=0, sticky="ew", pady=4)
            card.grid_columnconfigure(0, weight=1)

            # Linha do nome
            topo = ctk.CTkFrame(card, fg_color="transparent")
            topo.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 2))
            topo.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                topo, text=f"💊  {nome}",
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w"
            ).grid(row=0, column=0, sticky="w")

            ctk.CTkLabel(
                topo, text=dose,
                font=ctk.CTkFont(size=12),
                text_color=("#1a5fa8", "#5b9bd5"),
                anchor="e"
            ).grid(row=0, column=1, sticky="e")

            # Horários como pills
            pills = ctk.CTkFrame(card, fg_color="transparent")
            pills.grid(row=1, column=0, sticky="w", padx=12, pady=(2, 10))

            for j, hora in enumerate(horas):
                ctk.CTkLabel(
                    pills, text=f"🕐 {hora}",
                    font=ctk.CTkFont(size=11),
                    fg_color=("gray90", "gray25"),
                    corner_radius=6,
                    padx=8, pady=2,
                    text_color=("gray30", "gray80")
                ).grid(row=0, column=j, padx=(0, 4))

    def _status(self, msg, erro=False):
        cor = ("#c0392b", "#e74c3c") if erro else ("gray40", "gray60")
        self.lbl_status.configure(text=msg, text_color=cor)


# ══════════════════════════════════════════════════════════════════════════════
# INICIALIZAÇÃO
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    carregar_arquivo()
    app = App()
    app.mainloop()
