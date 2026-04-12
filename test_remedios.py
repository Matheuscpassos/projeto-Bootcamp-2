# testes/test_remedios.py
# Testes unitários para as funções do Gerenciador de Remédios

import pytest
import datetime
from unittest.mock import patch

# ── Reprodução das funções do notebook para teste ─────────────────────────────

remedios  = []
dosagens  = []
horarios  = []


def validar_nome(nome, lista):
    """Retorna True se o nome é válido (sem números e sem duplicata)."""
    if any(c.isdigit() for c in nome):
        return False, "apenas letras"
    if nome.lower() in [r.lower() for r in lista]:
        return False, "já existe"
    return True, "ok"


def formatar_dosagem(dose_str):
    """Converte string numérica em mg ou g."""
    if not dose_str.isdigit():
        return None
    dose_int = int(dose_str)
    if dose_int >= 1000:
        return f"{dose_int / 1000} g"
    return f"{dose_int} mg"


def validar_horario(hora):
    """Retorna True se o horário está no formato HH:MM válido."""
    try:
        datetime.datetime.strptime(hora, "%H:%M")
        return True
    except ValueError:
        return False


# ── Testes de nome ────────────────────────────────────────────────────────────

class TestValidarNome:
    def teste_nome_valido(self):
        ok, msg = validar_nome("Paracetamol", [])
        assert ok is True

    def teste_rejeita_numero_no_nome(self):
        ok, _ = validar_nome("Para2cetamol", [])
        assert ok is False

    def teste_rejeita_duplicata(self):
        ok, msg = validar_nome("Dipirona", ["Dipirona"])
        assert ok is False
        assert msg == "já existe"

    def teste_duplicata_case_insensitive(self):
        ok, _ = validar_nome("DIPIRONA", ["dipirona"])
        assert ok is False

    def teste_nome_novo_nao_duplicado(self):
        ok, _ = validar_nome("Ibuprofeno", ["Paracetamol"])
        assert ok is True


# ── Testes de dosagem ─────────────────────────────────────────────────────────

class TestFormatarDosagem:
    def teste_dosagem_em_mg(self):
        assert formatar_dosagem("500") == "500 mg"

    def teste_dosagem_convertida_para_g(self):
        assert formatar_dosagem("1000") == "1.0 g"

    def teste_dosagem_2000mg_vira_2g(self):
        assert formatar_dosagem("2000") == "2.0 g"

    def teste_rejeita_texto(self):
        assert formatar_dosagem("abc") is None

    def teste_rejeita_string_vazia(self):
        assert formatar_dosagem("") is None

    def teste_rejeita_valor_com_ponto(self):
        assert formatar_dosagem("10.5") is None


# ── Testes de horário ─────────────────────────────────────────────────────────

class TestValidarHorario:
    def teste_horario_valido_manha(self):
        assert validar_horario("08:00") is True

    def teste_horario_valido_meia_noite(self):
        assert validar_horario("00:00") is True

    def teste_horario_valido_ultimo_minuto(self):
        assert validar_horario("23:59") is True

    def teste_rejeita_hora_invalida(self):
        assert validar_horario("25:00") is False

    def teste_rejeita_formato_sem_dois_pontos(self):
        assert validar_horario("0800") is False

    def teste_rejeita_formato_com_traco(self):
        assert validar_horario("08-00") is False

    def teste_rejeita_texto(self):
        assert validar_horario("oito horas") is False

    def teste_rejeita_string_vazia(self):
        assert validar_horario("") is False

    def teste_rejeita_hora_sem_zero_a_esquerda(self):
        assert validar_horario("8:00") is False
