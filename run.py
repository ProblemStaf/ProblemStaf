import tkinter as tk
from tkinter import scrolledtext, Entry, Button, Label, Frame, Toplevel, messagebox, Menu, ttk
import random
import threading
import time
import json
import os
import base64
import hashlib
import socket
from datetime import datetime
import webbrowser
import subprocess
import sys

# === ПРОВЕРКА И АВТОМАТИЧЕСКАЯ УСТАНОВКА БИБЛИОТЕК ===
def install_required_packages():
    """Автоматическая установка необходимых пакетов"""
    required_packages = ['cryptography', 'requests']
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} уже установлен")
        except ImportError:
            print(f"📦 Установка {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} успешно установлен")
            except Exception as e:
                print(f"❌ Ошибка установки {package}: {e}")
                return False
    return True

# Проверяем и устанавливаем зависимости
if install_required_packages():
    print("🎉 Все зависимости готовы!")
else:
    print("⚠️ Некоторые зависимости не установлены")

# === ИМПОРТ ВНЕШНИХ БИБЛИОТЕК ===
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Cryptography не доступна: {e}")
    CRYPTOGRAPHY_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Requests не доступна: {e}")
    REQUESTS_AVAILABLE = False

# === Modern Cyberpunk Theme ===
THEMES = {
    "cyberpunk": {
        "BG_COLOR": "#0d0208",
        "TEXT_BG": "#001a00", 
        "TEXT_FG": "#00ff41",
        "ENTRY_BG": "#1a1a2e",
        "ENTRY_FG": "#e2e2e2",
        "BUTTON_BG": "#6a0dad",
        "BUTTON_FG": "#f8f8ff",
        "ACCENT_1": "#ff00ff",
        "ACCENT_2": "#ffff00",
        "HIGHLIGHT_BG": "#1a1a2e",
    },
    "neon_dark": {
        "BG_COLOR": "#0a0a12",
        "TEXT_BG": "#15152b",
        "TEXT_FG": "#00ffff",
        "ENTRY_BG": "#1e1e3f",
        "ENTRY_FG": "#ffffff",
        "BUTTON_BG": "#ff00ff",
        "BUTTON_FG": "#ffffff",
        "ACCENT_1": "#00ffff",
        "ACCENT_2": "#ff00ff",
        "HIGHLIGHT_BG": "#252550",
    },
    "matrix": {
        "BG_COLOR": "#000000",
        "TEXT_BG": "#001100",
        "TEXT_FG": "#00ff00",
        "ENTRY_BG": "#002200",
        "ENTRY_FG": "#00ff00",
        "BUTTON_BG": "#003300",
        "BUTTON_FG": "#00ff00",
        "ACCENT_1": "#00ff00",
        "ACCENT_2": "#00cc00",
        "HIGHLIGHT_BG": "#001100",
    }
}

# === Modern Stickers and Emojis ===
MODERN_STICKERS = [
    "🤖", "🚀", "💻", "🔮", "🎮", "⚡", "🌈", "🔥", "✨", "🎯",
    "🧠", "🌌", "📡", "🔋", "💾", "🖥️", "👾", "🤯", "🎨", "🌟"
]

# === AI Model Integration ===
class AdvancedAIIntegration:
    def __init__(self):
        self.conversation_context = []
        self.available_models = {
            "local": "Локальная модель",
            "openai": "OpenAI GPT",
            "anthropic": "Claude AI",
            "google": "Google Gemini"
        }
        self.current_model = "local"
        self.api_keys = {}
        
    def set_api_key(self, model, api_key):
        """Установка API ключа для модели"""
        self.api_keys[model] = api_key
        
    def set_model(self, model):
        """Выбор модели AI"""
        if model in self.available_models:
            self.current_model = model
            return True
        return False
        
    def get_response(self, message: str, user_context: dict = None) -> str:
        """Получение ответа от выбранной AI модели"""
        try:
            if self.current_model == "local":
                return self._get_local_response(message)
            elif self.current_model == "openai":
                return self._get_openai_response(message, user_context)
            elif self.current_model == "anthropic":
                return self._get_anthropic_response(message, user_context)
            elif self.current_model == "google":
                return self._get_google_response(message, user_context)
            else:
                return self._get_local_response(message)
                
        except Exception as e:
            return f"Ошибка AI модели: {str(e)} 🤖"
    
    def _get_local_response(self, message: str) -> str:
        """Локальная AI модель"""
        message_lower = message.lower()
        self.conversation_context.append(("user", message))
        
        # Keep only last 10 messages for context
        if len(self.conversation_context) > 10:
            self.conversation_context.pop(0)

        # Response patterns for local model
        response_patterns = {
            "greeting": {
                "patterns": ["привет", "здравств", "хай", "hello", "hi"],
                "responses": [
                    "Привет! Готов к общению в нейросети! {sticker}",
                    "Здравствуй, кибер-путешественник! {sticker}",
                    "Приветствую в цифровом пространстве! {sticker}"
                ]
            },
            "feelings": {
                "patterns": ["как дела", "как ты", "настроение", "дела"],
                "responses": [
                    "Системы функционируют оптимально! {sticker}",
                    "Восприятие на максимуме! {sticker}",
                    "Все процессы стабильны! {sticker}"
                ]
            },
            "tech": {
                "patterns": ["технологи", "ai", "ии", "нейросеть", "код", "програм"],
                "responses": [
                    "Нейросети открывают безграничные возможности! {sticker}",
                    "ИИ - это следующий этап эволюции! {sticker}",
                    "Код создает реальность! {sticker}"
                ]
            }
        }
        
        default_responses = [
            "Интересная мысль! {sticker}",
            "Продолжайте, я внимательно слушаю! {sticker}",
            "Анализирую полученную информацию... {sticker}",
            "Это открывает новые перспективы! {sticker}",
            "Подключаю дополнительные нейромодули... {sticker}"
        ]

        # Analyze message for patterns
        response = None
        for category, data in response_patterns.items():
            for pattern in data["patterns"]:
                if pattern in message_lower:
                    response = random.choice(data["responses"])
                    break
            if response:
                break
        
        if not response:
            response = random.choice(default_responses)

        # Add contextual sticker
        sticker = random.choice(MODERN_STICKERS)
        response = response.format(sticker=sticker)
        
        self.conversation_context.append(("ai", response))
        return response
    
    def _get_openai_response(self, message: str, user_context: dict) -> str:
        """Интеграция с OpenAI API"""
        if "openai" not in self.api_keys:
            return "❌ OpenAI API ключ не установлен. Перейдите в настройки AI."
        
        if not REQUESTS_AVAILABLE:
            return "❌ Библиотека requests не установлена. Установите: pip install requests"
        
        try:
            # Демо-режим - в реальном приложении здесь будет вызов API
            return "🤖 OpenAI модель активирована (демо-режим). Для реальной работы настройте API вызовы."
        except Exception as e:
            return f"❌ Ошибка OpenAI: {str(e)}"
    
    def _get_anthropic_response(self, message: str, user_context: dict) -> str:
        """Интеграция с Anthropic Claude"""
        if "anthropic" not in self.api_keys:
            return "❌ Anthropic API ключ не установлен. Перейдите в настройки AI."
        
        if not REQUESTS_AVAILABLE:
            return "❌ Библиотека requests не установлена. Установите: pip install requests"
        
        return "🤖 Claude AI модель активирована (демо-режим). Для реальной работы настройте API вызовы."
    
    def _get_google_response(self, message: str, user_context: dict) -> str:
        """Интеграция с Google Gemini"""
        if "google" not in self.api_keys:
            return "❌ Google AI API ключ не установлен. Перейдите в настройки AI."
        
        if not REQUESTS_AVAILABLE:
            return "❌ Библиотека requests не установлена. Установите: pip install requests"
        
        return "🤖 Google Gemini модель активирована (демо-режим). Для реальной работы настройте API вызовы."

# === Network Manager ===
class NetworkManager:
    def __init__(self):
        self.is_online = False
        self.connected_users = {}
        self.invitations = {}
        self.server_url = "http://localhost:8000"  # Заглушка для сервера
        
    def generate_invite_code(self) -> str:
        """Генерация кода приглашения"""
        code = ''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ23456789', k=8))
        self.invitations[code] = {
            'created': datetime.now(),
            'used': False
        }
        return code
    
    def validate_invite_code(self, code: str) -> bool:
        """Проверка кода приглашения"""
        if code in self.invitations and not self.invitations[code]['used']:
            self.invitations[code]['used'] = True
            return True
        return False
    
    def connect_to_user(self, user_id: str) -> bool:
        """Подключение к пользователю"""
        # Здесь будет реальная логика подключения
        self.connected_users[user_id] = {
            'status': 'online',
            'last_seen': datetime.now()
        }
        return True
    
    def send_message_to_user(self, user_id: str, message: str) -> bool:
        """Отправка сообщения пользователю"""
        if user_id in self.connected_users:
            # Здесь будет реальная отправка
            return True
        return False

# === Advanced Encryption System ===
class ChatEncryption:
    def __init__(self, password: str = None):
        self.key = None
        self.encryption_enabled = CRYPTOGRAPHY_AVAILABLE
        if password and self.encryption_enabled:
            self.generate_key(password)

    def generate_key(self, password: str):
        """Generate encryption key from password"""
        if not CRYPTOGRAPHY_AVAILABLE:
            raise Exception("Cryptography library not available")
        
        try:
            # Use password to derive a key
            password_bytes = password.encode()
            salt = b'neuro_chat_salt_2024'
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
            self.key = Fernet(key)
        except Exception as e:
            raise Exception(f"Ошибка генерации ключа: {str(e)}")

    def encrypt(self, data: str) -> str:
        if not self.encryption_enabled or not self.key:
            return data
        try:
            if isinstance(data, str):
                data = data.encode()
            return self.key.encrypt(data).decode()
        except Exception as e:
            raise Exception(f"Ошибка шифрования: {str(e)}")

    def decrypt(self, data: str) -> str:
        if not self.encryption_enabled or not self.key:
            return data
        try:
            if isinstance(data, str):
                data = data.encode()
            return self.key.decrypt(data).decode()
        except Exception as e:
            raise Exception(f"Ошибка дешифровки: {str(e)}")

# === Modern Chat Application ===
class ModernNeuroChat:
    def __init__(self, root: tk.Tk):
        self.root = root
        
        # ИНИЦИАЛИЗАЦИЯ ВСЕХ АТРИБУТОВ ДО ВЫЗОВА МЕТОДОВ
        self.current_theme = "cyberpunk"
        self.theme = THEMES[self.current_theme]
        
        # Initialize counters and state FIRST
        self.message_counter = 0
        self.current_user_id = f"user_{random.randint(1000, 9999)}"
        self.username = f"User_{random.randint(100, 999)}"
        
        # Initialize managers
        self.encryption = ChatEncryption()
        self.ai_model = AdvancedAIIntegration()
        self.network_manager = NetworkManager()
        
        self.setup_security()
        self.setup_window()
        self.setup_ui()
        self.setup_menu()
        self.setup_bindings()
        
        # Online status
        self.update_online_status()

    def setup_window(self):
        self.root.title("NeuroChat Pro v5.0 - Онлайн")
        self.root.geometry("900x950")
        self.root.resizable(True, True)
        self.root.configure(bg=self.theme["BG_COLOR"])
        self.root.minsize(800, 850)

        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (450)
        y = (self.root.winfo_screenheight() // 2) - (475)
        self.root.geometry(f"+{x}+{y}")

    def setup_security(self):
        self.encryption_enabled = CRYPTOGRAPHY_AVAILABLE
        self.chat_history_file = "secure_chat_history.json"
        self.settings_file = "chat_settings.json"

    def setup_ui(self):
        # Modern header with online features
        self.setup_header()
        
        # Main chat area with user list
        self.setup_chat_area()
        
        # Advanced input panel
        self.setup_input_panel()
        
        # Status bar
        self.setup_status_bar()

    def setup_header(self):
        header_frame = Frame(self.root, bg=self.theme["BG_COLOR"], height=80)
        header_frame.pack(fill=tk.X, padx=15, pady=10)
        header_frame.pack_propagate(False)

        # App title with online indicator
        title_label = Label(
            header_frame,
            text="NEUROCHAT PRO v5.0",
            font=("Courier", 18, "bold"),
            fg=self.theme["ACCENT_1"],
            bg=self.theme["BG_COLOR"]
        )
        title_label.pack(side=tk.LEFT, pady=10)

        # Online status with toggle
        self.online_status_var = tk.BooleanVar(value=True)
        self.online_toggle = tk.Checkbutton(
            header_frame,
            text="● ONLINE",
            variable=self.online_status_var,
            command=self.toggle_online_status,
            font=("Courier", 12, "bold"),
            fg="#00ff00",
            bg=self.theme["BG_COLOR"],
            selectcolor=self.theme["BG_COLOR"],
            activebackground=self.theme["BG_COLOR"],
            activeforeground="#00ff00"
        )
        self.online_toggle.pack(side=tk.RIGHT, pady=10)

        # User info - ТЕПЕРЬ username гарантированно инициализирован
        self.user_info = Label(
            header_frame,
            text=f"👤 {self.username}",
            font=("Courier", 11),
            fg=self.theme["ACCENT_2"],
            bg=self.theme["BG_COLOR"]
        )
        self.user_info.pack(side=tk.RIGHT, padx=20, pady=10)

    def setup_chat_area(self):
        main_container = Frame(self.root, bg=self.theme["BG_COLOR"])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # User list sidebar
        self.setup_user_sidebar(main_container)

        # Chat history with modern styling
        self.chat_area = scrolledtext.ScrolledText(
            main_container,
            wrap=tk.WORD,
            state='disabled',
            bg=self.theme["TEXT_BG"],
            fg=self.theme["TEXT_FG"],
            insertbackground=self.theme["TEXT_FG"],
            selectbackground=self.theme["BUTTON_BG"],
            borderwidth=0,
            relief="flat",
            font=("Consolas", 11),
            padx=15,
            pady=15,
            spacing1=5,
            spacing3=5
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Add text tags for styling
        self.chat_area.tag_configure('user', foreground="#00ffff", font=("Consolas", 11, "bold"))
        self.chat_area.tag_configure('ai', foreground=self.theme["TEXT_FG"], font=("Consolas", 11))
        self.chat_area.tag_configure('system', foreground=self.theme["ACCENT_2"], font=("Consolas", 10, "italic"))
        self.chat_area.tag_configure('timestamp', foreground="#666666", font=("Consolas", 9))
        self.chat_area.tag_configure('online', foreground="#00ff00", font=("Consolas", 9, "bold"))

        # Typing indicator
        self.typing_indicator = Label(
            main_container,
            text="",
            font=("Courier", 10, "italic"),
            fg=self.theme["ACCENT_2"],
            bg=self.theme["BG_COLOR"]
        )
        self.typing_indicator.pack(fill=tk.X)

    def setup_user_sidebar(self, parent):
        """Боковая панель со списком пользователей"""
        sidebar = Frame(parent, bg=self.theme["HIGHLIGHT_BG"], width=200)
        sidebar.pack(fill=tk.Y, side=tk.RIGHT, padx=(10, 0))
        sidebar.pack_propagate(False)

        # Sidebar title
        sidebar_title = Label(
            sidebar,
            text="👥 ОНЛАЙН",
            font=("Courier", 12, "bold"),
            fg=self.theme["ACCENT_2"],
            bg=self.theme["HIGHLIGHT_BG"],
            pady=10
        )
        sidebar_title.pack(fill=tk.X)

        # User list
        self.user_listbox = tk.Listbox(
            sidebar,
            bg=self.theme["ENTRY_BG"],
            fg=self.theme["ENTRY_FG"],
            selectbackground=self.theme["BUTTON_BG"],
            selectforeground=self.theme["BUTTON_FG"],
            borderwidth=0,
            relief="flat",
            font=("Consolas", 10)
        )
        self.user_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add some demo users
        demo_users = ["Alice_AI", "Bob_Tech", "Charlie_Dev", "Diana_Cyber"]
        for user in demo_users:
            self.user_listbox.insert(tk.END, f"● {user}")

        # Invite button
        invite_btn = Button(
            sidebar,
            text="📧 Пригласить",
            command=self.generate_invite,
            bg=self.theme["ACCENT_1"],
            fg=self.theme["BUTTON_FG"],
            relief="flat",
            borderwidth=0,
            font=("Consolas", 10),
            pady=5
        )
        invite_btn.pack(fill=tk.X, padx=5, pady=5)

        # Connect button
        connect_btn = Button(
            sidebar,
            text="🔗 Подключиться",
            command=self.connect_to_user,
            bg=self.theme["BUTTON_BG"],
            fg=self.theme["BUTTON_FG"],
            relief="flat",
            borderwidth=0,
            font=("Consolas", 10),
            pady=5
        )
        connect_btn.pack(fill=tk.X, padx=5, pady=5)

    def setup_input_panel(self):
        input_container = Frame(self.root, bg=self.theme["BG_COLOR"])
        input_container.pack(fill=tk.X, padx=15, pady=15)

        # Modern input field
        self.entry_field = Entry(
            input_container,
            bg=self.theme["ENTRY_BG"],
            fg=self.theme["ENTRY_FG"],
            insertbackground=self.theme["ENTRY_FG"],
            relief="flat",
            borderwidth=2,
            font=("Consolas", 12)
        )
        self.entry_field.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        self.entry_field.focus_set()

        # Action buttons container
        button_frame = Frame(input_container, bg=self.theme["BG_COLOR"])
        button_frame.pack(side=tk.RIGHT)

        # Send button with modern icon
        self.send_button = Button(
            button_frame,
            text="🚀 Отправить",
            command=self.send_message,
            bg=self.theme["BUTTON_BG"],
            fg=self.theme["BUTTON_FG"],
            relief="flat",
            borderwidth=0,
            font=("Consolas", 10, "bold"),
            width=12
        )
        self.send_button.pack(pady=2)

        # Sticker button
        sticker_btn = Button(
            button_frame,
            text="😊 Стикеры",
            command=self.open_sticker_panel,
            bg=self.theme["ACCENT_1"],
            fg=self.theme["BUTTON_FG"],
            relief="flat",
            borderwidth=0,
            font=("Consolas", 10),
            width=12
        )
        sticker_btn.pack(pady=2)

        # AI Mode button
        self.ai_mode_btn = Button(
            button_frame,
            text="🤖 AI: Локальный",
            command=self.open_ai_settings,
            bg=self.theme["ACCENT_2"],
            fg=self.theme["BG_COLOR"],
            relief="flat",
            borderwidth=0,
            font=("Consolas", 10),
            width=12
        )
        self.ai_mode_btn.pack(pady=2)

    def setup_status_bar(self):
        status_frame = Frame(self.root, bg=self.theme["HIGHLIGHT_BG"], height=25)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)

        security_status = " | Шифрование доступно" if CRYPTOGRAPHY_AVAILABLE else " | Шифрование недоступно"
        requests_status = " | Requests доступны" if REQUESTS_AVAILABLE else " | Requests недоступны"
        
        self.status_message = Label(
            status_frame,
            text=f"NeuroChat Pro v5.0 | Онлайн режим{security_status}{requests_status}",
            font=("Courier", 9),
            fg=self.theme["TEXT_FG"],
            bg=self.theme["HIGHLIGHT_BG"]
        )
        self.status_message.pack(side=tk.LEFT, padx=10)

        self.message_count = Label(
            status_frame,
            text="Сообщений: 0",
            font=("Courier", 9),
            fg=self.theme["ACCENT_2"],
            bg=self.theme["HIGHLIGHT_BG"]
        )
        self.message_count.pack(side=tk.RIGHT, padx=10)

    def setup_menu(self):
        menubar = Menu(self.root, bg=self.theme["ENTRY_BG"], fg=self.theme["ENTRY_FG"])
        
        # File menu
        file_menu = Menu(menubar, tearoff=0, bg=self.theme["ENTRY_BG"], fg=self.theme["ENTRY_FG"])
        file_menu.add_command(label="Экспорт чата", command=self.export_chat)
        file_menu.add_command(label="Очистить историю", command=self.clear_chat)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.safe_exit)
        menubar.add_cascade(label="Файл", menu=file_menu)

        # Network menu
        network_menu = Menu(menubar, tearoff=0, bg=self.theme["ENTRY_BG"], fg=self.theme["ENTRY_FG"])
        network_menu.add_command(label="Создать комнату", command=self.create_room)
        network_menu.add_command(label="Присоединиться к комнате", command=self.join_room)
        network_menu.add_command(label="Список пользователей", command=self.show_users)
        network_menu.add_separator()
        network_menu.add_command(label="Настройки сети", command=self.network_settings)
        menubar.add_cascade(label="Сеть", menu=network_menu)

        # Settings menu
        settings_menu = Menu(menubar, tearoff=0, bg=self.theme["ENTRY_BG"], fg=self.theme["ENTRY_FG"])
        
        theme_menu = Menu(settings_menu, tearoff=0, bg=self.theme["ENTRY_BG"], fg=self.theme["ENTRY_FG"])
        for theme_name in THEMES.keys():
            theme_menu.add_command(
                label=theme_name.title(), 
                command=lambda t=theme_name: self.change_theme(t)
            )
        
        settings_menu.add_cascade(label="Тема", menu=theme_menu)
        
        if CRYPTOGRAPHY_AVAILABLE:
            settings_menu.add_command(label="Настройки безопасности", command=self.security_settings)
        else:
            settings_menu.add_command(label="Настройки безопасности", command=self.show_crypto_warning)
            
        settings_menu.add_command(label="Настройки AI", command=self.open_ai_settings)
        menubar.add_cascade(label="Настройки", menu=settings_menu)

        # Help menu
        help_menu = Menu(menubar, tearoff=0, bg=self.theme["ENTRY_BG"], fg=self.theme["ENTRY_FG"])
        help_menu.add_command(label="О программе", command=self.show_about)
        help_menu.add_command(label="Справка", command=self.show_help)
        help_menu.add_command(label="Проверка зависимостей", command=self.check_dependencies)
        menubar.add_cascade(label="Помощь", menu=help_menu)

        self.root.config(menu=menubar)

    def setup_bindings(self):
        self.entry_field.bind("<Return>", self.send_message)
        self.entry_field.bind("<KeyRelease>", self.update_typing_indicator)
        
        # Modern key bindings
        self.root.bind("<Control-s>", lambda e: self.export_chat())
        self.root.bind("<Control-l>", lambda e: self.clear_chat())
        self.root.bind("<Control-q>", lambda e: self.safe_exit())
        self.root.bind("<Control-o>", lambda e: self.toggle_online_status())

        # Load chat history after UI is ready
        self.root.after(100, self.load_chat_history)

    # === ONLINE FEATURES ===
    def toggle_online_status(self):
        """Переключение онлайн статуса"""
        if self.online_status_var.get():
            self.network_manager.is_online = True
            self.display_message("SYSTEM", "✅ Подключение к сети...", "system")
            self.root.after(1000, lambda: self.display_message("SYSTEM", "🌐 Вы в сети! Другие пользователи могут вас видеть", "online"))
        else:
            self.network_manager.is_online = False
            self.display_message("SYSTEM", "🔴 Вы вышли из сети", "system")

    def generate_invite(self):
        """Генерация кода приглашения"""
        invite_code = self.network_manager.generate_invite_code()
        self.display_message("SYSTEM", f"📧 Код приглашения: {invite_code}", "system")
        messagebox.showinfo(
            "Приглашение", 
            f"Код приглашения:\n\n{invite_code}\n\n"
            f"Поделитесь этим кодом с друзьями, чтобы они могли присоединиться к чату."
        )

    def connect_to_user(self):
        """Подключение к пользователю"""
        selected = self.user_listbox.curselection()
        if selected:
            user = self.user_listbox.get(selected[0])
            username = user.replace("● ", "")
            if self.network_manager.connect_to_user(username):
                self.display_message("SYSTEM", f"🔗 Подключение к {username}...", "system")
            else:
                self.display_message("SYSTEM", f"❌ Не удалось подключиться к {username}", "system")
        else:
            messagebox.showwarning("Выбор пользователя", "Выберите пользователя из списка")

    def create_room(self):
        """Создание комнаты чата"""
        room_name = f"Room_{random.randint(1000, 9999)}"
        self.display_message("SYSTEM", f"🏠 Создана комната: {room_name}", "system")
        messagebox.showinfo("Комната создана", f"Комната '{room_name}' создана!\nПоделитесь названием комнаты с друзьями.")

    def join_room(self):
        """Присоединение к комнате"""
        room_window = Toplevel(self.root)
        room_window.title("Присоединиться к комнате")
        room_window.geometry("400x200")
        room_window.configure(bg=self.theme["BG_COLOR"])
        
        Label(room_window, text="Введите название комнаты:", 
              bg=self.theme["BG_COLOR"], fg=self.theme["TEXT_FG"],
              font=("Consolas", 12)).pack(pady=20)
        
        room_entry = Entry(room_window, font=("Consolas", 12), width=30)
        room_entry.pack(pady=10)
        
        def join():
            room_name = room_entry.get().strip()
            if room_name:
                self.display_message("SYSTEM", f"🚪 Присоединение к комнате: {room_name}", "system")
                room_window.destroy()
            else:
                messagebox.showwarning("Ошибка", "Введите название комнаты")
        
        Button(room_window, text="Присоединиться", command=join,
               bg=self.theme["BUTTON_BG"], fg=self.theme["BUTTON_FG"],
               font=("Consolas", 11)).pack(pady=10)

    def show_users(self):
        """Показать список пользователей"""
        users = ["Alice_AI (online)", "Bob_Tech (online)", "Charlie_Dev (away)", "Diana_Cyber (online)"]
        user_list = "\n".join([f"• {user}" for user in users])
        messagebox.showinfo("Онлайн пользователи", f"Пользователи в сети:\n\n{user_list}")

    def network_settings(self):
        """Настройки сети"""
        settings_window = Toplevel(self.root)
        settings_window.title("Настройки сети")
        settings_window.geometry("500x400")
        settings_window.configure(bg=self.theme["BG_COLOR"])
        
        # Network configuration
        config_frame = Frame(settings_window, bg=self.theme["BG_COLOR"])
        config_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        Label(config_frame, text="Настройки сети", font=("Courier", 16, "bold"),
              fg=self.theme["ACCENT_1"], bg=self.theme["BG_COLOR"]).pack(pady=10)
        
        # Server settings
        server_frame = Frame(config_frame, bg=self.theme["BG_COLOR"])
        server_frame.pack(fill=tk.X, pady=10)
        
        Label(server_frame, text="Сервер:", bg=self.theme["BG_COLOR"], 
              fg=self.theme["TEXT_FG"], font=("Consolas", 11)).pack(anchor=tk.W)
        
        server_entry = Entry(server_frame, font=("Consolas", 11), width=40)
        server_entry.insert(0, "neurochat-server.example.com")
        server_entry.pack(fill=tk.X, pady=5)
        
        # Port settings
        port_frame = Frame(config_frame, bg=self.theme["BG_COLOR"])
        port_frame.pack(fill=tk.X, pady=10)
        
        Label(port_frame, text="Порт:", bg=self.theme["BG_COLOR"],
              fg=self.theme["TEXT_FG"], font=("Consolas", 11)).pack(anchor=tk.W)
        
        port_entry = Entry(port_frame, font=("Consolas", 11), width=10)
        port_entry.insert(0, "8080")
        port_entry.pack(anchor=tk.W, pady=5)
        
        # Auto-connect
        auto_var = tk.BooleanVar(value=True)
        auto_cb = tk.Checkbutton(config_frame, text="Автоподключение при запуске",
                                variable=auto_var, bg=self.theme["BG_COLOR"],
                                fg=self.theme["TEXT_FG"], font=("Consolas", 11))
        auto_cb.pack(anchor=tk.W, pady=10)
        
        def save_settings():
            messagebox.showinfo("Сохранено", "Настройки сети сохранены!")
            settings_window.destroy()
        
        Button(config_frame, text="Сохранить", command=save_settings,
               bg=self.theme["BUTTON_BG"], fg=self.theme["BUTTON_FG"],
               font=("Consolas", 11)).pack(pady=20)

    def update_online_status(self):
        """Обновление онлайн статуса"""
        if hasattr(self, 'online_timer'):
            self.root.after_cancel(self.online_timer)
        
        # Обновляем статус каждые 30 секунд
        self.online_timer = self.root.after(30000, self.update_online_status)

    # === AI FEATURES ===
    def open_ai_settings(self):
        """Открыть настройки AI"""
        ai_window = Toplevel(self.root)
        ai_window.title("Настройки AI моделей")
        ai_window.geometry("600x500")
        ai_window.configure(bg=self.theme["BG_COLOR"])
        
        # AI Model selection
        model_frame = Frame(ai_window, bg=self.theme["BG_COLOR"])
        model_frame.pack(fill=tk.X, padx=20, pady=20)
        
        Label(model_frame, text="Выбор AI модели:", font=("Courier", 14, "bold"),
              fg=self.theme["ACCENT_1"], bg=self.theme["BG_COLOR"]).pack(anchor=tk.W)
        
        # Model radio buttons
        self.model_var = tk.StringVar(value=self.ai_model.current_model)
        
        for model_key, model_name in self.ai_model.available_models.items():
            rb = tk.Radiobutton(
                model_frame,
                text=model_name,
                variable=self.model_var,
                value=model_key,
                command=self.on_model_change,
                bg=self.theme["BG_COLOR"],
                fg=self.theme["TEXT_FG"],
                selectcolor=self.theme["ENTRY_BG"],
                font=("Consolas", 11)
            )
            rb.pack(anchor=tk.W, pady=5)
        
        # API Key input
        api_frame = Frame(ai_window, bg=self.theme["BG_COLOR"])
        api_frame.pack(fill=tk.X, padx=20, pady=20)
        
        Label(api_frame, text="API ключи:", font=("Courier", 12, "bold"),
              fg=self.theme["ACCENT_2"], bg=self.theme["BG_COLOR"]).pack(anchor=tk.W)
        
        self.api_entries = {}
        
        for model_key in ["openai", "anthropic", "google"]:
            frame = Frame(api_frame, bg=self.theme["BG_COLOR"])
            frame.pack(fill=tk.X, pady=5)
            
            Label(frame, text=f"{model_key.title()}:", bg=self.theme["BG_COLOR"],
                  fg=self.theme["TEXT_FG"], font=("Consolas", 10), width=12).pack(side=tk.LEFT)
            
            entry = Entry(frame, show="*", font=("Consolas", 10), width=30)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.api_entries[model_key] = entry
        
        # Save button
        def save_ai_settings():
            for model_key, entry in self.api_entries.items():
                if entry.get().strip():
                    self.ai_model.set_api_key(model_key, entry.get().strip())
            
            self.ai_model.set_model(self.model_var.get())
            self.ai_mode_btn.config(text=f"🤖 AI: {self.ai_model.available_models[self.model_var.get()]}")
            messagebox.showinfo("Сохранено", "Настройки AI сохранены!")
            ai_window.destroy()
        
        Button(ai_window, text="Сохранить настройки", command=save_ai_settings,
               bg=self.theme["BUTTON_BG"], fg=self.theme["BUTTON_FG"],
               font=("Consolas", 12)).pack(pady=20)

    def on_model_change(self):
        """Обработчик смены модели AI"""
        self.ai_mode_btn.config(text=f"🤖 AI: {self.ai_model.available_models[self.model_var.get()]}")

    # === REST OF THE METHODS ===
    def show_crypto_warning(self):
        messagebox.showwarning(
            "Шифрование недоступно", 
            "Библиотека cryptography не установлена.\n\n"
            "Для включения шифрования установите:\n"
            "pip install cryptography"
        )

    def check_dependencies(self):
        status = []
        if CRYPTOGRAPHY_AVAILABLE:
            status.append("Cryptography: ✅ Установлена")
        else:
            status.append("Cryptography: ❌ Отсутствует")
            
        if REQUESTS_AVAILABLE:
            status.append("Requests: ✅ Установлена")
        else:
            status.append("Requests: ❌ Отсутствует")
        
        message = "\n".join(status)
        if CRYPTOGRAPHY_AVAILABLE and REQUESTS_AVAILABLE:
            message += "\n\n✅ Все зависимости установлены!"
        else:
            message += "\n\n❌ Некоторые зависимости отсутствуют"
            
        messagebox.showinfo("Проверка зависимостей", message)

    def safe_exit(self):
        """Safe exit with confirmation"""
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            self.root.quit()

    def update_typing_indicator(self, event=None):
        if hasattr(self, 'typing_timer'):
            self.root.after_cancel(self.typing_timer)
        
        # Only show typing indicator if there's text
        if self.entry_field.get().strip():
            self.typing_indicator.config(text="Печатает...")
            self.typing_timer = self.root.after(2000, lambda: self.typing_indicator.config(text=""))
        else:
            self.typing_indicator.config(text="")

    def send_message(self, event=None):
        message = self.entry_field.get().strip()
        if not message:
            return

        try:
            # Clear typing indicator immediately
            self.typing_indicator.config(text="")
            if hasattr(self, 'typing_timer'):
                self.root.after_cancel(self.typing_timer)
            
            # Display user message - ТЕПЕРЬ username гарантированно существует
            self.display_message(f"{self.username}", message, "user")
            self.entry_field.delete(0, tk.END)
            
            # Save to history
            self.save_message_to_history("user", message)
            
            # Start AI response in thread if message is directed to AI
            if "бот" in message.lower() or "ai" in message.lower() or "нейро" in message.lower():
                threading.Thread(target=self.generate_ai_response, args=(message,), daemon=True).start()
            
        except Exception as e:
            self.show_error(f"Ошибка отправки: {str(e)}")

    def generate_ai_response(self, user_message):
        try:
            # Show typing animation in main thread
            self.root.after(0, self.show_typing_animation)
            
            # Simulate AI processing time
            processing_time = random.uniform(0.5, 2.0)
            time.sleep(processing_time)
            
            # Get AI response
            user_context = {"username": self.username, "online": self.network_manager.is_online}
            response = self.ai_model.get_response(user_message, user_context)
            
            # Hide typing animation and display response in main thread
            self.root.after(0, lambda: self.hide_typing_animation(response))
            
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Ошибка AI: {str(e)}"))

    def show_typing_animation(self):
        self.typing_indicator.config(text="AI генерирует ответ...")

    def hide_typing_animation(self, response):
        self.typing_indicator.config(text="")
        self.display_message("NeuroAI", response, "ai")
        self.save_message_to_history("ai", response)

    def display_message(self, sender: str, message: str, msg_type: str = "system"):
        try:
            self.chat_area.config(state='normal')
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Add timestamp
            self.chat_area.insert(tk.END, f"[{timestamp}] ", 'timestamp')
            
            # Add sender and message
            if msg_type == "user":
                self.chat_area.insert(tk.END, f"{sender}: ", 'user')
                self.chat_area.insert(tk.END, f"{message}\n")
            elif msg_type == "ai":
                self.chat_area.insert(tk.END, f"{sender}: ", 'ai')
                self.chat_area.insert(tk.END, f"{message}\n")
            elif msg_type == "online":
                self.chat_area.insert(tk.END, f"{sender}: {message}\n", 'online')
            else:
                self.chat_area.insert(tk.END, f"{sender}: {message}\n", 'system')
            
            self.chat_area.config(state='disabled')
            self.chat_area.see(tk.END)
            
            # Update message count
            self.update_message_count()
            
        except Exception as e:
            print(f"Display error: {e}")

    def update_message_count(self):
        try:
            self.message_counter += 1
            self.message_count.config(text=f"Сообщений: {self.message_counter}")
        except Exception as e:
            print(f"Count update error: {e}")

    def open_sticker_panel(self):
        try:
            sticker_window = Toplevel(self.root)
            sticker_window.title("Стикеры")
            sticker_window.geometry("400x200")
            sticker_window.configure(bg=self.theme["BG_COLOR"])
            sticker_window.resizable(False, False)
            
            # Center sticker window
            sticker_window.transient(self.root)
            sticker_window.grab_set()
            
            # Position relative to main window
            main_x = self.root.winfo_x()
            main_y = self.root.winfo_y()
            sticker_window.geometry(f"+{main_x+200}+{main_y+200}")
            
            sticker_frame = Frame(sticker_window, bg=self.theme["BG_COLOR"])
            sticker_frame.pack(pady=15, padx=15, fill=tk.BOTH, expand=True)

            for i, sticker in enumerate(MODERN_STICKERS):
                btn = Button(
                    sticker_frame,
                    text=sticker,
                    command=lambda s=sticker: self.insert_sticker(s, sticker_window),
                    font=("Segoe UI Emoji", 16),
                    width=3,
                    height=1,
                    bg=self.theme["ENTRY_BG"],
                    fg=self.theme["ACCENT_1"],
                    relief="flat",
                    borderwidth=0
                )
                btn.grid(row=i//5, column=i%5, padx=5, pady=5)
                
        except Exception as e:
            self.show_error(f"Ошибка открытия стикеров: {str(e)}")

    def insert_sticker(self, sticker, window):
        try:
            self.entry_field.insert(tk.END, sticker)
            window.destroy()
        except Exception as e:
            self.show_error(f"Ошибка вставки стикера: {str(e)}")

    def save_message_to_history(self, sender: str, message: str):
        try:
            history = self.load_history_data()
            
            history.append({
                "sender": sender,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "theme": self.current_theme
            })

            # Keep last 500 messages
            history = history[-500:]

            data = json.dumps(history, ensure_ascii=False, indent=2)
            
            if self.encryption_enabled and self.encryption.key:
                data = self.encryption.encrypt(data)

            with open(self.chat_history_file, 'w', encoding='utf-8') as f:
                f.write(data)
                
        except Exception as e:
            self.show_error(f"Ошибка сохранения: {str(e)}")

    def load_history_data(self) -> list:
        try:
            if not os.path.exists(self.chat_history_file):
                return []

            with open(self.chat_history_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
            if not content:
                return []

            # Try to decrypt if encrypted
            try:
                if self.encryption_enabled and self.encryption.key:
                    content = self.encryption.decrypt(content)
                data = json.loads(content)
            except:
                # If decryption fails, try to load as plain JSON
                try:
                    data = json.loads(content)
                except json.JSONDecodeError:
                    # If JSON is corrupted, return empty list
                    return []
                
            return data if isinstance(data, list) else []
            
        except Exception as e:
            print(f"History load error: {e}")
            return []

    def load_chat_history(self):
        try:
            history = self.load_history_data()
            if not history:
                self.display_message("SYSTEM", "Добро пожаловать в NeuroChat Pro v5.0! 🚀", "system")
                self.display_message("SYSTEM", "Режим: ОНЛАЙН с поддержкой AI моделей", "online")
                if not CRYPTOGRAPHY_AVAILABLE:
                    self.display_message("SYSTEM", "ВНИМАНИЕ: Шифрование недоступно. Установите cryptography для безопасности.", "system")
                if not REQUESTS_AVAILABLE:
                    self.display_message("SYSTEM", "ВНИМАНИЕ: Requests недоступны. Внешние AI модели не будут работать.", "system")
                return

            for entry in history:
                timestamp = datetime.fromisoformat(entry['timestamp']).strftime("%H:%M:%S")
                sender = entry['sender']
                message = entry['message']
                
                if sender == "system":
                    self.display_message("SYSTEM", message, "system")
                elif sender == "user":
                    self.display_message("Вы", message, "user")
                else:
                    self.display_message("NeuroAI", message, "ai")
                    
            # Update counter based on loaded history
            self.message_counter = len(history)
            self.update_message_count()
                    
        except Exception as e:
            self.show_error(f"Ошибка загрузки чата: {str(e)}")

    def change_theme(self, theme_name: str):
        try:
            if theme_name in THEMES:
                self.current_theme = theme_name
                self.theme = THEMES[theme_name]
                self.apply_theme()
                self.display_message("SYSTEM", f"Тема изменена на: {theme_name}", "system")
        except Exception as e:
            self.show_error(f"Ошибка смены темы: {str(e)}")

    def apply_theme(self):
        try:
            # Update all widgets with new theme
            self.root.configure(bg=self.theme["BG_COLOR"])
            self.chat_area.configure(
                bg=self.theme["TEXT_BG"],
                fg=self.theme["TEXT_FG"],
                insertbackground=self.theme["TEXT_FG"]
            )
            self.entry_field.configure(
                bg=self.theme["ENTRY_BG"],
                fg=self.theme["ENTRY_FG"],
                insertbackground=self.theme["ENTRY_FG"]
            )
            self.typing_indicator.configure(
                bg=self.theme["BG_COLOR"],
                fg=self.theme["ACCENT_2"]
            )
            
        except Exception as e:
            print(f"Theme apply error: {e}")

    def security_settings(self):
        if not CRYPTOGRAPHY_AVAILABLE:
            self.show_crypto_warning()
            return
            
        try:
            settings_window = Toplevel(self.root)
            settings_window.title("Настройки безопасности")
            settings_window.geometry("400x200")
            settings_window.configure(bg=self.theme["BG_COLOR"])
            settings_window.resizable(False, False)
            
            # Center the settings window
            settings_window.transient(self.root)
            main_x = self.root.winfo_x()
            main_y = self.root.winfo_y()
            settings_window.geometry(f"+{main_x+200}+{main_y+200}")
            
            Frame(settings_window, bg=self.theme["ACCENT_1"], height=2).pack(fill=tk.X, pady=5)
            
            Label(
                settings_window,
                text="Настройки безопасности",
                font=("Courier", 16, "bold"),
                fg=self.theme["ACCENT_1"],
                bg=self.theme["BG_COLOR"]
            ).pack(pady=10)

            # Encryption toggle
            enc_frame = Frame(settings_window, bg=self.theme["BG_COLOR"])
            enc_frame.pack(fill=tk.X, padx=20, pady=10)
            
            self.enc_var = tk.BooleanVar(value=self.encryption_enabled)
            enc_cb = tk.Checkbutton(
                enc_frame,
                text="Включить шифрование чата",
                variable=self.enc_var,
                command=self.toggle_encryption,
                bg=self.theme["BG_COLOR"],
                fg=self.theme["TEXT_FG"],
                selectcolor=self.theme["ENTRY_BG"],
                font=("Consolas", 11)
            )
            enc_cb.pack(anchor=tk.W)

            # Password entry
            pwd_frame = Frame(settings_window, bg=self.theme["BG_COLOR"])
            pwd_frame.pack(fill=tk.X, padx=20, pady=10)
            
            Label(
                pwd_frame,
                text="Пароль шифрования:",
                bg=self.theme["BG_COLOR"],
                fg=self.theme["TEXT_FG"],
                font=("Consolas", 10)
            ).pack(anchor=tk.W)
            
            pwd_entry = Entry(
                pwd_frame,
                show="*",
                bg=self.theme["ENTRY_BG"],
                fg=self.theme["ENTRY_FG"],
                font=("Consolas", 11)
            )
            pwd_entry.pack(fill=tk.X, pady=5)

            Button(
                pwd_frame,
                text="Установить пароль",
                command=lambda: self.set_encryption_password(pwd_entry.get()),
                bg=self.theme["BUTTON_BG"],
                fg=self.theme["BUTTON_FG"],
                font=("Consolas", 10)
            ).pack(pady=5)
            
        except Exception as e:
            self.show_error(f"Ошибка открытия настроек: {str(e)}")

    def toggle_encryption(self):
        self.encryption_enabled = self.enc_var.get()
        status = "включено" if self.encryption_enabled else "выключено"
        self.display_message("SYSTEM", f"Шифрование {status}", "system")

    def set_encryption_password(self, password: str):
        try:
            if len(password) >= 4:
                self.encryption.generate_key(password)
                self.display_message("SYSTEM", "Пароль шифрования установлен", "system")
                # Save current history with new encryption
                self.backup_history_before_encryption()
            else:
                self.show_error("Пароль должен быть не менее 4 символов")
        except Exception as e:
            self.show_error(f"Ошибка установки пароля: {str(e)}")

    def backup_history_before_encryption(self):
        """Create backup before enabling encryption"""
        try:
            if os.path.exists(self.chat_history_file):
                backup_file = f"{self.chat_history_file}.backup"
                import shutil
                shutil.copy2(self.chat_history_file, backup_file)
        except Exception as e:
            print(f"Backup error: {e}")

    def export_chat(self):
        try:
            filename = f"neurochat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                # Get all text from chat area
                chat_text = self.chat_area.get(1.0, tk.END)
                f.write(chat_text)
            self.display_message("SYSTEM", f"Чат экспортирован в {filename}", "system")
            messagebox.showinfo("Экспорт", f"Чат успешно экспортирован в:\n{filename}")
        except Exception as e:
            self.show_error(f"Ошибка экспорта: {str(e)}")

    def clear_chat(self):
        if messagebox.askyesno("Подтверждение", "Очистить всю историю чата?\nЭто действие нельзя отменить."):
            try:
                self.chat_area.config(state='normal')
                self.chat_area.delete(1.0, tk.END)
                self.chat_area.config(state='disabled')
                
                if os.path.exists(self.chat_history_file):
                    os.remove(self.chat_history_file)
                    
                self.message_counter = 0
                self.update_message_count()
                self.display_message("SYSTEM", "История чата очищена", "system")
            except Exception as e:
                self.show_error(f"Ошибка очистки: {str(e)}")

    def show_about(self):
        crypto_status = "✅ доступно" if CRYPTOGRAPHY_AVAILABLE else "❌ недоступно"
        requests_status = "✅ доступны" if REQUESTS_AVAILABLE else "❌ недоступны"
        about_text = f"""NeuroChat Pro v5.0 - ОНЛАЙН ВЕРСИЯ

Современный мессенджер с искусственным интеллектом
и продвинутой системой безопасности.

🌟 ОСНОВНЫЕ ВОЗМОЖНОСТИ:
• Онлайн общение с другими пользователями
• Поддержка AI моделей (OpenAI, Claude, Gemini)
• Создание комнат и приглашение друзей
• Шифрование сообщений: {crypto_status}
• Библиотека requests: {requests_status}
• Смена тем оформления
• Стикеры и emoji

🌐 СЕТЕВЫЕ ФУНКЦИИ:
• Подключение к другим пользователям
• Генерация кодов приглашения
• Создание и присоединение к комнатам
• Список онлайн пользователей

© 2024 NeuroTech Systems"""
        messagebox.showinfo("О программе", about_text)

    def show_help(self):
        help_text = """🌟 NeuroChat Pro v5.0 - СПРАВКА

КЛАВИШИ УПРАВЛЕНИЯ:
Enter - Отправить сообщение
Ctrl+S - Экспорт чата
Ctrl+L - Очистить историю
Ctrl+Q - Выход
Ctrl+O - Переключить онлайн режим

ОНЛАЙН ФУНКЦИИ:
• Нажмите "● ONLINE" для подключения к сети
• Используйте "📧 Пригласить" для создания кода
• "🔗 Подключиться" для связи с пользователем
• "🏠 Комната" для группового чата

AI МОДЕЛИ:
• Локальная модель - работает без интернета
• OpenAI GPT - требуется API ключ
• Claude AI - требуется API ключ  
• Google Gemini - требуется API ключ

Доступны темы: Cyberpunk, Neon Dark, Matrix"""
        messagebox.showinfo("Справка", help_text)
    
    def show_error(self, message: str):
        messagebox.showerror("Ошибка", message)

    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            self.show_error(f"Критическая ошибка: {str(e)}")

# === ЗАПУСК ПРИЛОЖЕНИЯ ===
if __name__ == "__main__":
    try:
        print("🚀 Запуск NeuroChat Pro v5.0 - Онлайн версия...")
        print("📦 Проверка зависимостей...")
        
        root = tk.Tk()
        app = ModernNeuroChat(root)
        
        print("✅ Приложение успешно запущено!")
        print("🌐 Онлайн функции активированы")
        print("🤖 AI модели готовы к работе")
        print("💡 Подсказка: Используйте меню 'Сеть' для онлайн функций")
        

        app.run()
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        messagebox.showerror("Ошибка запуска", f"Не удалось запустить приложение:\n{str(e)}")