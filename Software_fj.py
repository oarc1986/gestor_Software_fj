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



