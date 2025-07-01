import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import sounddevice as sd
import soundfile as sf
import numpy as np
import requests
import tempfile
import os
from datetime import datetime
import pyperclip
import config
import json
import base64
import sys

class TranscriptApp:
    def __init__(self, root):
        self.root = root
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(config.WINDOW_SIZE)
        self.root.resizable(config.WINDOW_RESIZABLE, config.WINDOW_RESIZABLE)
        
        # Configurar identificação da aplicação no Windows
        self.setup_windows_taskbar()
        
        # Configurar ícone da aplicação
        self.setup_app_icon()
        
        # Arquivo para salvar configurações
        self.config_file = "transcritor_config.json"
        
        # Variáveis de controle
        self.recording = False
        self.audio_data = []
        self.sample_rate = config.SAMPLE_RATE
        self.temp_file = None
        
        # API Key da OpenAI
        self.api_key = ""
        
        self.setup_ui()
        self.load_api_key()
        
        # Aplicar ícone após tudo estar carregado
        self.root.after(500, self.apply_icon_delayed)
    
    def apply_icon_delayed(self):
        """Aplica o ícone após a janela estar completamente carregada"""
        icon_path_ico = os.path.abspath('icon.ico')
        icon_path_png = os.path.abspath('icon.png')
        
        try:
            if os.path.exists(icon_path_ico):
                # Reaplicar ícone ICO
                self.root.iconbitmap(icon_path_ico)
            elif os.path.exists(icon_path_png):
                # Se ICO não existir, tentar PNG
                img = tk.PhotoImage(file=icon_path_png)
                self.root.iconphoto(True, img)
            
            # Para Windows - forçar atualização na barra de tarefas
            if sys.platform == "win32":
                try:
                    import ctypes
                    
                    # Obter handle da janela
                    hwnd = int(self.root.frame(), 16)
                    
                    # Forçar redesenho da barra de tarefas
                    ctypes.windll.user32.SetWindowPos(
                        hwnd, 0, 0, 0, 0, 0, 
                        0x0001 | 0x0002 | 0x0020  # SWP_NOSIZE | SWP_NOMOVE | SWP_FRAMECHANGED
                    )
                    
                except:
                    pass
                    
        except Exception:
            pass
    
    def setup_windows_taskbar(self):
        """Configura corretamente o ícone e identificação no Windows"""
        try:
            # No Windows, definir um App User Model ID único
            if sys.platform == "win32":
                try:
                    import ctypes
                    myappid = 'transcriptor.audio.app.1.0'  # ID único da aplicação
                    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
                except:
                    pass
        except Exception:
            pass
    
    def setup_app_icon(self):
        """Configura o ícone da aplicação para janela e barra de tarefas"""
        icon_path_ico = os.path.abspath('icon.ico')
        icon_path_png = os.path.abspath('icon.png')
        
        try:
            if not os.path.exists(icon_path_ico):
                # Tentar gerar ícone se não existir
                try:
                    import create_icon
                    create_icon.create_app_icon()
                    create_icon.create_png_icon()
                except:
                    pass
            
            # Tentar ICO primeiro
            if os.path.exists(icon_path_ico):
                # Método 1: Configuração básica do ícone
                try:
                    self.root.iconbitmap(icon_path_ico)
                except:
                    # Se ICO falhar, tentar PNG
                    try:
                        if os.path.exists(icon_path_png):
                            img = tk.PhotoImage(file=icon_path_png)
                            self.root.iconphoto(True, img)
                    except:
                        pass
                
                # Método 2: Para Windows - configuração específica da barra de tarefas
                if sys.platform == "win32":
                    try:
                        # Usar bibliotecas Windows específicas
                        import ctypes
                        
                        # Definir constantes do Windows
                        ICON_SMALL = 0
                        ICON_BIG = 1
                        WM_SETICON = 0x0080
                        
                        # Aguardar janela estar pronta
                        self.root.update()
                        
                        # Carregar ícone
                        hicon = ctypes.windll.user32.LoadImageW(
                            None, 
                            icon_path, 
                            1,  # IMAGE_ICON
                            0, 0, 
                            0x00000010  # LR_LOADFROMFILE
                        )
                        
                        if hicon:
                            # Obter handle da janela usando Tkinter
                            hwnd = int(self.root.frame(), 16)
                            
                            # Definir ícone pequeno e grande
                            ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon)
                            ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon)
                    except Exception as e:
                        # Método alternativo para Windows
                        try:
                            self.root.after(100, lambda: self.root.iconbitmap(icon_path_ico))
                        except:
                            pass
                
                # Método 3: Configurações alternativas do Tkinter
                try:
                    self.root.wm_iconbitmap(icon_path_ico)
                except:
                    pass
                    
                try:
                    self.root.tk.call('wm', 'iconbitmap', self.root._w, icon_path_ico)
                except:
                    pass
                    
        except Exception as e:
            # Se falhar, tentar criar um ícone simples
            try:
                import create_icon
                create_icon.create_simple_icon()
                create_icon.create_png_icon()
                if os.path.exists(icon_path_ico):
                    self.root.iconbitmap(icon_path_ico)
                elif os.path.exists(icon_path_png):
                    img = tk.PhotoImage(file=icon_path_png)
                    self.root.iconphoto(True, img)
            except:
                pass
    
    def setup_dark_theme(self):
        """Configura o tema noturno da aplicação"""
        # Configurar janela principal
        self.root.configure(bg=config.DARK_BG)
        
        # Configurar opções padrão para widgets Tkinter
        self.root.option_add('*TCombobox*Listbox.selectBackground', config.DARK_SELECT_BG)
        self.root.option_add('*TCombobox*Listbox.background', config.DARK_BG_SECONDARY)
        self.root.option_add('*TCombobox*Listbox.foreground', config.DARK_FG)
    
    def apply_dark_style(self, style):
        """Aplica estilo escuro aos widgets ttk"""
        # Configurar estilo para Frame
        style.configure("TFrame", background=config.DARK_BG)
        
        # Configurar estilo para Label
        style.configure("TLabel", 
                       background=config.DARK_BG, 
                       foreground=config.DARK_FG)
        
        # Configurar estilo para LabelFrame  
        style.configure("TLabelframe", 
                       background=config.DARK_BG, 
                       foreground=config.DARK_FG,
                       bordercolor=config.DARK_BORDER)
        style.configure("TLabelframe.Label", 
                       background=config.DARK_BG, 
                       foreground=config.DARK_FG)
        
        # Configurar estilo para Button
        style.configure("TButton",
                       background=config.DARK_BUTTON_BG,
                       foreground=config.DARK_FG,
                       borderwidth=1,
                       focuscolor='none')
        style.map("TButton",
                 background=[('active', config.DARK_BUTTON_HOVER),
                           ('pressed', config.DARK_ACCENT)])
        
        # Configurar estilo para Entry
        style.configure("TEntry",
                       fieldbackground=config.DARK_ENTRY_BG,
                       background=config.DARK_ENTRY_BG,
                       foreground=config.DARK_FG,
                       bordercolor=config.DARK_BORDER,
                       insertcolor=config.DARK_FG)
        
        # Configurar estilo especial para botão de gravar
        style.configure("Record.TButton",
                       background=config.DARK_ACCENT,
                       foreground=config.DARK_BG,
                       font=('Arial', 10, 'bold'))
        style.map("Record.TButton",
                 background=[('active', '#00b894'),
                           ('pressed', '#00a085')])
        
        # Configurar estilo para botão parar
        style.configure("Stop.TButton",
                       background="#dc3545",
                       foreground=config.DARK_FG,
                       font=('Arial', 10, 'bold'))
        style.map("Stop.TButton",
                 background=[('active', '#c82333'),
                           ('pressed', '#bd2130')])
    
    def setup_ui(self):
        # Configurar tema noturno
        self.setup_dark_theme()
        
        # Configurar menu
        self.setup_menu()
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        self.apply_dark_style(style)
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Botão Gravar/Parar
        self.record_button = ttk.Button(
            main_frame, 
            text=config.BUTTON_RECORD, 
            command=self.toggle_recording,
            style="Record.TButton"
        )
        self.record_button.grid(row=0, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        
        # Configurar estilo do botão
        style.configure("Record.TButton", font=config.BUTTON_FONT)
        style.configure("Stop.TButton", font=config.BUTTON_FONT)
        
        # Caixa de texto para resultado
        text_frame = ttk.LabelFrame(main_frame, text="Texto Transcrito", padding="10")
        text_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.text_area = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            width=config.TEXT_AREA_WIDTH,
            height=config.TEXT_AREA_HEIGHT,
            font=config.TEXT_FONT,
            bg=config.DARK_BG_SECONDARY,
            fg=config.DARK_FG,
            insertbackground=config.DARK_FG,
            selectbackground=config.DARK_SELECT_BG,
            selectforeground=config.DARK_FG,
            borderwidth=1,
            relief="solid"
        )
        self.text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botão Copiar
        self.copy_button = ttk.Button(
            main_frame,
            text=config.BUTTON_COPY,
            command=self.copy_text,
            state="disabled"
        )
        self.copy_button.grid(row=2, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set(config.STATUS_READY)
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E))
    
    def setup_menu(self):
        """Configura o menu da aplicação"""
        menubar = tk.Menu(self.root, 
                         bg=config.DARK_BG_SECONDARY, 
                         fg=config.DARK_FG,
                         activebackground=config.DARK_ACCENT,
                         activeforeground=config.DARK_BG)
        self.root.config(menu=menubar)
        
        # Menu Configurações
        config_menu = tk.Menu(menubar, tearoff=0,
                             bg=config.DARK_BG_SECONDARY, 
                             fg=config.DARK_FG,
                             activebackground=config.DARK_ACCENT,
                             activeforeground=config.DARK_BG)
        menubar.add_cascade(label="Configurações", menu=config_menu)
        config_menu.add_command(label="Alterar API Key", command=self.change_api_key)
        config_menu.add_command(label="Remover API Key", command=self.remove_api_key)
        config_menu.add_separator()
        config_menu.add_command(label="Sobre", command=self.show_about)
        
        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0,
                           bg=config.DARK_BG_SECONDARY, 
                           fg=config.DARK_FG,
                           activebackground=config.DARK_ACCENT,
                           activeforeground=config.DARK_BG)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Como Usar", command=self.show_help)
        help_menu.add_command(label="Obter API Key", command=self.open_api_key_url)
    
    def load_api_key(self):
        """Carrega a API key salva ou solicita uma nova"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                    # Descriptografar API key (codificação simples)
                    encoded_key = config_data.get('api_key', '')
                    if encoded_key:
                        self.api_key = base64.b64decode(encoded_key.encode()).decode()
                        self.status_var.set("API Key carregada - Pronto para gravar")
                        return
        except Exception:
            pass
        
        # Se não conseguiu carregar, solicita nova API key
        self.ask_for_api_key()
    
    def save_api_key(self):
        """Salva a API key de forma segura"""
        try:
            # Criptografar API key (codificação simples)
            encoded_key = base64.b64encode(self.api_key.encode()).decode()
            config_data = {
                'api_key': encoded_key,
                'app_version': '1.0.0'
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f)
            
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {str(e)}")
            return False
    
    def change_api_key(self):
        """Permite alterar a API key"""
        current_key = "***" + self.api_key[-8:] if len(self.api_key) > 8 else "***"
        
        new_key = tk.simpledialog.askstring(
            "Alterar API Key",
            f"API Key atual: {current_key}\n\nDigite a nova API key:",
            show='*'
        )
        
        if new_key and new_key.strip():
            self.api_key = new_key.strip()
            if self.save_api_key():
                messagebox.showinfo("Sucesso", "API Key alterada com sucesso!")
                self.status_var.set("API Key atualizada - Pronto para gravar")
    
    def remove_api_key(self):
        """Remove a API key salva"""
        if messagebox.askyesno("Confirmar", "Deseja remover a API Key salva?\n\nVocê precisará digitar novamente na próxima execução."):
            try:
                if os.path.exists(self.config_file):
                    os.remove(self.config_file)
                self.api_key = ""
                messagebox.showinfo("Sucesso", "API Key removida com sucesso!")
                self.status_var.set("API Key removida - Configure novamente")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover configurações: {str(e)}")
    
    def show_about(self):
        """Mostra informações sobre o aplicativo"""
        about_text = """Transcritor de Áudio v1.0.0

Aplicação para transcrição de áudio usando OpenAI Whisper API.

Funcionalidades:
• Gravação via microfone
• Transcrição automática
• Copiar texto
• Interface minimalista

Tecnologias:
• Python + Tkinter
• OpenAI Whisper API
• sounddevice + numpy"""
        
        messagebox.showinfo("Sobre", about_text)
    
    def show_help(self):
        """Mostra ajuda de uso"""
        help_text = """Como Usar:

1. Configure sua API Key (menu Configurações)
2. Clique "🎤 Gravar" para iniciar
3. Fale no microfone
4. Clique "⏹️ Parar" para finalizar
5. Aguarde a transcrição
6. Use "📋 Copiar Texto" para copiar

Dicas:
• Fale claramente e próximo ao microfone
• Evite ruídos de fundo
• A transcrição funciona melhor com português e inglês"""
        
        messagebox.showinfo("Como Usar", help_text)
    
    def open_api_key_url(self):
        """Abre URL para obter API Key"""
        import webbrowser
        webbrowser.open("https://platform.openai.com/api-keys")
        messagebox.showinfo("API Key", "Página aberta no navegador!\n\n1. Faça login na OpenAI\n2. Clique 'Create new secret key'\n3. Copie a chave gerada\n4. Cole no aplicativo")
    
    def ask_for_api_key(self):
        """Solicita a API key da OpenAI ao usuário"""
        api_key = tk.simpledialog.askstring(
            config.DIALOG_API_KEY_TITLE,
            config.DIALOG_API_KEY_MESSAGE + "\n\n(A chave será salva para próximas execuções)",
            show='*'
        )
        
        if api_key:
            self.api_key = api_key.strip()
            if self.save_api_key():
                self.status_var.set("API Key configurada - Pronto para gravar")
            else:
                self.status_var.set("API Key configurada (não salva) - Pronto para gravar")
        else:
            messagebox.showerror("Erro", config.ERROR_API_KEY_REQUIRED)
            self.root.quit()
    
    def toggle_recording(self):
        """Alterna entre gravar e parar gravação"""
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        """Inicia a gravação de áudio"""
        try:
            self.recording = True
            self.audio_data = []
            
            # Atualizar UI
            self.record_button.config(text=config.BUTTON_STOP, style="Stop.TButton")
            self.status_var.set(config.STATUS_RECORDING)
            self.text_area.delete(1.0, tk.END)
            self.copy_button.config(state="disabled")
            
            # Iniciar gravação em thread separada
            self.recording_thread = threading.Thread(target=self._record_audio)
            self.recording_thread.start()
            
        except Exception as e:
            messagebox.showerror("Erro", config.ERROR_RECORDING_START.format(str(e)))
            self.recording = False
    
    def _record_audio(self):
        """Função de gravação de áudio executada em thread separada"""
        try:
            def audio_callback(indata, frames, time, status):
                if self.recording:
                    self.audio_data.append(indata.copy())
            
            with sd.InputStream(callback=audio_callback, 
                              samplerate=self.sample_rate, 
                              channels=config.CHANNELS, 
                              dtype=config.AUDIO_FORMAT):
                while self.recording:
                    sd.sleep(100)  # Pequena pausa para não sobrecarregar
                    
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", config.ERROR_RECORDING_AUDIO.format(str(e))))
    
    def stop_recording(self):
        """Para a gravação e processa o áudio"""
        self.recording = False
        
        # Atualizar UI
        self.record_button.config(text=config.BUTTON_RECORD, style="Record.TButton")
        self.status_var.set(config.STATUS_PROCESSING)
        
        # Processar áudio em thread separada
        processing_thread = threading.Thread(target=self._process_audio)
        processing_thread.start()
    
    def _process_audio(self):
        """Processa o áudio gravado e envia para transcrição"""
        try:
            if not self.audio_data:
                self.root.after(0, lambda: self.status_var.set(config.STATUS_NO_AUDIO))
                return
            
            # Concatenar dados de áudio
            audio_array = np.concatenate(self.audio_data, axis=0)
            
            # Salvar arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix=config.TEMP_FILE_SUFFIX) as tmp_file:
                self.temp_file = tmp_file.name
                sf.write(self.temp_file, audio_array, self.sample_rate)
            
            # Enviar para transcrição
            self.root.after(0, lambda: self.status_var.set(config.STATUS_TRANSCRIBING))
            self._transcribe_audio()
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", config.ERROR_PROCESSING_AUDIO.format(str(e))))
            self.root.after(0, lambda: self.status_var.set(config.STATUS_ERROR_PROCESSING))
    
    def _transcribe_audio(self):
        """Envia áudio para API da OpenAI e obtém transcrição"""
        try:
            if not self.temp_file or not os.path.exists(self.temp_file):
                raise Exception(config.ERROR_NO_AUDIO_FILE)
            
            # Preparar requisição para API
            url = config.API_URL
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            with open(self.temp_file, 'rb') as audio_file:
                files = {
                    'file': ('audio.wav', audio_file, 'audio/wav'),
                    'model': (None, config.MODEL),
                    'language': (None, config.LANGUAGE)
                }
                
                response = requests.post(url, headers=headers, files=files, timeout=config.TIMEOUT)
            
            # Limpar arquivo temporário
            if config.DELETE_TEMP_FILES:
                try:
                    os.unlink(self.temp_file)
                except:
                    pass
            
            if response.status_code == 200:
                result = response.json()
                transcript = result.get('text', 'Nenhum texto detectado')
                
                # Atualizar UI no thread principal
                self.root.after(0, lambda: self._display_transcript(transcript))
            else:
                error_msg = f"Erro na API: {response.status_code}"
                try:
                    error_detail = response.json().get('error', {}).get('message', '')
                    if error_detail:
                        error_msg += f" - {error_detail}"
                except:
                    pass
                
                self.root.after(0, lambda: messagebox.showerror("Erro de API", error_msg))
                self.root.after(0, lambda: self.status_var.set(config.STATUS_ERROR_TRANSCRIPTION))
                
        except requests.exceptions.Timeout:
            self.root.after(0, lambda: messagebox.showerror("Erro", "Timeout na requisição"))
            self.root.after(0, lambda: self.status_var.set(config.STATUS_TIMEOUT))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", config.ERROR_TRANSCRIPTION.format(str(e))))
            self.root.after(0, lambda: self.status_var.set(config.STATUS_ERROR_TRANSCRIPTION))
    
    def _display_transcript(self, transcript):
        """Exibe o texto transcrito na interface"""
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, transcript)
        self.copy_button.config(state="normal")
        self.status_var.set(config.STATUS_COMPLETED.format(len(transcript)))
    
    def copy_text(self):
        """Copia o texto para a área de transferência"""
        text = self.text_area.get(1.0, tk.END).strip()
        if text:
            try:
                pyperclip.copy(text)
                self.status_var.set(config.STATUS_COPIED)
            except Exception as e:
                messagebox.showerror("Erro", config.ERROR_COPY.format(str(e)))
        else:
            messagebox.showwarning("Aviso", config.WARNING_NO_TEXT_TO_COPY)

def main():
    # Verificar dependências
    try:
        import tkinter.simpledialog
    except ImportError:
        print(config.ERROR_NO_PYTHON)
        return
    
    # Criar e executar aplicação
    root = tk.Tk()
    app = TranscriptApp(root)
    

    
    root.mainloop()

if __name__ == "__main__":
    main() 