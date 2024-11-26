import customtkinter as tk
import threading
from lib.Connection import Connection
from lib.utils import get_serial_ports
from lib.constants import MARGIN_Y

tk.set_appearance_mode("dark")
tk.set_default_color_theme("blue")


class App(tk.CTk):
    def __init__(self):
        super().__init__()
        self.total_steps = 0
        self.connected = "Desconectado"
        self.connection = None
        self.is_running = False
        self.geometry("900x600")
        self.title("Sistema de calibración de milimetros por paso")
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.button_ON = tk.CTkButton(
            self, text="Encender", state="disabled", command=self.turn_on
        )
        self.button_ON.grid(row=0, column=0, pady=MARGIN_Y)

        self.button_OFF = tk.CTkButton(
            self, text="Apagar", state="disabled", command=self.turn_off
        )
        self.button_OFF.grid(row=1, column=0, pady=MARGIN_Y)

        self.button_Connect = tk.CTkButton(self, text="Conectar", command=self.connect)
        self.button_Connect.grid(row=2, column=0, pady=MARGIN_Y)

        self.port_label = tk.CTkLabel(self, text="Puerto del Arduino")
        self.port_label.grid(row=3, column=0, pady=MARGIN_Y)

        self.port_checkbox = tk.CTkComboBox(self, values=get_serial_ports())
        self.port_checkbox.grid(row=4, column=0, pady=MARGIN_Y)
        self.refresh_button = tk.CTkButton(
            self, text="Actualizar Puertos", command=self.refresh_ports
        )
        self.refresh_button.grid(row=5, column=0, pady=MARGIN_Y)

        self.connection_status = tk.CTkCanvas(self, width=60, height=60, bg="gray")
        self.connection_status.grid(row=6, column=0, pady=MARGIN_Y)

        self.connection_status_label = tk.CTkLabel(
            self, text=f"Estado: {self.connected}"
        )
        self.connection_status_label.grid(row=7, column=0, pady=MARGIN_Y)

        self.is_getting_data_status = tk.CTkCanvas(self, width=20, height=20, bg="gray")
        self.is_getting_data_status.grid(row=0, column=1, pady=MARGIN_Y)

        self.is_getting_data_label = tk.CTkLabel(
            self, text="Sistema encendido capturando datos desde Arduino"
        )
        self.is_getting_data_label.grid(row=1, column=1, pady=MARGIN_Y)

        self.total_steps_read = tk.CTkLabel(
            self,
            text="Total de pasos leidos",
        )
        self.total_steps_read.grid(row=2, column=1, pady=MARGIN_Y)

        self.total_steps_entry = tk.CTkEntry(self, state="disabled")
        self.total_steps_entry.grid(row=3, column=1, pady=MARGIN_Y)

        self.history_label = tk.CTkLabel(
            self, text="Registro histórico", state="disabled"
        )
        self.history_label.grid(row=4, column=1, pady=MARGIN_Y)

        self.history_text = tk.CTkTextbox(self, height=200, width=200)
        self.history_text.grid(row=5, column=1, pady=MARGIN_Y)

        self.bottom_limit_status = tk.CTkCanvas(self, width=20, height=20, bg="gray")
        self.bottom_limit_status.grid(row=0, column=2, pady=MARGIN_Y)

        self.bottom_limit_label = tk.CTkLabel(
            self, text="Detcción extremo inferior LSD"
        )
        self.bottom_limit_label.grid(row=1, column=2, pady=MARGIN_Y)

        self.top_limit_status = tk.CTkCanvas(self, width=20, height=20, bg="gray")
        self.top_limit_status.grid(row=2, column=2, pady=MARGIN_Y)

        self.top_limit_label = tk.CTkLabel(self, text="Detcción extremo superior LSU")
        self.top_limit_label.grid(row=3, column=2, pady=MARGIN_Y)

    def refresh_ports(self):
        self.port_checkbox.set("")
        self.port_checkbox.configure(values=get_serial_ports())
        self.port_checkbox.set(get_serial_ports()[0])

    def get_port(self):
        if self.port_checkbox.get() == "No se encontraron puertos":
            error_message = tk.CTkToplevel(self)
            error_message.geometry("300x100")
            error_message_label = tk.CTkLabel(
                error_message, text="No se encontraron puertos disponibles"
            )
            error_message_label.pack()
            error_message_button = tk.CTkButton(
                error_message, text="Cerrar", command=error_message.destroy
            )
            error_message_button.pack()

            error_message.grab_set()
            self.wait_window(error_message)

            return None

        return self.port_checkbox.get()

    def connect(self):
        port = self.get_port()
        if port is None:
            return

        self.connection = Connection(port, 9600)

        if self.connection.is_open:
            self.connected = "Conectado"
            self.connection_status.configure(bg="green")
            self.connection_status_label.configure(text=f"Estado: {self.connected}")
            self.button_ON.configure(state="normal")
            self.button_OFF.configure(state="normal")

    def close_connection(self):
        if self.connection.disconnect():
            self.connected = "Desconectado"
            self.connection_status.configure(bg="gray")
            self.connection_status_label.configure(text=f"Estado: {self.connected}")

    def turn_on(self):
        self.is_getting_data_status.configure(bg="green")
        self.is_running = True
        self.connection.write("ON".encode("utf-8"))
        threading.Thread(target=self.start_reading).start()

    def turn_off(self):
        self.is_getting_data_status.configure(bg="gray")
        self.is_running = False
        self.connection.write("OFF".encode("utf-8"))

    def start_reading(self):
        while self.is_running:
            data = self.connection.readline().decode("utf-8").strip()

            if data == "LSU":
                print("Limite superior detectado")
                self.top_limit_status.configure(bg="green")
            elif data == "LSD":
                print("Limite inferior detectado")
                self.bottom_limit_status.configure(bg="green")
            elif "Pasos: " in data:
                self.total_steps = int(data.split(": ")[1])
                self.total_steps_entry.configure(state="normal")
                self.total_steps_entry.delete(0, tk.END)
                self.total_steps_entry.insert(0, self.total_steps)
                self.total_steps_entry.configure(state="disabled")

                self.top_limit_status.configure(bg="gray")
                self.bottom_limit_status.configure(bg="gray")
            else:
                self.history_text.insert(tk.END, data + "\n")
                self.top_limit_status.configure(bg="gray")
                self.bottom_limit_status.configure(bg="gray")


if __name__ == "__main__":
    app = App()
    app.mainloop()
    app.connection.close()
