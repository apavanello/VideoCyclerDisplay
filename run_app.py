# run_app.py

import os
import sys
import threading
import webbrowser
import tkinter as tk
from tkinter import font as tkfont
from waitress import serve
import traceback  # 1. Importe a biblioteca traceback
import time  # 2. Importe a biblioteca time

# --- Bloco de inicialização do Django ---
# Vamos tentar inicializar o Django aqui fora para capturar o erro mais cedo.
try:
    # Configura o ambiente Django
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    import django

    django.setup()

    # Se chegarmos aqui, o Django foi configurado com sucesso.
    from core.wsgi import application

except Exception as e:
    # 3. Se a configuração do Django falhar, este é o nosso ponto de captura
    print("=" * 80)
    print("!!! ERRO FATAL DURANTE A INICIALIZAÇÃO DO DJANGO !!!")
    print("=" * 80)

    # Imprime o traceback completo do erro real
    traceback.print_exc()

    print("\n" * 2)
    print("A aplicação irá fechar em 30 segundos...")
    time.sleep(30)  # Pausa para que você possa ler o erro
    sys.exit(1)  # Sai com um código de erro

# --- O resto do código só será executado se o Django iniciar com sucesso ---

HOST = '127.0.0.1'
PORT = 8000
URL_DISPLAY = f"http://{HOST}:{PORT}/"
URL_ADMIN = f"http://{HOST}:{PORT}/admin/"


def run_server():
    print(f"Iniciando servidor em http://{HOST}:{PORT}")
    serve(application, host=HOST, port=PORT)


def open_display_page():
    print(f"Abrindo página do display: {URL_DISPLAY}")
    webbrowser.open_new(URL_DISPLAY)


def open_admin_page():
    print(f"Abrindo página de admin: {URL_ADMIN}")
    webbrowser.open_new(URL_ADMIN)


def on_closing():
    print("Fechando a aplicação...")
    root.destroy()
    os._exit(0)


if __name__ == '__main__':
    # A inicialização do Django já aconteceu. Se chegamos aqui, está tudo bem.
    print("Inicialização do Django bem-sucedida. Iniciando a GUI...")

    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    root = tk.Tk()
    root.title("Painel de Controle do Display")

    window_width = 300
    window_height = 180
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    root.resizable(False, False)

    button_font = tkfont.Font(family="Helvetica", size=12)
    label_font = tkfont.Font(family="Helvetica", size=10)

    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(expand=True, fill="both")

    btn_display = tk.Button(main_frame, text="Abrir Display", font=button_font, command=open_display_page, width=20)
    btn_display.pack(pady=5)

    btn_admin = tk.Button(main_frame, text="Acessar Admin", font=button_font, command=open_admin_page, width=20)
    btn_admin.pack(pady=5)

    status_label = tk.Label(main_frame, text=f"Servidor rodando em {HOST}:{PORT}", font=label_font, fg="gray")
    status_label.pack(pady=(10, 0))

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()