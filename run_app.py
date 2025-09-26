import os
import sys
import multiprocessing

# --- FUNÇÃO DO SERVIDOR (NÍVEL SUPERIOR) ---
# Esta função é o ponto de entrada para o novo processo do servidor.
# Ela é agora totalmente autônoma.
def run_waitress(host, port):
    """
    Função alvo para o processo do servidor.
    IMPORTANTE: Ela inicializa o Django DENTRO do seu próprio processo.
    """
    try:
        # Configura o ambiente Django para este novo processo.
        project_root = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, project_root)
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
        import django
        django.setup()

        # Importa a aplicação WSGI e o servidor AQUI, dentro do processo.
        from core.wsgi import application
        from waitress import serve
        
        print(f"Iniciando servidor (PID: {os.getpid()}) em http://{host}:{port}")
        serve(application, host=host, port=port)
    except Exception as e:
        # Em uma aplicação real, seria bom ter um log aqui.
        print(f"Erro fatal no processo do servidor: {e}")

# --- Ponto de Entrada Lógico e Desvio de Execução ---
def main():
    if '--createsuperuser' in sys.argv:
        from admin_setup import create_superuser_interactive
        create_superuser_interactive()
        sys.exit(0)
    else:
        run_gui_application()

def run_gui_application():
    """Contém toda a lógica para a aplicação com interface gráfica."""
    import webbrowser
    import tkinter as tk
    from tkinter import font as tkfont, messagebox
    import traceback
    import subprocess

    # --- Pré-verificação do Django ---
    # A GUI ainda faz uma verificação para garantir que a configuração é válida antes de iniciar.
    try:
        project_root = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, project_root)
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
        import django
        django.setup()
    except Exception as e:
        traceback.print_exc()
        messagebox.showerror("Erro Fatal", f"Não foi possível validar a configuração do Django. A aplicação será fechada.\n\nErro: {e}")
        sys.exit(1)

    # --- Variáveis Globais da GUI ---
    server_process = None
    URL_DISPLAY_LOCAL = ""
    URL_ADMIN_LOCAL = ""

    # --- Funções da Interface ---
    def start_server():
        nonlocal server_process, URL_DISPLAY_LOCAL, URL_ADMIN_LOCAL
        host = host_entry.get().strip()
        port_str = port_entry.get().strip()
        if not port_str.isdigit() or not (1 <= int(port_str) <= 65535):
            messagebox.showerror("Erro de Validação", "A porta deve ser um número entre 1 e 65535.")
            return
        
        port = int(port_str)
        URL_DISPLAY_LOCAL = f"http://127.0.0.1:{port}/"
        URL_ADMIN_LOCAL = f"http://127.0.0.1:{port}/admin/"
        
        # O alvo é a função global 'run_waitress'.
        # NÃO passamos mais o objeto 'application'.
        server_process = multiprocessing.Process(target=run_waitress, args=(host, port))
        server_process.daemon = True
        server_process.start()
        
        print("Processo do servidor iniciado.")
        update_gui_state(is_running=True, host=host, port=port)

    # ... (O resto das funções: stop_server, open_display_page, etc. permanecem as mesmas)
    def stop_server():
        nonlocal server_process
        if server_process and server_process.is_alive():
            print("Parando o processo do servidor...")
            server_process.terminate()
            server_process.join()
            server_process = None
            print("Servidor parado.")
            update_gui_state(is_running=False)

    def open_display_page():
        webbrowser.open_new(URL_DISPLAY_LOCAL)

    def open_admin_page():
        webbrowser.open_new(URL_ADMIN_LOCAL)

    def run_createsuperuser_process():
        command_list = [sys.executable, '--createsuperuser']
        subprocess.Popen(command_list, creationflags=subprocess.CREATE_NEW_CONSOLE)

    def on_closing():
        if messagebox.askokcancel("Sair", "Tem certeza que deseja fechar a aplicação? O servidor será parado."):
            stop_server()
            print("Fechando a aplicação...")
            root.destroy()
            os._exit(0)

    def update_gui_state(is_running, host=None, port=None):
        state_map = {
            'stopped': {'start': 'normal', 'stop': 'disabled', 'display': 'disabled', 'admin': 'disabled', 'host': 'normal', 'port': 'normal'},
            'running': {'start': 'disabled', 'stop': 'normal', 'display': 'normal', 'admin': 'normal', 'host': 'disabled', 'port': 'disabled'},
        }
        current_state = 'running' if is_running else 'stopped'
        host_entry.config(state=state_map[current_state]['host'])
        port_entry.config(state=state_map[current_state]['port'])
        btn_start.config(state=state_map[current_state]['start'])
        btn_stop.config(state=state_map[current_state]['stop'])
        btn_display.config(state=state_map[current_state]['display'])
        btn_admin.config(state=state_map[current_state]['admin'])
        if is_running:
            status_label.config(text=f"Servidor rodando em {host}:{port}", fg="green")
        else:
            status_label.config(text="Servidor parado. Preencha os dados e clique em 'Iniciar'.", fg="gray")
    
    # --- Criação e Loop Principal da GUI ---
    root = tk.Tk()
    # ... (O resto do seu código de criação da GUI permanece o mesmo)
    root.title("Painel de Controle do Display")
    root.resizable(False, False)
    button_font = tkfont.Font(family="Helvetica", size=11)
    label_font = tkfont.Font(family="Helvetica", size=10)
    entry_font = tkfont.Font(family="Helvetica", size=11)
    main_frame = tk.Frame(root, padx=15, pady=15)
    main_frame.pack(expand=True, fill="both")
    config_frame = tk.Frame(main_frame, pady=10)
    config_frame.pack(fill='x')
    tk.Label(config_frame, text="Host:", font=label_font).grid(row=0, column=0, sticky='w', padx=5)
    host_entry = tk.Entry(config_frame, font=entry_font, width=15)
    host_entry.insert(0, "0.0.0.0")
    host_entry.grid(row=0, column=1, sticky='ew')
    tk.Label(config_frame, text="Porta:", font=label_font).grid(row=1, column=0, sticky='w', padx=5, pady=5)
    port_entry = tk.Entry(config_frame, font=entry_font, width=15)
    port_entry.insert(0, "8000")
    port_entry.grid(row=1, column=1, sticky='ew')
    config_frame.grid_columnconfigure(1, weight=1)
    server_control_frame = tk.Frame(main_frame)
    server_control_frame.pack(fill='x', pady=5)
    btn_start = tk.Button(server_control_frame, text="Iniciar Servidor", font=button_font, command=start_server, bg="#4CAF50", fg="white")
    btn_start.pack(side='left', expand=True, fill='x', padx=2)
    btn_stop = tk.Button(server_control_frame, text="Parar Servidor", font=button_font, command=stop_server, bg="#f44336", fg="white")
    btn_stop.pack(side='left', expand=True, fill='x', padx=2)
    actions_frame = tk.Frame(main_frame, pady=10)
    actions_frame.pack(fill='x')
    btn_display = tk.Button(actions_frame, text="Abrir Display", font=button_font, command=open_display_page)
    btn_display.pack(fill='x', pady=2)
    btn_admin = tk.Button(actions_frame, text="Acessar Admin", font=button_font, command=open_admin_page)
    btn_admin.pack(fill='x', pady=2)
    btn_createsuperuser = tk.Button(actions_frame, text="Criar Superusuário", font=button_font, command=run_createsuperuser_process)
    btn_createsuperuser.pack(fill='x', pady=2)
    status_label = tk.Label(main_frame, text="", font=label_font, fg="gray", wraplength=280)
    status_label.pack(pady=(10, 0))
    update_gui_state(is_running=False)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

# Ponto de entrada final do script
if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()