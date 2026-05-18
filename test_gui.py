# testes/test_gui.py
# Testes automatizados para o Gerenciador de Remédios (GUI v2.0)
# Execução: pytest testes/ -v

import datetime
import os
import sys
import tempfile
import pytest
from unittest.mock import patch, MagicMock

# Adiciona a raiz do projeto ao path para importar o módulo principal
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa apenas as funções puras (sem iniciar a GUI)
from gerenciador_remedios import (
    validar_nome,
    formatar_dosagem,
    validar_horario,
    salvar_tudo,
    carregar_arquivo,
)
import gerenciador_remedios as app_module


# ══════════════════════════════════════════════════════════════════════════════
# FIXTURE: estado limpo antes de cada teste
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture(autouse=True)
def limpar_listas():
    """Garante que as listas globais estejam vazias antes de cada teste."""
    app_module.remedios.clear()
    app_module.dosagens.clear()
    app_module.horarios.clear()
    yield
    app_module.remedios.clear()
    app_module.dosagens.clear()
    app_module.horarios.clear()


# ══════════════════════════════════════════════════════════════════════════════
# TESTES — validar_nome
# ══════════════════════════════════════════════════════════════════════════════

class TestValidarNome:
    def test_nome_valido_retorna_true(self):
        ok, erro = validar_nome("Paracetamol")
        assert ok is True
        assert erro == ""

    def test_nome_vazio_invalido(self):
        ok, erro = validar_nome("")
        assert ok is False
        assert erro != ""

    def test_nome_so_espacos_invalido(self):
        ok, erro = validar_nome("   ")
        assert ok is False

    def test_nome_com_numero_invalido(self):
        ok, erro = validar_nome("Para2cetamol")
        assert ok is False
        assert "número" in erro.lower()

    def test_nome_duplicado_invalido(self):
        app_module.remedios.append("Dipirona")
        ok, erro = validar_nome("Dipirona")
        assert ok is False
        assert "cadastrado" in erro.lower()

    def test_duplicata_case_insensitive(self):
        app_module.remedios.append("dipirona")
        ok, _ = validar_nome("DIPIRONA")
        assert ok is False

    def test_nome_diferente_do_existente_valido(self):
        app_module.remedios.append("Paracetamol")
        ok, _ = validar_nome("Ibuprofeno")
        assert ok is True

    def test_nome_com_acento_valido(self):
        ok, _ = validar_nome("Ácido Fólico")
        assert ok is True


# ══════════════════════════════════════════════════════════════════════════════
# TESTES — formatar_dosagem
# ══════════════════════════════════════════════════════════════════════════════

class TestFormatarDosagem:
    def test_dosagem_pequena_em_mg(self):
        ok, resultado = formatar_dosagem("500")
        assert ok is True
        assert resultado == "500 mg"

    def test_dosagem_1000_converte_para_g(self):
        ok, resultado = formatar_dosagem("1000")
        assert ok is True
        assert resultado == "1.0 g"

    def test_dosagem_2500_converte_para_g(self):
        ok, resultado = formatar_dosagem("2500")
        assert ok is True
        assert resultado == "2.5 g"

    def test_dosagem_1_mg_valida(self):
        ok, resultado = formatar_dosagem("1")
        assert ok is True
        assert resultado == "1 mg"

    def test_dosagem_999_mg(self):
        ok, resultado = formatar_dosagem("999")
        assert ok is True
        assert "mg" in resultado

    def test_dosagem_texto_invalida(self):
        ok, _ = formatar_dosagem("abc")
        assert ok is False

    def test_dosagem_vazia_invalida(self):
        ok, _ = formatar_dosagem("")
        assert ok is False

    def test_dosagem_com_ponto_invalida(self):
        ok, _ = formatar_dosagem("10.5")
        assert ok is False

    def test_dosagem_negativa_invalida(self):
        ok, _ = formatar_dosagem("-100")
        assert ok is False

    def test_dosagem_zero_invalida(self):
        ok, _ = formatar_dosagem("0")
        assert ok is False


# ══════════════════════════════════════════════════════════════════════════════
# TESTES — validar_horario
# ══════════════════════════════════════════════════════════════════════════════

class TestValidarHorario:
    def test_horario_valido_manha(self):
        assert validar_horario("08:00") is True

    def test_horario_valido_meia_noite(self):
        assert validar_horario("00:00") is True

    def test_horario_valido_ultimo_minuto(self):
        assert validar_horario("23:59") is True

    def test_horario_valido_meio_dia(self):
        assert validar_horario("12:30") is True

    def test_hora_invalida_acima_23(self):
        assert validar_horario("25:00") is False

    def test_minuto_invalido_acima_59(self):
        assert validar_horario("10:60") is False

    def test_formato_sem_dois_pontos(self):
        assert validar_horario("0800") is False

    def test_formato_com_traco(self):
        assert validar_horario("08-00") is False

    def test_sem_zero_a_esquerda(self):
        assert validar_horario("8:00") is False

    def test_texto_invalido(self):
        assert validar_horario("oito horas") is False

    def test_string_vazia(self):
        assert validar_horario("") is False

    def test_horario_com_espacos_e_strip(self):
        # A GUI envia strings com possíveis espaços; validar_horario faz strip
        assert validar_horario("  08:00  ") is True


# ══════════════════════════════════════════════════════════════════════════════
# TESTES — persistência (salvar_tudo / carregar_arquivo)
# ══════════════════════════════════════════════════════════════════════════════

class TestPersistencia:
    def test_salvar_e_carregar_um_remedio(self, tmp_path):
        arquivo = tmp_path / "lista.txt"
        app_module.ARQUIVO = str(arquivo)

        app_module.remedios.append("Paracetamol")
        app_module.dosagens.append("500 mg")
        app_module.horarios.append(["08:00", "20:00"])

        salvar_tudo()

        # Limpa memória e recarrega do arquivo
        app_module.remedios.clear()
        app_module.dosagens.clear()
        app_module.horarios.clear()

        carregar_arquivo()

        assert app_module.remedios == ["Paracetamol"]
        assert app_module.dosagens == ["500 mg"]
        assert app_module.horarios == [["08:00", "20:00"]]

    def test_salvar_e_carregar_multiplos_remedios(self, tmp_path):
        arquivo = tmp_path / "lista.txt"
        app_module.ARQUIVO = str(arquivo)

        app_module.remedios  = ["Dipirona", "Ibuprofeno"]
        app_module.dosagens  = ["1.0 g", "400 mg"]
        app_module.horarios  = [["06:00", "18:00"], ["08:00"]]

        salvar_tudo()

        app_module.remedios.clear()
        app_module.dosagens.clear()
        app_module.horarios.clear()

        carregar_arquivo()

        assert len(app_module.remedios) == 2
        assert "Dipirona" in app_module.remedios
        assert "Ibuprofeno" in app_module.remedios

    def test_carregar_arquivo_inexistente_nao_quebra(self, tmp_path):
        app_module.ARQUIVO = str(tmp_path / "nao_existe.txt")
        carregar_arquivo()  # Não deve lançar exceção
        assert app_module.remedios == []

    def test_salvar_apaga_dados_anteriores(self, tmp_path):
        arquivo = tmp_path / "lista.txt"
        app_module.ARQUIVO = str(arquivo)

        # Salva versão inicial
        app_module.remedios = ["Remedio A"]
        app_module.dosagens = ["100 mg"]
        app_module.horarios = [["08:00"]]
        salvar_tudo()

        # Remove o primeiro e salva novamente
        app_module.remedios.clear()
        app_module.dosagens.clear()
        app_module.horarios.clear()
        salvar_tudo()

        carregar_arquivo()
        assert app_module.remedios == []


# ══════════════════════════════════════════════════════════════════════════════
# TESTES — fluxo completo de adição e exclusão (sem GUI)
# ══════════════════════════════════════════════════════════════════════════════

class TestFluxoCompleto:
    def test_adicionar_remedio_valido(self, tmp_path):
        app_module.ARQUIVO = str(tmp_path / "lista.txt")

        nome  = "Paracetamol"
        ok_n, _       = validar_nome(nome)
        ok_d, dose    = formatar_dosagem("500")
        ok_h          = validar_horario("08:00")

        assert ok_n and ok_d and ok_h

        app_module.remedios.append(nome)
        app_module.dosagens.append(dose)
        app_module.horarios.append(["08:00"])

        assert len(app_module.remedios) == 1

    def test_excluir_remedio_existente(self, tmp_path):
        app_module.ARQUIVO = str(tmp_path / "lista.txt")

        app_module.remedios  = ["Paracetamol", "Dipirona"]
        app_module.dosagens  = ["500 mg", "1.0 g"]
        app_module.horarios  = [["08:00"], ["06:00", "18:00"]]

        # Exclui Paracetamol
        idx = next(i for i, r in enumerate(app_module.remedios)
                   if r.lower() == "paracetamol")
        del app_module.remedios[idx]
        del app_module.dosagens[idx]
        del app_module.horarios[idx]

        assert "Paracetamol" not in app_module.remedios
        assert "Dipirona" in app_module.remedios

    def test_nao_permite_duplicata_apos_adicionar(self):
        app_module.remedios.append("Paracetamol")
        ok, _ = validar_nome("Paracetamol")
        assert ok is False

    def test_horarios_multiplos_validos(self):
        horas = ["08:00", "14:00", "22:00"]
        assert all(validar_horario(h) for h in horas)

    def test_horarios_com_um_invalido_detectado(self):
        horas = ["08:00", "99:99", "22:00"]
        invalidos = [h for h in horas if not validar_horario(h)]
        assert len(invalidos) == 1
        assert "99:99" in invalidos
