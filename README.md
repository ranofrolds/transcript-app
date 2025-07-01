# 🎤 Transcritor de Áudio

Aplicação minimalista para transcrição de áudio usando a API Whisper da OpenAI.

## ✨ Funcionalidades

- **Gravação de áudio** via microfone com um clique
- **Transcrição automática** usando OpenAI Whisper API
- **Interface limpa e minimalista** em Tkinter
- **Copiar texto** para área de transferência
- **Suporte ao português** (configurável)
- **API Key salva automaticamente** - não precisa digitar toda vez
- **Menu completo** para gerenciar configurações
- **Execução sem terminal** (modo silencioso)
- **Arquivos temporários** são removidos automaticamente

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- API Key da OpenAI ([obter aqui](https://platform.openai.com/api-keys))
- Microfone funcionando

### Passos

1. **Clone ou baixe o projeto:**

   ```bash
   git clone <url-do-repositório>
   cd transcript
   ```

2. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o aplicativo:**

   ```bash
   # Com terminal:
   python main.py

   # Sem terminal (modo silencioso):
   pythonw main.pyw

   # Ou use o script:
   executar_sem_terminal.bat
   ```

## 🔧 Configuração

### API Key da OpenAI

Na primeira execução, o aplicativo solicitará sua API key da OpenAI.

**Como obter uma API key:**

1. Acesse [platform.openai.com](https://platform.openai.com)
2. Faça login ou crie uma conta
3. Vá em "API Keys"
4. Clique em "Create new secret key"
5. Copie a chave e cole no aplicativo

### Problemas de Áudio

Se encontrar problemas com o microfone:

1. **Verifique se o microfone está funcionando** em outras aplicações
2. **Execute como administrador** se necessário
3. **Instale drivers de áudio atualizados**

## 📱 Como Usar

### Fluxo Básico

1. **Abra o aplicativo** → `python main.py` ou `pythonw main.pyw` (sem terminal)
2. **Configure API key** (apenas na primeira vez)
3. **Clique em "🎤 Gravar"** → botão vira "⏹️ Parar"
4. **Fale no microfone** → status mostra "🔴 Gravando..."
5. **Clique em "⏹️ Parar"** → áudio é enviado para transcrição
6. **Texto aparece** na caixa de texto
7. **Clique em "📋 Copiar Texto"** para copiar

### Gerenciar API Key

- **Menu Configurações** → Alterar API Key
- **Menu Configurações** → Remover API Key
- **Menu Ajuda** → Obter API Key (abre site OpenAI)

### Interface

```
┌─────────────────────────────────┐
│        🎤 Gravar               │
├─────────────────────────────────┤
│ ┌─ Texto Transcrito ─────────┐ │
│ │                            │ │
│ │  [texto transcrito aqui]   │ │
│ │                            │ │
│ └────────────────────────────┘ │
├─────────────────────────────────┤
│        📋 Copiar Texto         │
├─────────────────────────────────┤
│ Status: Pronto para gravar     │
└─────────────────────────────────┘
```

## 🔧 Compilação para Windows (.exe)

Para criar um executável standalone:

1. **Instale PyInstaller:**

   ```bash
   pip install pyinstaller
   ```

2. **Compile o aplicativo:**

   ```bash
   pyinstaller --onefile --windowed --name "Transcritor" main.py
   ```

3. **Encontre o .exe em:**
   ```
   dist/Transcritor.exe
   ```

### Parâmetros do PyInstaller

- `--onefile`: Arquivo único
- `--windowed`: Sem console
- `--name`: Nome do executável

## 🛠️ Dependências

| Biblioteca    | Versão   | Função                           |
| ------------- | -------- | -------------------------------- |
| `sounddevice` | >=0.4.6  | Gravação de áudio                |
| `soundfile`   | >=0.12.1 | Manipulação de arquivos de áudio |
| `numpy`       | >=1.25.0 | Processamento de arrays de áudio |
| `requests`    | >=2.31.0 | Comunicação com API OpenAI       |
| `pyperclip`   | >=1.8.2  | Cópia para área de transferência |
| `openai`      | >=1.3.0  | Client oficial OpenAI (opcional) |

## ⚙️ Configurações Avançadas

### Alterar Idioma da Transcrição

Edite o arquivo `main.py`, linha ~187:

```python
files = {
    'file': ('audio.wav', audio_file, 'audio/wav'),
    'model': (None, 'whisper-1'),
    'language': (None, 'en')  # Mude para 'en', 'es', 'fr', etc.
}
```

### Alterar Taxa de Amostragem

Edite o arquivo `main.py`, linha ~18:

```python
self.sample_rate = 16000  # Mude para 44100 para qualidade máxima
```

### Timeout da API

Edite o arquivo `main.py`, linha ~192:

```python
response = requests.post(url, headers=headers, files=files, timeout=60)  # 60 segundos
```

## 🐛 Solução de Problemas

### Erro de Permissão de Microfone

**Windows:**

1. Vá em Configurações → Privacidade → Microfone
2. Ative "Permitir que apps acessem seu microfone"

### Erro de API Key

- Verifique se a API key está correta
- Verifique se há créditos na conta OpenAI
- Teste a key em [platform.openai.com](https://platform.openai.com)

### Erro de Instalação (Python 3.12)

**Problema comum com Python 3.12 e numpy:**

#### Solução Automática:

```bash
# Execute o script de resolução:
resolver_problemas_instalacao.bat
```

#### Soluções Manuais:

**Opção 1 - Atualizar pip:**

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Opção 2 - Usar versões mínimas:**

```bash
pip install -r requirements_minimal.txt
```

**Opção 3 - Anaconda (Recomendado):**

```bash
conda install -c conda-forge sounddevice soundfile numpy requests pyperclip
```

**Opção 4 - Python 3.11:**

- Baixe Python 3.11 em: https://python.org
- Python 3.11 tem melhor compatibilidade

### Aplicativo Não Inicia

1. Verifique se Python 3.8+ está instalado
2. Execute: `python --version`
3. Reinstale dependências: `pip install -r requirements.txt --force-reinstall`

## 📋 Limitações

- **Arquivos grandes**: Whisper API tem limite de 25MB
- **Duração máxima**: ~25 minutos de áudio
- **Formato**: Apenas WAV (16kHz, mono)
- **Idiomas**: Funciona melhor com português e inglês

## 🆘 Suporte

### Logs e Debug

Para logs detalhados, execute:

```bash
python main.py > log.txt 2>&1
```

### Contato

- Abra uma issue no repositório
- Inclua sempre:
  - Versão do Python
  - Sistema operacional
  - Mensagem de erro completa
  - Arquivo `log.txt` se disponível

---

**Versão:** 1.0.0  
**Licença:** MIT  
**Compatibilidade:** Windows 10/11, Python 3.8+
