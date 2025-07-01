# 🚀 Início Rápido - Transcritor de Áudio

## 📋 Pré-requisitos

- Python 3.8+
- API Key da OpenAI
- Microfone

## ⚡ Instalação Rápida

### Opção 1: Script Automático (Windows)

```bash
# Clique duas vezes em:
instalar_e_executar.bat
```

### Opção 2: Manual

```bash
pip install -r requirements.txt

# Com terminal:
python main.py

# Sem terminal:
pythonw main.pyw
```

## 🎯 Como Usar

1. **Execute** → `pythonw main.pyw` (sem terminal) ou `python main.py`
2. **Configure API key** (apenas na primeira vez)
3. **Clique "🎤 Gravar"** → botão vira "⏹️ Parar"
4. **Fale** → status mostra "🔴 Gravando..."
5. **Clique "⏹️ Parar"** → aguarde transcrição
6. **Clique "📋 Copiar Texto"** → texto na área de transferência

## ⚙️ Gerenciar API Key

- **Menu Configurações** → Alterar/Remover API Key
- **Menu Ajuda** → Obter nova API Key

## 🔑 API Key OpenAI

1. Acesse: https://platform.openai.com/api-keys
2. Faça login
3. Clique "Create new secret key"
4. Copie e cole no app

## 🔧 Compilar para .EXE

```bash
# Execute:
compilar_exe.bat

# Ou manual:
pip install pyinstaller
pyinstaller --onefile --windowed --name "Transcritor" main.py
```

Executável estará em: `dist/Transcritor.exe`

## ⚙️ Configurações Rápidas

Edite `config.py` para alterar:

- **Idioma:** `LANGUAGE = "en"` (inglês)
- **Qualidade:** `SAMPLE_RATE = 44100` (máxima)
- **Timeout:** `TIMEOUT = 60` (60 segundos)

## 🐛 Problemas Comuns

**Erro de instalação (Python 3.12):**

```bash
# Execute o script automático:
resolver_problemas_instalacao.bat

# Ou manual:
python -m pip install --upgrade pip
pip install -r requirements_minimal.txt
```

**Erro de microfone:**

- Windows: Configurações → Privacidade → Microfone → Ativar

**Erro API Key:**

- Verifique se está correta
- Verifique créditos na conta OpenAI

---

**Pronto para usar!** 🎉
