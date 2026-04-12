# 💊 Gerenciador de Remédios

Aplicação desktop para cadastrar, visualizar e excluir remédios com nome, dosagem e horários de uso. Desenvolvida em Python com interface gráfica (GUI) usando **CustomTkinter**.

---

## Funcionalidades

- Cadastrar remédio com nome, dosagem (mg/g) e horários (formato 24h)
- Validação de nome (sem números, sem duplicatas)
- Conversão automática de dosagem: valores ≥ 1000 mg são exibidos em gramas
- Suporte a múltiplos horários por remédio (separados por vírgula)
- Excluir remédio com confirmação (busca case-insensitive)
- Persistência em arquivo `lista.txt`
- Carregamento automático dos dados ao abrir o programa
- Interface com modo escuro e barra de status

---

## Pré-requisitos

- Python 3.11 ou superior
- pip

---

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/gerenciador-remedios.git
cd gerenciador-remedios

# 2. (Opcional) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt
```

---

## Como executar

```bash
python gerenciador_remedios.py
```

A interface abrirá automaticamente em modo escuro.

---

## Como executar os testes

```bash
pytest testes/ -v
```

---

## Como executar o lint

```bash
flake8 gerenciador_remedios.py --max-line-length=100
```

---

## Estrutura do projeto

```
gerenciador-remedios/
├── gerenciador_remedios.py   # Aplicação principal (GUI + lógica)
├── requirements.txt          # Dependências do projeto
├── testes/
│   └── test_gui.py           # Testes automatizados
├── .github/
│   └── workflows/
│       └── ci.yml            # Pipeline CI com GitHub Actions
├── lista.txt                 # Gerado automaticamente ao usar o app
└── README.md                 # Este arquivo
```

---

## Pipeline CI/CD

A cada **push** ou **pull request**, o GitHub Actions executa automaticamente:

1. **Lint** — verificação de qualidade estática com `flake8`
2. **Testes** — execução dos testes unitários com `pytest`

---

## Tecnologias utilizadas

| Ferramenta | Finalidade |
|---|---|
| Python 3.11 | Linguagem principal |
| CustomTkinter | Interface gráfica (GUI) |
| pytest | Testes automatizados |
| flake8 | Lint e análise estática |
| GitHub Actions | Integração contínua (CI) |

---

## Autor

Projeto desenvolvido como estudo de GUI em Python com integração CI/CD via GitHub Actions.
