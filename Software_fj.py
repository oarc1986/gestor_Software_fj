import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod
from datetime import datetime

# Logger
def registrar_log(mensaje):
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {mensaje}\n")


# Excepciones
class SistemaError(Exception):
    pass

class ValidacionError(SistemaError):
    pass

class ReservaError(SistemaError):
    pass


# Clase abstracta
class Servicio(ABC):

    @abstractmethod
    def calcular_costo(self, duracion):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# Servicios
class ReservaSala(Servicio):
    def calcular_costo(self, duracion):
        if duracion <= 0:
            raise ReservaError("Duración inválida")
        return duracion * 50

    def descripcion(self):
        return "Reserva de Sala"


class AlquilerEquipo(Servicio):
    def calcular_costo(self, duracion):
        if duracion <= 0:
            raise ReservaError("Duración inválida")
        return duracion * 30

    def descripcion(self):
        return "Alquiler de Equipo"


class Asesoria(Servicio):
    def calcular_costo(self, duracion):
        if duracion <= 0:
            raise ReservaError("Duración inválida")
        return duracion * 100

    def descripcion(self):
        return "Asesoría Especializada"


# Cliente
class Cliente:
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor) < 3:
            raise ValidacionError("Nombre inválido")
        self._nombre = valor

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if "@" not in valor:
            raise ValidacionError("Email inválido")
        self._email = valor


# Reserva
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "pendiente"

    def confirmar(self):
        if self.estado != "pendiente":
            raise ReservaError("Ya confirmada o cancelada")
        self.estado = "confirmada"

    def calcular_total(self):
        return self.servicio.calcular_costo(self.duracion)


# Sistema
class Sistema:
    def __init__(self):
        self.reservas = []

    def crear_reserva(self, nombre, email, tipo_servicio, duracion):
        try:
            cliente = Cliente(nombre, email)

            if tipo_servicio == "Sala":
                servicio = ReservaSala()
            elif tipo_servicio == "Equipo":
                servicio = AlquilerEquipo()
            else:
                servicio = Asesoria()

            try:
                duracion = int(duracion)
            except:
                raise ReservaError("Duración debe ser un número")

            reserva = Reserva(cliente, servicio, duracion)
            total = reserva.calcular_total()
            reserva.confirmar()
            self.reservas.append(reserva)

            return total

        except Exception as e:
            registrar_log(str(e))
            raise


# Interfaz
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ")

        self.sistema = Sistema()

        # UI
        tk.Label(root, text="Nombre").grid(row=0, column=0)
        self.nombre = tk.Entry(root)
        self.nombre.grid(row=0, column=1)

        tk.Label(root, text="Email").grid(row=1, column=0)
        self.email = tk.Entry(root)
        self.email.grid(row=1, column=1)

        tk.Label(root, text="Duración").grid(row=2, column=0)
        self.duracion = tk.Entry(root)
        self.duracion.grid(row=2, column=1)

        self.tipo = tk.StringVar(value="Sala")
        tk.OptionMenu(root, self.tipo, "Sala", "Equipo", "Asesoría").grid(row=3, column=1)

        tk.Button(root, text="Crear Reserva", command=self.crear_reserva).grid(row=4, column=0, columnspan=2)
        tk.Button(root, text="Simular", command=self.iniciar_simulacion).grid(row=5, column=0, columnspan=2)

        self.texto = tk.Text(root, height=15, width=50)
        self.texto.grid(row=6, column=0, columnspan=2)

    def crear_reserva(self):
        try:
            total = self.sistema.crear_reserva(
                self.nombre.get(),
                self.email.get(),
                self.tipo.get(),
                self.duracion.get()
            )
            messagebox.showinfo("Éxito", f"Total: ${total}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def iniciar_simulacion(self):
        self.pruebas = [
            ("Oscar", "oscar@mail.com", "Sala", 2),
            ("Lu", "correo@mail.com", "Equipo", 3),
            ("Maria", "maria_mail.com", "Sala", 2),
            ("Pedro", "pedro@mail.com", "Asesoría", "abc"),
            ("Ana", "ana@mail.com", "Sala", 5),
            ("Carlos", "carlos@mail.com", "Equipo", 1),
            ("", "test@mail.com", "Sala", 2),
            ("Laura", "laura@mail.com", "Asesoría", 3),
            ("Miguel", "miguel@mail.com", "Sala", -1),
            ("Sofia", "sofia@mail.com", "Equipo", 2),
        ]

        self.indice_simulacion = 0
        self.texto.delete("1.0", tk.END)

        self.root.after(100, self.ejecutar_paso)

    def ejecutar_paso(self):
        if self.indice_simulacion >= len(self.pruebas):
            return

        datos = self.pruebas[self.indice_simulacion]

        try:
            total = self.sistema.crear_reserva(*datos)
            resultado = f"{self.indice_simulacion+1}. OK - ${total}"
        except Exception as e:
            resultado = f"{self.indice_simulacion+1}. ERROR - {e}"

        self.texto.insert(tk.END, resultado + "\n")

        self.indice_simulacion += 1
        self.root.after(200, self.ejecutar_paso)



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()