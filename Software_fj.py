#Tarea 4 POO
import tkinter as tk
from tkinter import messagebox
from abc import ABC,abstractmethod
from datetime import datetime

#logger: registro de errores con su respectiva fecha
def registrar_log(mensaje):
    with open("logs.txt","a",encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {mensaje}\n")

#Excepciones
class SistemaError(Exception):
    pass 
class ValidacionError(SistemaError):
    pass
class ReservaError(SistemaError):
    pass

#Clase abstracta
class Servicio(ABC):
    def __init__(self, nombre):
        self._nombre = nombre

    @abstractmethod
    def calcular_costo(self, duracion):
        pass

    @abstractmethod
    def descripcion(self):
        pass

# Clientes
class Cliente:
    def __init__(self, nombre, id, edad, mail):
        self.nombre = nombre
        self.id = id
        self.edad = edad
        self.mail = mail

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor) < 3:
            raise ValidacionError("Nombre inválido")
        self._nombre = valor

    @property
    def edad(self):
        return self._edad

    @edad.setter
    def edad(self, valor):
        if valor <= 0:
            raise ValidacionError("Edad inválida")
        self._edad = valor

    @property
    def mail(self):
        return self._mail

    @mail.setter
    def mail(self, valor):
        if "@" not in valor:
            raise ValidacionError("Email inválido")
        self._mail = valor

    def mostrar_info(self):
        return f"{self.nombre} ({self.edad}) - {self.mail}"

#Servicios
class ReservaSala(Servicio):
    def calcular_costo(self, duracion):
        return duracion * 50

    def descripcion(self):
        return "Reserva de Sala"


class AlquilerEquipo(Servicio):
    def calcular_costo(self, duracion):
        return duracion * 30

    def descripcion(self):
        return "Alquiler de Equipo"


class Asesoria(Servicio):
    def calcular_costo(self, duracion):
        return duracion * 100

    def descripcion(self):
        return "Asesoría Especializada"

#Reserva
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
        try:
            return self.servicio.calcular_costo(self.duracion)
        except Exception as e:
            raise ReservaError("Error al calcular costo") from e

#Sistema
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

            reserva = Reserva(cliente, servicio, int(duracion))
            total = reserva.calcular_total()

            reserva.confirmar()
            self.reservas.append(reserva)

            return total

        except Exception as e:
            registrar_log(str(e))
            raise







