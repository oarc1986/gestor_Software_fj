#Tarea 4 POO
import tkinter as tk
from tkinter import messagebox
from abc import ABC,abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self,nombre,id,edad,mail):
        self._nombre=nombre
        self._edad=edad
        self._id=id
        self._mail=mail

    

