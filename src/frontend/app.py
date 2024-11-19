import customtkinter as tk

tk.set_appearance_mode("dark")
tk.set_default_color_theme("blue")


class App(tk.CTk):
    def __init__(self):
        super().__init__()
        self.connected = "Desconectado"

        self.geometry("900x600")
        self.title("Sistema de calibración de milimetros por paso")
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.button_ON = tk.CTkButton(self, text="Encender")
        self.button_ON.grid(row=0, column=0)

        self.button_OFF = tk.CTkButton(self, text="Apagar")
        self.button_OFF.grid(row=1, column=0)

        self.button_Connect = tk.CTkButton(self, text="Conectar")
        self.button_Connect.grid(row=2, column=0)

        self.port_label = tk.CTkLabel(self, text="Puerto del Arduino")
        self.port_label.grid(row=3, column=0)
        self.port_checkbox = tk.CTkComboBox(self, values=["COM1", "COM2", "COM3"])
        self.port_checkbox.grid(row=4, column=0)

        self.connectionn_status = tk.CTkCanvas(self, width=60, height=60, bg="gray")
        self.connectionn_status.grid(row=5, column=0)

        self.connection_status_label = tk.CTkLabel(
            self, text=f"Estado: {self.connected}"
        )
        self.connection_status_label.grid(row=6, column=0)

        self.is_getting_data_status = tk.CTkCanvas(self, width=20, height=20, bg="gray")
        self.is_getting_data_status.grid(row=0, column=1)

        self.is_getting_data_label = tk.CTkLabel(
            self, text="Sistema encendido capturando datos desde Arduino"
        )
        self.is_getting_data_label.grid(row=1, column=1)

        self.total_steps_read = tk.CTkLabel(self, text="Total de pasos leidos")
        self.total_steps_read.grid(row=2, column=1)

        self.total_steps_entry = tk.CTkEntry(self)
        self.total_steps_entry.grid(row=3, column=1)

        self.history_label = tk.CTkLabel(self, text="Registro histórico")
        self.history_label.grid(row=4, column=1)

        self.history_text = tk.CTkEntry(self, height=200, width=200)
        self.history_text.grid(row=5, column=1)

        self.bottom_limit_status = tk.CTkCanvas(self, width=20, height=20, bg="gray")
        self.bottom_limit_status.grid(row=0, column=2)

        self.bottom_limit_label = tk.CTkLabel(
            self, text="Detcción extremo inferior LSD"
        )
        self.bottom_limit_label.grid(row=1, column=2)

        self.top_limit_status = tk.CTkCanvas(self, width=20, height=20, bg="gray")
        self.top_limit_status.grid(row=2, column=2)

        self.top_limit_label = tk.CTkLabel(self, text="Detcción extremo superior LSU")
        self.top_limit_label.grid(row=3, column=2)


if __name__ == "__main__":
    app = App()
    app.mainloop()
