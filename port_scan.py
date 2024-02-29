import socket
import ipaddress
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import threading

def validate_ports(start_port, end_port):
    try:
        start_port = int(start_port)
        end_port = int(end_port)
        if 1 <= start_port <= 65535 and 1 <= end_port <= 65535 and start_port <= end_port:
            return True
    except ValueError:
        pass
    return False

def scan_ports(host, start_port, end_port, output_text):
    
    output_text.delete(1.0, tk.END)  # Limpa o texto anterior

    open_ports = []

    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            service_name = get_service_name(port)
            output_text.insert(tk.END, f"Porta {port}: {service_name}\n")
            open_ports.append(port)
        sock.close()

    show_completion_message(open_ports)

def get_service_name(port):
    try:
        service_name = socket.getservbyport(port)
    except OSError:
        service_name = "Desconhecido"
    return service_name

def show_completion_message(open_ports):
    if open_ports:
        messagebox.showinfo("Concluído", f"Escaneamento concluído. Portas abertas: {', '.join(map(str, open_ports))}")
    else:
        messagebox.showinfo("Concluído", "Escaneamento concluído. Nenhuma porta aberta encontrada.")

def scan_and_display():
    host = entry_host.get()
    start_port = entry_start_port.get()
    end_port = entry_end_port.get()

    if not validate_ports(start_port, end_port):
        messagebox.showerror("Erro", "Intervalo de portas inválido.")
        return

    start_port, end_port = int(start_port), int(end_port)

    # Iniciar escaneamento em uma thread separada
    threading.Thread(target=scan_ports, args=(host, start_port, end_port, result_text)).start()

# Criando a interface gráfica
app = tk.Tk()
app.title("Scanner de Portas")

label_host = tk.Label(app, text="Host ou IP:")
label_host.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

entry_host = tk.Entry(app)
entry_host.grid(row=0, column=1, padx=10, pady=5)

label_start_port = tk.Label(app, text="Porta Inicial:")
label_start_port.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

entry_start_port = tk.Entry(app)
entry_start_port.grid(row=1, column=1, padx=10, pady=5)

label_end_port = tk.Label(app, text="Porta Final:")
label_end_port.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

entry_end_port = tk.Entry(app)
entry_end_port.grid(row=2, column=1, padx=10, pady=5)

scan_button = tk.Button(app, text="Escanear Portas", command=scan_and_display)
scan_button.grid(row=3, column=0, columnspan=2, pady=10)

result_text = scrolledtext.ScrolledText(app, height=10, width=40)
result_text.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

app.mainloop()