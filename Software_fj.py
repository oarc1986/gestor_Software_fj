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

