# Configurações do Transcritor de Áudio

# ========== CONFIGURAÇÕES DE ÁUDIO ==========
SAMPLE_RATE = 16000  # Taxa de amostragem (16kHz recomendado para Whisper)
CHANNELS = 1         # Número de canais (1 = mono, 2 = estéreo)
AUDIO_FORMAT = 'float32'  # Formato dos dados de áudio

# ========== CONFIGURAÇÕES DA API OPENAI ==========
API_URL = "https://api.openai.com/v1/audio/transcriptions"
MODEL = "whisper-1"  # Modelo Whisper da OpenAI
LANGUAGE = "pt"      # Idioma ('pt', 'en', 'es', 'fr', etc. ou None para auto-detect)
TIMEOUT = 30         # Timeout da requisição em segundos

# ========== CONFIGURAÇÕES DA INTERFACE ==========
WINDOW_TITLE = "Transcritor de Áudio"
WINDOW_SIZE = "500x400"
WINDOW_RESIZABLE = True

# Tema Noturno - Cores
DARK_BG = "#1e1e1e"          # Fundo principal escuro
DARK_FG = "#ffffff"          # Texto branco
DARK_BG_SECONDARY = "#2d2d2d" # Fundo secundário
DARK_ACCENT = "#00d4aa"      # Cor de destaque (verde-azulado)
DARK_BUTTON_BG = "#3c3c3c"   # Fundo dos botões
DARK_BUTTON_HOVER = "#4a4a4a" # Botão em hover
DARK_ENTRY_BG = "#2d2d2d"    # Fundo de entrada de texto
DARK_BORDER = "#404040"      # Bordas
DARK_SELECT_BG = "#0d7377"   # Seleção de texto

# Textos dos botões
BUTTON_RECORD = "🎤 Gravar"
BUTTON_STOP = "⏹️ Parar"
BUTTON_COPY = "📋 Copiar Texto"

# Textos de status
STATUS_READY = "Pronto para gravar"
STATUS_RECORDING = "🔴 Gravando..."
STATUS_PROCESSING = "Processando áudio..."
STATUS_TRANSCRIBING = "Enviando para transcrição..."
STATUS_COMPLETED = "Transcrição concluída - {} caracteres"
STATUS_COPIED = "Texto copiado para área de transferência!"
STATUS_NO_AUDIO = "Nenhum áudio gravado"
STATUS_ERROR_PROCESSING = "Erro no processamento"
STATUS_ERROR_TRANSCRIPTION = "Erro na transcrição"
STATUS_TIMEOUT = "Timeout"

# ========== CONFIGURAÇÕES AVANÇADAS ==========
DELETE_TEMP_FILES = True  # Deletar arquivos temporários após transcrição
TEMP_FILE_SUFFIX = '.wav'  # Extensão do arquivo temporário

# Configurações do ScrolledText
TEXT_AREA_WIDTH = 50
TEXT_AREA_HEIGHT = 15
TEXT_FONT = ("Segoe UI", 10)

# Configurações dos botões
BUTTON_FONT = ("Segoe UI", 12, "bold")

# ========== MENSAGENS DE ERRO ==========
ERROR_NO_PYTHON = "Erro: Python não está disponível"
ERROR_API_KEY_REQUIRED = "API key é obrigatória para usar o aplicativo"
ERROR_NO_AUDIO_FILE = "Arquivo de áudio não encontrado"
ERROR_RECORDING_START = "Erro ao iniciar gravação: {}"
ERROR_RECORDING_AUDIO = "Erro na gravação: {}"
ERROR_PROCESSING_AUDIO = "Erro ao processar áudio: {}"
ERROR_TRANSCRIPTION = "Erro na transcrição: {}"
ERROR_COPY = "Erro ao copiar: {}"

# Avisos
WARNING_NO_TEXT_TO_COPY = "Nenhum texto para copiar"

# Títulos de diálogos
DIALOG_API_KEY_TITLE = "API Key OpenAI"
DIALOG_API_KEY_MESSAGE = "Digite sua API key da OpenAI:" 